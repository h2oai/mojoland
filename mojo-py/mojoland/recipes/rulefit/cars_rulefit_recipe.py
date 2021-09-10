#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
from typing import Iterator, List
from h2o.estimators import H2ORuleFitEstimator

from ..datasets import cars_frame, cars_data
from ..baserecipe import BaseRecipe


class CarsRulefitRecipe(BaseRecipe):

    def bake(self) -> H2ORuleFitEstimator:
        fr = cars_frame()
        model = H2ORuleFitEstimator(min_rule_length=3, max_rule_length=7, max_num_rules=50)
        model.train(y="mpg", training_frame=fr, ignored_columns=["name"])
        return model


    def source(self) -> Iterator[List[str]]:
        return cars_data()
