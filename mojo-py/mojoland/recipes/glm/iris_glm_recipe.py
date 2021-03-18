#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
from typing import Iterator, List
from h2o.estimators import H2OGeneralizedLinearEstimator

from ..datasets import iris_frame, iris_data
from ..baserecipe import BaseRecipe


class IrisGlmRecipe(BaseRecipe):
    """Multinomial classification (3 classes), features are numeric (4 factors)."""

    def bake(self) -> H2OGeneralizedLinearEstimator:
        fr = iris_frame()
        model = H2OGeneralizedLinearEstimator()
        model.train(y="Species", training_frame=fr)
        return model

    def source(self) -> Iterator[List[str]]:
        return iris_data()
