#!/usr/bin/env python3
import os
import re

import h2o
from h2o.estimators import H2OEstimator


class MojoRecipe(object):
    """
    """

    def __init__(self):
        self.model = None

    def make(self):
        # 1. Build the model
        assert not self.is_model_built()
        self.model = self._train_model_impl()
        assert isinstance(self.model, H2OEstimator)

        # 2. Save the mojo
        mojofile = self.model.download_mojo(path=self._mojo_dirname())
        newname = os.path.join(self._mojo_dirname(), self._mojo_filename())
        os.rename(mojofile, newname)

        # 3. Save model's artifacts



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

    def _mojo_dirname(self):
        algo, version, dataset = self._name_parts()
        return os.path.join("mojos", algo, version, dataset)

    def _name_parts(self):
        classname = self.__class__.__name__
        parts = [t for t in re.split("([A-Z][a-z]*)", classname) if t]  # split into camel-cased parts
        assert len(parts) == 3 and parts[2] == "Recipe", "Unexpected class name: %s" % classname
        dataset = parts[0].lower()
        algo = parts[1].lower()
        version = "v%s" % self._get_mojo_version(algo)
        return (algo, version, dataset)

    @staticmethod
    def _get_mojo_version(algo):
        if not MojoRecipe._mojo_versions:
            models_info = h2o.api("GET /4/modelsinfo")["models"]
            MojoRecipe._mojo_versions = {mi["algo"]: mi["mojo_version"] for mi in models_info if mi["have_mojo"]}
        return MojoRecipe._mojo_versions[algo]



assert os.path.abspath(os.curdir).endswith("src"), "Unexpected current directory: %s" % os.path.abspath(os.curdir)
