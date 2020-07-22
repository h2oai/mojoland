#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from .iris_deeplearning_recipe import IrisDeeplearningRecipe
from .stars_deeplearning_recipe import StarsDeeplearningRecipe
from .names_deeplearning_recipe import NamesDeeplearningRecipe
from .eyestate_deeplearning_recipe import EyestateDeeplearningRecipe
from .cars_deeplearning_recipe import CarsDeeplearningRecipe
from .missing_deeplearning_recipe import MissingDeeplearningRecipe
from .titanic_deeplearning_recipe import TitanicDeeplearningRecipe

__all__ = (
    "IrisDeeplearningRecipe", "StarsDeeplearningRecipe", "NamesDeeplearningRecipe", "EyestateDeeplearningRecipe",
    "CarsDeeplearningRecipe", "MissingDeeplearningRecipe", "TitanicDeeplearningRecipe")
