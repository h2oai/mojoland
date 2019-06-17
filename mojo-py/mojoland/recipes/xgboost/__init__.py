#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from .cars_dart_xgb_recipe import CarsdartXgboostRecipe
from .cars_tree_xgb_recipe import CarstreeXgboostRecipe

from .eyestate_tree_xgb_recipe import EyestatetreeXgboostRecipe
from .eyestate_linear_xgb_recipe import EyestatelinearXgboostRecipe

from .iris_dart_xgb_recipe import IrisdartXgboostRecipe
from .iris_tree_xgb_recipe import IristreeXgboostRecipe

from .missing_tree_xgb_recipe import MissingtreeXgboostRecipe
from .missing_linear_xgb_recipe import MissinglinearXgboostRecipe

from .names_dart_xgb_recipe import NamesdartXgboostRecipe
from .names_tree_xgb_recipe import NamestreeXgboostRecipe

from .stars_tree_xgb_recipe import StarstreeXgboostRecipe
from .stars_linear_xgb_recipe import StarslinearXgboostRecipe

from .titanic_dart_xgb_recipe import TitanicdartXgboostRecipe
from .titanic_tree_xgb_recipe import TitanictreeXgboostRecipe
from .titanic_linear_xgb_recipe import TitaniclinearXgboostRecipe


__all__ = (
    "CarsdartXgboostRecipe", "CarstreeXgboostRecipe",
    "EyestatetreeXgboostRecipe", "EyestatelinearXgboostRecipe",
    "IrisdartXgboostRecipe", "IristreeXgboostRecipe",
    "MissingtreeXgboostRecipe",  "MissinglinearXgboostRecipe",
    "NamesdartXgboostRecipe", "NamestreeXgboostRecipe",
    "StarstreeXgboostRecipe", "StarslinearXgboostRecipe",
    "TitanicdartXgboostRecipe", "TitanictreeXgboostRecipe", "TitaniclinearXgboostRecipe"
)
