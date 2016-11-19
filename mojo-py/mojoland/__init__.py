#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from .backend import MojoServer
from .mojo_model import MojoModel
from .recipes.baserecipe import BaseRecipe
from .recipes.connoisseur import Connoisseur, MojoUnstableError

__all__ = ("BaseRecipe", "Connoisseur", "MojoServer", "MojoModel", "MojoUnstableError")



def list_recipes():
    import mojoland.recipes
    return [getattr(mojoland.recipes, c)
            for c in dir(mojoland.recipes)
            if c.endswith("Recipe") and c != "BaseRecipe"]
