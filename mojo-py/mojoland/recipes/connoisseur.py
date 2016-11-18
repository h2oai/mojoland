#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
import colorama
import os
import re
from typing import Dict, Generator, List, Optional, Tuple, Type

import h2o
from mojoland import MojoModel, MojoUnstableError
from .baserecipe import MojoRecipe

colorama.init()



class Connoisseur:

    def __init__(self):
        self._latest_mojo_versions = Connoisseur._retrieve_mojo_versions()


    def degustate(self, recipe: Type[MojoRecipe]):
        assert issubclass(recipe, MojoRecipe), "%r is not a subclass of MojoRecipe" % recipe
        flavor, dish = self._name_parts(recipe)

        print(colorama.Fore.YELLOW)
        print("#----------------------------------------------------------")
        print("#  Tasting %s %s recipe" % (flavor.capitalize(), dish.capitalize()))
        print("#----------------------------------------------------------")
        print(colorama.Fore.RESET)

        self._bake_if_needed(recipe)

        for version in self._enumerate_dish_versions(flavor, dish):
            self._taste(recipe, version)


    #-------------------------------------------------------------------------------------------------------------------
    # Private
    #-------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def _retrieve_mojo_versions() -> Dict[str, str]:
        """Return a map {algo: algos_latest_mojo_version}."""
        models_info = h2o.api("GET /4/modelsinfo")["models"]
        mojo_versions = {}
        for mi in models_info:
            assert "have_mojo" in mi and "mojo_version" in mi, "Invalid /4/modelsinfo entry: %r" % mi
            if mi["have_mojo"]:
                version = mi["mojo_version"]
                assert isinstance(version, str) and len(version) >= 4 and version[-3] == ".", \
                    "Unexpected version number: %r" % version
                if version == "1.00":
                    version = "0.01"
                mojo_versions[mi["algo"]] = version
        return mojo_versions


    #---- Naming ---------------------------------------------------------------

    def _mojo_dirname(self, flavor: str, dish: str, version: str) -> str:
        recipesdir = os.path.dirname(__file__)
        targetdir = os.path.abspath(os.path.join(recipesdir, "..", "..", "..", "mojo-data", "mojos"))
        assert os.path.isdir(targetdir), "Directory %s cannot be found (%s)" % (targetdir, __file__)
        return os.path.join(targetdir, flavor, dish, version)


    def _mojo_filename(self, flavor: str, dish: str, version: str = None) -> str:
        if version is None:
            version = "v" + self._latest_mojo_versions[flavor]
        dirname = self._mojo_dirname(flavor, dish, version)
        mojoname = "%s_%s_%s.mojo" % (flavor, version, dish)
        return os.path.join(dirname, mojoname)


    def _nibble_filename(self, flavor: str, dish: str, version: str, nibble_name: str) -> str:
        return self._mojo_filename(flavor, dish, version)[:-5] + "_" + nibble_name + ".txt"


    def _name_parts(self, recipe: Type[MojoRecipe]):
        """
        Retrieve the recipe's name parts, based on class naming convention.

        The class name should follow the pattern {Dataset}{Algo}Recipe, for
        example "IrisGbmRecipe" or "Airlines1DrfRecipe". This also returns the
        latest mojo version of the algo (which is retrieved from the server).

        @returns: tuple (algo, dataset)
        """
        classname = recipe.__name__
        parts = re.split("([A-Z][a-z0-9]*)", classname)[1::2]  # split into camel-cased parts
        assert len(parts) == 3 and parts[2] == "Recipe", "Unexpected class name: %s" % classname
        dataset = parts[0].lower()
        algo = parts[1].lower()
        return algo, dataset


    #---- Baking ---------------------------------------------------------------

    def _is_cooked(self, flavor: str, dish: str) -> bool:
        mojoname = self._mojo_filename(flavor, dish)
        return os.path.isfile(mojoname)


    def _bake_if_needed(self, recipe: Type[MojoRecipe]) -> None:
        flavor, dish = self._name_parts(recipe)
        if self._is_cooked(flavor, dish):
            return

        print("Baking the recipe...")
        h2omodel = recipe().bake()
        print()

        mojoname = self._mojo_filename(flavor, dish)
        print("Saving the mojo to %s" % mojoname)
        dirname = os.path.dirname(mojoname)
        tmp_mojofile = h2omodel.download_mojo(dirname)
        os.rename(tmp_mojofile, mojoname)
        print()


    #---- Tasting --------------------------------------------------------------

    def _enumerate_dish_versions(self, flavor: str, dish: str) -> List[str]:
        parentdir = os.path.abspath(self._mojo_dirname(flavor, dish, "."))
        dirnames = next(os.walk(parentdir, topdown=True))[1]
        return dirnames


    def _taste(self, recipe: Type[MojoRecipe], vversion: str) -> None:
        flavor, dish = self._name_parts(recipe)
        mojo_filename = self._mojo_filename(flavor, dish, vversion)
        assert os.path.exists(mojo_filename), "Mojo file %s does not exist" % mojo_filename
        mojo = MojoModel(mojo_filename, int(vversion[1:-3]))
        for nibble_name, commands in recipe().nibbles(mojo):
            nibble_filename = self._nibble_filename(flavor, dish, vversion, nibble_name)
            nibble_original = self._read_nibble(nibble_filename)
            nibble_fresh = self._make_nibble(mojo, commands)
            if nibble_original is None:
                print("Creating %s -> %s" % (nibble_name, nibble_filename))
                with open(nibble_filename, "w") as f:
                    f.write(nibble_fresh)
            else:
                print("Testing %s vs %s... " % (nibble_name, nibble_filename), end="")
                if nibble_fresh == nibble_original:
                    print("ok")
                else:
                    print(colorama.Fore.LIGHTRED_EX + "fail" + colorama.Fore.RESET)
                    tmp_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "temp"))
                    tmp_file = os.path.join(tmp_dir, os.path.basename(nibble_filename))
                    with open(tmp_file, "w") as f:
                        f.write(nibble_fresh)
                    self._print_diff(nibble_original, nibble_fresh)
                    raise MojoUnstableError("Mismatch in artifact %s of mojo %s; new artifact saved in %s" %
                                            (nibble_name, os.path.basename(mojo_filename), tmp_file))
        mojo.close()


    def _read_nibble(self, filename: str) -> Optional[str]:
        if os.path.exists(filename):
            with open(filename, "r") as f:
                return f.read()
        return None


    def _make_nibble(self, mojo: MojoModel, commands: Generator[Tuple[str, ...], None, None]) -> str:
        out = ""
        for command in commands:
            res = mojo.call(*command)
            out += res + "\n"
        return out


    def _print_diff(self, original, fresh):
        lines_original = original.split("\n")
        lines_fresh = fresh.split("\n")
        if len(lines_original) != len(lines_fresh):
            print("Original has %d lines and computed has %d lines" % (len(lines_original), len(lines_fresh)))
        else:
            for i in range(len(lines_fresh)):
                if lines_original[i] != lines_fresh[i]:
                    print("Difference in line %d:" % (i + 1))
                    print("Original: %s" % lines_original[i])
                    print("Computed: %s" % lines_fresh[i])
                    break



