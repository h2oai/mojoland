#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
from typing import Iterator, List
from h2o.estimators import H2ORuleFitEstimator

from ..datasets import iris_frame, iris_data
from ..baserecipe import BaseRecipe


class IrisRulefitRecipe(BaseRecipe):
    """Multinomial classification (3 classes), features are numeric (4 factors)."""

    def bake(self) -> H2ORuleFitEstimator:
        fr = iris_frame()
        model = H2ORuleFitEstimator(min_rule_length=3, max_rule_length=7, max_num_rules=50)
        model.train(y="Species", training_frame=fr)
        return model

    def source(self) -> Iterator[List[str]]:
        return iris_data()
