#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
from typing import Iterator, List

from h2o.estimators import H2ORandomForestEstimator

from ..datasets import eyestate_frame, eyestate_data
from ..baserecipe import BaseRecipe


class EyestateDrfRecipe(BaseRecipe):
    """Binomial model, all features are numeric."""

    def bake(self) -> H2ORandomForestEstimator:
        fr = eyestate_frame()
        model = H2ORandomForestEstimator(ntrees=100)
        model.train(y="eyeDetection", training_frame=fr)
        return model


    def source(self) -> Iterator[List[str]]:
        return eyestate_data()
