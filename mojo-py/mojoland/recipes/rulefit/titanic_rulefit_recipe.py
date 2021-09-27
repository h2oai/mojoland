#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
from typing import Iterator, List
from h2o.estimators import H2ORuleFitEstimator

from ..datasets import titanic_frame, titanic_data
from ..baserecipe import BaseRecipe


class TitanicRulefitRecipe(BaseRecipe):
    """Multinomial classification (8 classes), with mixed feature types."""

    def bake(self) -> H2ORuleFitEstimator:
        fr = titanic_frame()
        fr["parch"] = fr["parch"].asfactor()
        model = H2ORuleFitEstimator(min_rule_length=3, max_rule_length=7, max_num_rules=50)
        model.train(y="parch", training_frame=fr, ignored_columns=["name", "ticket", "boat", "home.dest"])
        return model

    def source(self) -> Iterator[List[str]]:
        return titanic_data()
