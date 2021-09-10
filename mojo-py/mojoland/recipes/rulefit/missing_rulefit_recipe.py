#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
from typing import Iterator, List
from h2o.estimators import H2ORuleFitEstimator

from ..datasets import missing_frame, missing_data
from ..baserecipe import BaseRecipe


class MissingRulefitRecipe(BaseRecipe):
    """Artificial dataset with missing values."""

    def bake(self) -> H2ORuleFitEstimator:
        fr = missing_frame()
        model = H2ORuleFitEstimator(min_rule_length=3, max_rule_length=7, max_num_rules=50)
        model.train(training_frame=fr)
        return model

    def source(self) -> Iterator[List[str]]:
        return missing_data()
