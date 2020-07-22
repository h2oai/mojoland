#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
from typing import Iterator, List
from h2o.estimators import H2ODeepLearningEstimator

from ..datasets import eyestate_frame, eyestate_data
from ..baserecipe import BaseRecipe


class EyestateDeeplearningRecipe(BaseRecipe):
    """Binomial model, all features are numeric."""

    def bake(self) -> H2ODeepLearningEstimator:
        fr = eyestate_frame()
        model = H2ODeepLearningEstimator(epochs=100, reproducible=True)
        model.train(y="eyeDetection", training_frame=fr)
        return model


    def source(self) -> Iterator[List[str]]:
        return eyestate_data()
