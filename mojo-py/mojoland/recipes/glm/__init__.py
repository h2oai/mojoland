#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from .iris_glm_recipe import IrisGlmRecipe
from .stars_glm_recipe import StarsGlmRecipe
from .names_glm_recipe import NamesGlmRecipe
from .eyestate_glm_recipe import EyestateGlmRecipe
from .cars_glm_recipe import CarsGlmRecipe
from .missing_glm_recipe import MissingGlmRecipe
from .titanic_glm_recipe import TitanicGlmRecipe

__all__ = (
    "IrisGlmRecipe", "StarsGlmRecipe", "NamesGlmRecipe", "EyestateGlmRecipe",
    "CarsGlmRecipe", "MissingGlmRecipe", "TitanicGlmRecipe")
