#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
import os
import re
from typing import Optional

import h2o
from h2o.estimators import H2OEstimator
from mojoland.backend import MojoServer


class MojoRecipe(object):
    """
    """

    def __init__(self):
        self.model = None     # type: Optional[H2OEstimator]
        self.model_id = None  # type: Optional[str]


    def make(self):
        server = MojoServer.get()

        # 1. Build the model
        assert not self.is_model_built()
        self.model = self._train_model_impl()
        assert isinstance(self.model, H2OEstimator)

        # 2. Save the mojo to file and load in MojoServer
        mojofile = self.model.download_mojo(path=self._mojo_dirname())
        newname = self._mojo_fullname()
        os.rename(mojofile, newname)
        self.model_id = server.load_model(newname)

        # 3. Save model's artifacts
        for artifact_name, commands in self._generate_artifacts():
            artfile = self._artifact_fullname(artifact_name)
            with open(artfile, "w") as out:
                for method, params in commands:
                    res = server.invoke_method(self.model_id, method, params)
                    out.write(res + "\n")



    def is_model_built(self):
        """Return True if the model described by this recipe has already been built."""
        filename = os.path.join(self._mojo_dirname(), self._mojo_filename())
        return os.path.exists(filename)


    #-------------------------------------------------------------------------------------------------------------------
    #  Protected
    #-------------------------------------------------------------------------------------------------------------------

    def _train_model_impl(self):
        raise NotImplemented


    def _generate_artifacts(self):
        raise NotImplemented


    #-------------------------------------------------------------------------------------------------------------------
    #  Private
    #-------------------------------------------------------------------------------------------------------------------

    def _mojo_filename(self):
        algo, version, dataset = self._name_parts()
        return "%s_%s_%s.mojo" % (algo, version, dataset)


    def _artifact_filename(self, aname):
        algo, version, dataset = self._name_parts()
        return "%s_%s_%s_%s.mojo" % (algo, version, dataset, aname)


    def _mojo_dirname(self):
        curdir = os.path.dirname(__file__)
        assert curdir.endswith("recipes"), "Unexpected current directory: %s" % curdir
        targetdir = os.path.abspath(os.path.join(curdir, "..", "..", "..", "mojo-data", "mojos"))
        assert os.path.isdir(targetdir), "Directory %s cannot be found (%s)" % (targetdir, __file__)
        algo, version, dataset = self._name_parts()
        return os.path.join(targetdir, algo, version, dataset)


    def _mojo_fullname(self):
        return os.path.join(self._mojo_dirname(), self._mojo_filename())


    def _artifact_fullname(self, aname):
        return os.path.join(self._mojo_dirname(), self._artifact_filename(aname))


    def _name_parts(self):
        """
        Retrieve the recipe's name parts, based on class naming convention.

        The class name should follow the pattern {Dataset}{Algo}Recipe, for
        example "IrisGbmRecipe" or "Airlines1DrfRecipe". This also returns the
        latest mojo version of the algo (which is retrieved from the server).

        @returns: tuple (algo, mojo_version, dataset)
        """
        classname = self.__class__.__name__
        parts = [t for t in re.split("([A-Z][a-z0-9]*)", classname) if t]  # split into camel-cased parts
        assert len(parts) == 3 and parts[2] == "Recipe", "Unexpected class name: %s" % classname
        dataset = parts[0].lower()
        algo = parts[1].lower()
        version = "v%s" % self._get_mojo_version(algo)
        return algo, version, dataset


    @staticmethod
    def _get_mojo_version(algo):
        """Return the current mojo version corresponding to algorithm `algo`."""
        if not hasattr(MojoRecipe, "_mojo_versions"):
            models_info = h2o.api("GET /4/modelsinfo")["models"]
            MojoRecipe._mojo_versions = {mi["algo"]: mi["mojo_version"] for mi in models_info if mi["have_mojo"]}
        return MojoRecipe._mojo_versions[algo]

