#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
from typing import Iterator, List
from h2o.estimators import H2OGeneralizedLinearEstimator

from ..datasets import cars_frame, cars_data
from ..baserecipe import BaseRecipe


class CarsGlmRecipe(BaseRecipe):

    def bake(self) -> H2OGeneralizedLinearEstimator:
        fr = cars_frame()
        model = H2OGeneralizedLinearEstimator()
        model.train(y="mpg", training_frame=fr, ignored_columns=["name"])
        return model


    def source(self) -> Iterator[List[str]]:
        return cars_data()
