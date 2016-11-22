#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from .iris_drf_recipe import IrisDrfRecipe
from .stars_drf_recipe import StarsDrfRecipe
from .names_drf_recipe import NamesDrfRecipe
from .eyestate_drf_recipe import EyestateDrfRecipe
from .cars_drf_recipe import CarsDrfRecipe
from .missing_drf_recipe import MissingDrfRecipe
from .titanic_drf_recipe import TitanicDrfRecipe

__all__ = ("IrisDrfRecipe", "StarsDrfRecipe", "NamesDrfRecipe", "EyestateDrfRecipe", "CarsDrfRecipe",
           "MissingDrfRecipe", "TitanicDrfRecipe")
