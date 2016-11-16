#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from h2o.estimators import H2OGradientBoostingEstimator

from ..datasets import iris_frame, iris_data
from ..baserecipe import MojoRecipe


class IrisGbmRecipe(MojoRecipe):

    def _train_model_impl(self):
        fr = iris_frame()
        model = H2OGradientBoostingEstimator(ntrees=20)
        model.train(y="Species", training_frame=fr)
        return model


    def _generate_artifacts(self):
        yield ("scores_a", self._scores_a)
        yield ("scores_b", self._scores_b)
        yield ("scores_c", self._scores_c)
        yield ("parameters", self._parameters)
        yield ("multiparams", self._multiparams)


    def _scores_a(self):
        for row in iris_data():
            yield ("score0~dada", "[%s]" % ",".join(row[:-1]), "[0,0,0,0,0]")


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
        for _, arg1, arg2 in self._scores_a():
            yield ("score0~dadda", arg1, 0, arg2)


    def _parameters(self):
        yield ("isSupervised", )
        yield ("nfeatures", )
        yield ("nclasses", )
        yield ("getModelCategory", )
        yield ("getUUID", )
        yield ("getHeader", )
        yield ("getModelCategories", )
        yield ("getNumCols", )
        yield ("getResponseName", )
        yield ("getResponseIdx", )
        yield ("getNumResponseClasses", )
        yield ("isClassifier", )
        yield ("isAutoEncoder", )
        yield ("getDomainValues~", )
        yield ("getPredsSize~", )
        yield ("getNames", )


    def _multiparams(self):
        for mc in ["Multinomial", "Binomial", "Regression"]:
            yield ("getPredsSize~m", mc)
        for i in [0, 1, 2, 3, 4, 5, -1]:
            yield ("getNumClasses", i)
            yield ("getDomainValues~i", i)
        for n in ["Sepal.Length", "Sepal.Width", "Petal.Length", "Petal.Width", "Species", "foo", ""]:
            yield ("getDomainValues~s", n)
            yield ("getColIdx", n)
        for e in ["Iris-setosa", "Iris-versicolor", "Iris-virginica", "None", "Iris-mixed", ""]:
            yield ("mapEnum", 4, e)
