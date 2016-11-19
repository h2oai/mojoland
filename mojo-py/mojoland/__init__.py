#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from .backend import MojoServer
from .mojo_model import MojoModel
from .recipes.baserecipe import BaseRecipe

__all__ = ("BaseRecipe", "MojoServer", "MojoModel", "MojoUnstableError")


class MojoUnstableError(Exception):
    pass


def list_recipes():
    import mojoland.recipes
    return [getattr(mojoland.recipes, c)
            for c in dir(mojoland.recipes)
            if c.endswith("Recipe") and c != "BaseRecipe"]
