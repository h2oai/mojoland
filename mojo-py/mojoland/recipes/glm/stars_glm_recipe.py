#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
from typing import Iterator, List
from h2o.estimators import H2OGeneralizedLinearEstimator

from ..datasets import stars_frame, stars_data
from ..baserecipe import BaseRecipe


class StarsGlmRecipe(BaseRecipe):
    """Regression model, some input columns are ignored."""

    def bake(self) -> H2OGeneralizedLinearEstimator:
        fr = stars_frame()
        assert fr.type("distance") == "int"
        model = H2OGeneralizedLinearEstimator()
        model.train(y="distance", training_frame=fr, ignored_columns=["name1", "name2"])
        return model


    def source(self) -> Iterator[List[str]]:
        return stars_data()
