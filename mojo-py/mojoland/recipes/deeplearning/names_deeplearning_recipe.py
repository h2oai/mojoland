#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
from typing import Iterator, List
from h2o.estimators import H2ODeepLearningEstimator

from ..datasets import names_frame, names_data
from ..baserecipe import BaseRecipe


class NamesDeeplearningRecipe(BaseRecipe):
    """Binomial classification with a categorical levels with 1575 factors."""

    def bake(self) -> H2ODeepLearningEstimator:
        fr = names_frame()
        fr = fr[:5000, :]
        fr["name"] = fr["name"].ascharacter().asfactor()  # trim nlevels()
        assert 256 < fr["name"].nlevels()[0] < 500
        model = H2ODeepLearningEstimator(epochs=100, reproducible=True)
        model.train(y="sex", training_frame=fr)
        return model

    def source(self) -> Iterator[List[str]]:
        return names_data()
