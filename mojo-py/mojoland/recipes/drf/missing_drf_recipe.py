#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
from typing import Iterator, List

from h2o.estimators import H2ORandomForestEstimator

from ..datasets import missing_frame, missing_data
from ..baserecipe import BaseRecipe


class MissingDrfRecipe(BaseRecipe):
    """Artificial dataset with missing values."""

    def bake(self) -> H2ORandomForestEstimator:
        fr = missing_frame()
        model = H2ORandomForestEstimator(ntrees=50)
        model.train(training_frame=fr)
        return model

    def source(self) -> Iterator[List[str]]:
        return missing_data()
