#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
from typing import Iterator, List

from h2o.estimators import H2OXGBoostEstimator

from mojoland.recipes.datasets import iris_frame, iris_data
from mojoland.recipes.baserecipe import BaseRecipe


class IristreeXgboostRecipe(BaseRecipe):
    """Multinomial classification (3 classes), features are numeric (4 factors)."""

    def bake(self) -> H2OXGBoostEstimator:
        fr = iris_frame()
        model = H2OXGBoostEstimator(ntrees=20, distribution="multinomial", booster="gbtree")
        model.train(y="Species", training_frame=fr)
        return model

    def source(self) -> Iterator[List[str]]:
        return iris_data()
