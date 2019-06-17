#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
from typing import Iterator, List

from h2o.estimators import H2OXGBoostEstimator

from mojoland.recipes.datasets import missing_frame, missing_data
from mojoland.recipes.baserecipe import BaseRecipe


class MissinglinearXgboostRecipe(BaseRecipe):
    """Artificial dataset with missing values."""

    def bake(self) -> H2OXGBoostEstimator:
        fr = missing_frame()
        model = H2OXGBoostEstimator(ntrees=50, distribution="gaussian", booster="gblinear")
        model.train(training_frame=fr)
        return model

    def source(self) -> Iterator[List[str]]:
        return missing_data()
