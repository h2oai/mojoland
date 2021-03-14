#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from .iris_glm_recipe import IrisGLMRecipe
from .stars_glm_recipe import StarsGLMRecipe
from .names_glm_recipe import NamesGLMRecipe
from .eyestate_glm_recipe import EyestateGLMRecipe
from .cars_glm_recipe import CarsGLMRecipe
from .missing_glm_recipe import MissingGLMRecipe
from .titanic_glm_recipe import TitanicGLMRecipe

__all__ = (
    "IrisGLMRecipe", "StarsGLMRecipe", "NamesGLMRecipe", "EyestateGLMRecipe",
    "CarsGLMRecipe", "MissingGLMRecipe", "TitanicGLMRecipe")
