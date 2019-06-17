#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
from typing import Iterator, List

from h2o.estimators import H2OXGBoostEstimator

from ..datasets import cars_frame, cars_data
from ..baserecipe import BaseRecipe


class CarsdartXgboostRecipe(BaseRecipe):
    """Regression model, all features are numeric."""

    def bake(self) -> H2OXGBoostEstimator:
        fr = cars_frame()
        fr = fr[fr["mpg"].isna() == 0]
        model = H2OXGBoostEstimator(ntrees=50, booster="dart")
        model.train(y="mpg", training_frame=fr, ignored_columns=["name"])
        return model

    def source(self) -> Iterator[List[str]]:
        return cars_data()
