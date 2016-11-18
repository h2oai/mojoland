#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
from typing import Iterator, List, Tuple
from h2o.estimators import H2OEstimator
import mojoland


class BaseRecipe:
    """
    Base class for all mojo recipes.

    Each recipe must adhere to the following naming convention:
    `{Dataset}{Algo}Recipe`. For example, `IrisGbmRecipe` or `StarsDrfRecipe`.
    Whenever we want to follow a culinary metaphor, we will be saying that the
    "Dataset" part of the name is the "dish name", and "algo" is the "flavor".

    A recipe has two responsibilities: first is to produce a trained h2o model
    ("baking" the recipe), and second is to take a `MojoModel` corresponding
    to this recipe and produce artifacts of this model that must be stable
    over time.
    """

    def bake(self) -> H2OEstimator:
        """Train and return a new H2O model corresponding to this recipe."""
        raise NotImplemented


    def nibbles(self, mojo: "mojoland.MojoModel" = None) -> Iterator[Tuple[str, "mojoland.Commands"]]:
        yield ("parameters", mojo.simple_params_nibble())
        yield ("multiparams", mojo.multi_params_nibble())
        yield ("scores0", mojo.scores0(self.source()))
        yield ("scores1", mojo.scores1(self.source()))
        yield ("scores2", mojo.scores2())


    def source(self) -> Iterator[List[str]]:
        raise NotImplemented
