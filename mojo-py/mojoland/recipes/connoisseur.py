#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
import colorama
import os
import re
from typing import Callable, Dict, Iterator, List, Optional, Tuple, Type

import h2o
from mojoland import MojoModel, get_backend
from .baserecipe import BaseRecipe


class Connoisseur:

    def __init__(self, *, backend):
        # Initialize external connectors
        colorama.init()
        h2o.init()
        self._backend = get_backend(backend)
        print()
        # Create the class
        self._latest_mojo_versions = Connoisseur._retrieve_mojo_versions()
        self._can_bake = False


    def degustate(self, recipe: Type[BaseRecipe]):
        assert issubclass(recipe, BaseRecipe), "%r is not a subclass of MojoRecipe" % recipe
        flavor, dish = self._name_parts(recipe)

        print(colorama.Fore.LIGHTYELLOW_EX)
        print("#----------------------------------------------------------")
        print("#  Tasting %s %s recipe" % (flavor.capitalize(), dish.capitalize()))
        print("#----------------------------------------------------------")
        print(colorama.Fore.RESET)

        self._bake_if_needed(recipe)

        for version in self._enumerate_dish_versions(flavor, dish):
            self._taste(recipe, version)


    @property
    def can_bake(self) -> bool:
        return self._can_bake

    @can_bake.setter
    def can_bake(self, value: bool):
        self._can_bake = value


    #-------------------------------------------------------------------------------------------------------------------
    # Private
    #-------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def _retrieve_mojo_versions() -> Dict[str, str]:
        """Return a map {algo: algo's_latest_mojo_version}."""
        models_info = h2o.api("GET /4/modelsinfo")["models"]
        mojo_versions = {}
        for mi in models_info:
            assert "have_mojo" in mi and "mojo_version" in mi, "Invalid /4/modelsinfo entry: %r" % mi
            if mi["have_mojo"]:
                version = mi["mojo_version"]
                assert isinstance(version, str) and len(version) >= 4 and version[-3] == ".", \
                    "Unexpected version number: %r" % version
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


    def _name_parts(self, recipe: Type[BaseRecipe]):
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


    def _bake_if_needed(self, recipe: Type[BaseRecipe]) -> None:
        flavor, dish = self._name_parts(recipe)
        if self._is_cooked(flavor, dish):
            return

        if not self._can_bake:
            raise MojoNotFoundError("Mojo for recipe %s not found" % recipe.__name__)

        print("Baking the recipe...")
        h2omodel = recipe().bake()
        print()

        mojoname = self._mojo_filename(flavor, dish)
        print("Saving the mojo to %s" % mojoname)
        h2omodel.download_mojo(mojoname)
        print()


    #---- Tasting --------------------------------------------------------------

    def _enumerate_dish_versions(self, flavor: str, dish: str) -> List[str]:
        parentdir = os.path.abspath(self._mojo_dirname(flavor, dish, "."))
        dirnames = next(os.walk(parentdir, topdown=True))[1]
        return dirnames


    def _taste(self, recipe: Type[BaseRecipe], vversion: str) -> None:
        flavor, dish = self._name_parts(recipe)
        mojo_filename = self._mojo_filename(flavor, dish, vversion)
        assert os.path.exists(mojo_filename), "Mojo file %s does not exist" % mojo_filename
        mojo = MojoModel(mojo_filename, int(vversion[1:-3]), backend=self._backend)
        for nibble_name, commands in recipe().nibbles(mojo):
            nibble_filename = self._nibble_filename(flavor, dish, vversion, nibble_name)
            nibble_original = self._read_nibble(nibble_filename)
            nibble_fresh = self._make_nibble(mojo, commands)
            if nibble_original is None:
                if not self._can_bake:
                    raise MojoNotFoundError("Nibble %s for mojo %s not found" % (nibble_name, recipe.__name__))
                print("Making nibble %s -> %s" %
                      (colorama.Fore.LIGHTCYAN_EX + nibble_name + colorama.Fore.RESET, nibble_filename))
                with open(nibble_filename, "w") as f:
                    f.write(nibble_fresh)
                # Verify that it is possible to reproduce the results...
                nibble_original = self._make_nibble(mojo, commands)
                if nibble_original != nibble_fresh:
                    tmp_file = self._write_temp_nibble(nibble_original, nibble_filename)
                    raise MojoUnstableError("Nibble %s of mojo %s is unstable; comparison nibble save in %s" %
                                            (nibble_name, os.path.basename(mojo_filename), tmp_file))
            else:
                print("Tasting nibble %s in %s... " %
                      (colorama.Fore.LIGHTCYAN_EX + nibble_name + colorama.Fore.RESET, nibble_filename), end="")
                res = self._compare_nibbles(nibble_fresh, nibble_original, 1e-10)
                if res is None:
                    print("ok")
                else:
                    print(colorama.Fore.LIGHTRED_EX + "fail" + colorama.Fore.RESET)
                    tmp_file = self._write_temp_nibble(nibble_fresh, nibble_filename)
                    self._print_diff(nibble_original, nibble_fresh, list(commands()), res)
                    raise MojoUnstableError("Mismatch in nibble %s of mojo %s; new nibble saved in %s" %
                                            (nibble_name, os.path.basename(mojo_filename), tmp_file))
        mojo.close()


    def _compare_nibbles(self, fresh, original, tolerance):
        """
        Test whether 2 nibbles are same, allowing for numeric differences up to `tolerance`.
        :returns: None if two nibbles are same, otherwise line number where the mismatch occurred
            (or -1 if two files have different number of lines)
        """
        lines_original = original.split("\n")
        lines_fresh = fresh.split("\n")
        re_float = re.compile(r"\s*[+-]?\d+(?:\.\d*)?(?:[eE][+-]?\d+)?\s*")
        if len(lines_original) == len(lines_fresh):
            for i in range(len(lines_fresh)):
                oline = lines_original[i]
                fline = lines_fresh[i]
                if oline == lines_fresh[i]:
                    continue
                if oline.startswith("[") and oline.endswith("]"):
                    oelems = oline[1:-1].split(",")
                    felems = fline[1:-1].split(",")
                    if len(oelems) != len(felems):
                        return i
                    for j in range(len(oelems)):
                        if re.match(re_float, oelems[j]) and re.match(re_float, felems[j]):
                            x = float(oelems[j])
                            y = float(felems[j])
                            if abs(x - y) > tolerance:
                                return i
                        elif oelems[j] != felems[j]:
                            return i
                elif re.match(re_float, oline) and re.match(re_float, fline):
                    x = float(oline)
                    y = float(fline)
                    if abs(x - y) > tolerance:
                        return i
                else:
                    return i
            return None
        else:
            return -1


    def _read_nibble(self, filename: str) -> Optional[str]:
        if os.path.exists(filename):
            with open(filename, "r") as f:
                return f.read()
        return None


    def _make_nibble(self, mojo: MojoModel, commands: Callable[[], Iterator[Tuple[str, ...]]]) -> str:
        out = ""
        for command in commands():
            res = mojo.call(*command)
            out += res + "\n"
        return out


    def _write_temp_nibble(self, nibble_text: str, nibble_filename: str) -> str:
        tmp_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "temp"))
        tmp_file = os.path.join(tmp_dir, os.path.basename(nibble_filename))
        with open(tmp_file, "w") as f:
            f.write(nibble_text)
        return tmp_file


    def _print_diff(self, original, fresh, commands, lineno):
        lines_original = original.split("\n")
        lines_fresh = fresh.split("\n")
        if lineno == -1:
            print("Original has %d lines and computed has %d lines" % (len(lines_original), len(lines_fresh)))
        else:
            i = lineno
            print()
            print("Difference in line %d:" % (i + 1))
            print("Command: %s(%s)" % (commands[i][0],
                                       ", ".join(str(t) for t in commands[i][1:])))
            print("Original: %s" % lines_original[i])
            print("Computed: %s" % lines_fresh[i])
            print()




class MojoUnstableError(Exception):
    pass


class MojoNotFoundError(Exception):
    pass
