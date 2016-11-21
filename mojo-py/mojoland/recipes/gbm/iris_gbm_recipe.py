#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
from typing import Iterator, List

from h2o.estimators import H2OGradientBoostingEstimator

from ..datasets import iris_frame, iris_data
from ..baserecipe import BaseRecipe


class IrisGbmRecipe(BaseRecipe):
    """Multinomial classification (3 classes), features are numeric (4 factors)."""

    def bake(self) -> H2OGradientBoostingEstimator:
        fr = iris_frame()
        model = H2OGradientBoostingEstimator(ntrees=20, distribution="multinomial")
        model.train(y="Species", training_frame=fr)
        return model

    def source(self) -> Iterator[List[str]]:
        return iris_data()
