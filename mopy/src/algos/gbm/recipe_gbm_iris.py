#!/usr/bin/env python3

from h2o.estimators import H2OGradientBoostingEstimator
from ..baserecipe import MojoRecipe
from ..datasets import iris


class IrisGbmRecipe(MojoRecipe):

    def _train_model_impl(self):
        fr = iris()
        model = H2OGradientBoostingEstimator(n_trees=20)
        model.train(y="Species", training_frame=fr)
        return model
