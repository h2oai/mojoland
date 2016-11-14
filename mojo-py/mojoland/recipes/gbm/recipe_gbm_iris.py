#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from h2o.estimators import H2OGradientBoostingEstimator

from ..datasets import iris_frame, iris_data
from ..baserecipe import MojoRecipe


class IrisGbmRecipe(MojoRecipe):

    def _train_model_impl(self):
        fr = iris_frame()
        model = H2OGradientBoostingEstimator(n_trees=20)
        model.train(y="Species", training_frame=fr)
        return model


    def _generate_artifacts(self):
        yield ("scores", self._score_artifact())


    def _score_artifact(self):
        return [("score0~dada", {"arg1": "[%s]" % ",".join(row), "arg2": "[0,0,0,0,0]"})
                for row in iris_data()]
