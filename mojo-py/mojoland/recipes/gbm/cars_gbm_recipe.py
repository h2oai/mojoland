#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
from typing import Iterator, List

from h2o.estimators import H2OGradientBoostingEstimator

from ..datasets import cars_frame, cars_data
from ..baserecipe import BaseRecipe


class CarsGbmRecipe(BaseRecipe):
    """Regression model (laplace distribution), all features are numeric."""

    def bake(self) -> H2OGradientBoostingEstimator:
        fr = cars_frame()
        model = H2OGradientBoostingEstimator(ntrees=50, distribution="laplace")
        model.train(y="mpg", training_frame=fr, ignored_columns=["name"])
        return model


    def source(self) -> Iterator[List[str]]:
        return cars_data()
