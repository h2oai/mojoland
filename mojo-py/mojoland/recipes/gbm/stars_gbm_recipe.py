#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from h2o.estimators import H2OGradientBoostingEstimator

from ..cookbook import v0_simple_params
from ..datasets import stars_frame, stars_data
from ..baserecipe import BaseRecipe


class StarsGbmRecipe(BaseRecipe):

    def bake(self):
        fr = stars_frame()
        assert fr.type("distance") == "int"
        model = H2OGradientBoostingEstimator(ntrees=100)
        model.train(y="distance", training_frame=fr, ignored_columns=["name1", "name2"])
        return model


    def nibbles(self):
        yield ("parameters", v0_simple_params)
        # yield ("scores_a", self._scores_a)
        # yield ("scores_b", self._scores_b)
        # yield ("scores_c", self._scores_c)
        yield ("multiparams", self._multiparams)


    def _scores_a(self):
        for row in stars_data():
            yield ("score0~dada", "[%s]" % ",".join(row[:-1]), "[0,0,0,0,0,0,0,0,0]")


    def _scores_b(self):
        yield ("score0~dada", "[NaN,0,0,0,0]", "[0,0,0,0,0]")
        yield ("score0~dada", "[1,NaN,0,0,0]", "[0,0,0,0,0]")
        yield ("score0~dada", "[1,2,NaN,0,0]", "[0,0,0,0,0]")
        yield ("score0~dada", "[1,2,3,NaN,0]", "[0,0,0,0,0]")
        yield ("score0~dada", "[1,2,3,10,NaN]", "[0,0,0,0,0]")
        yield ("score0~dada", "[1e6,2e7,3e8,10e10,1e308]", "[0,0,0,0,0]")
        yield ("score0~dada", "[NaN,NaN,NaN,NaN,NaN]", "[0,0,0,0,0]")
        yield ("score0~dada", "[-1,-2,0,-3,-10]", "[0,0,0,0,0]")
        yield ("score0~dada", "[0,0,0,0,0]", "[0,0,0,0,0]")
        yield ("score0~dada", "[2.2250738585072012e-308,2e-308,3e-308,1e-308,2e-309]", "[0,0,0,0,0]")
        yield ("score0~dada", "[1, 2, 3, 4, 5, 6, 7]", "[0,0,0,0,0]")
        yield ("score0~dada", "[1, 2, 3]", "[0,0,0,0,0]")
        yield ("score0~dada", "[1, 2, 3, 4, 5]", "[0,0,0]")


    def _scores_c(self):
        i = 0
        for _, arg1, arg2 in self._scores_a():
            i += 1
            yield ("score0~dadda", arg1, i * 0.1, arg2)


    def _multiparams(self):
        for mc in ["Multinomial", "Binomial", "Regression", "Clustering", "AutoEncoder", "DimReduction"]:
            yield ("getPredsSize~m", mc)
        for i in range(-1, 12):
            yield ("getNumClasses", i)
            yield ("getDomainValues~i", i)
        for n in ["Sepal.Length", "Sepal.Width", "Petal.Length", "Petal.Width", "Species", "foo", ""]:
            yield ("getDomainValues~s", n)
            yield ("getColIdx", n)
        for e in ["Iris-setosa", "Iris-versicolor", "Iris-virginica", "None", "Iris-mixed", ""]:
            yield ("mapEnum", 4, e)
