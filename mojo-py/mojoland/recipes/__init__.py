#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from .drf import *
from .gbm import *
from .baserecipe import BaseRecipe

__all__ = tuple(name for name in dir() if name.endswith("Recipe"))

for name in dir():
    if name.endswith("Recipe"):
        locals()[name].__module__ = "mojoland.recipes"
