#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
from typing import Iterator, List

from h2o.estimators import H2OXGBoostEstimator

from mojoland.recipes.datasets import eyestate_frame, eyestate_data
from mojoland.recipes.baserecipe import BaseRecipe


class EyestatetreeXgboostRecipe(BaseRecipe):
    """Binomial model, all features are numeric."""

    def bake(self) -> H2OXGBoostEstimator:
        fr = eyestate_frame()
        model = H2OXGBoostEstimator(ntrees=100, distribution="bernoulli", booster="gbtree")
        model.train(y="eyeDetection", training_frame=fr)
        return model


    def source(self) -> Iterator[List[str]]:
        return eyestate_data()
