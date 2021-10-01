#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
from typing import Iterator, List
from h2o.estimators import H2ORuleFitEstimator

from ..datasets import stars_frame, stars_data
from ..baserecipe import BaseRecipe


class StarsRulefitRecipe(BaseRecipe):
    """Regression model, some input columns are ignored."""

    def bake(self) -> H2ORuleFitEstimator:
        fr = stars_frame()
        assert fr.type("distance") == "int"
        model = H2ORuleFitEstimator(min_rule_length=3, max_rule_length=7, max_num_rules=50)
        model.train(y="distance", training_frame=fr, ignored_columns=["name1", "name2"])
        return model


    def source(self) -> Iterator[List[str]]:
        return stars_data()
