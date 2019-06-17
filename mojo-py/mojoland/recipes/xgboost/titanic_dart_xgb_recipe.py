#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
from typing import Iterator, List

from h2o.estimators import H2OXGBoostEstimator

from ..datasets import titanic_frame, titanic_data
from ..baserecipe import BaseRecipe


class TitanicdartXgboostRecipe(BaseRecipe):
    """Multinomial classification (8 classes), with mixed feature types."""

    def bake(self) -> H2OXGBoostEstimator:
        fr = titanic_frame()
        fr["parch"] = fr["parch"].asfactor()
        model = H2OXGBoostEstimator(ntrees=50, distribution="multinomial", booster="dart")
        model.train(y="parch", training_frame=fr, ignored_columns=["name", "ticket", "boat", "home.dest"])
        return model

    def source(self) -> Iterator[List[str]]:
        return titanic_data()
