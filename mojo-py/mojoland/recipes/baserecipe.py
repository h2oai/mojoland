#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
from typing import Generator, List, Tuple
from h2o.estimators import H2OEstimator
from mojoland import MojoModel


class BaseRecipe(object):

    def bake(self) -> H2OEstimator:
        raise NotImplemented


    def nibbles(self, mojo: MojoModel = None) -> List[Tuple[str, Generator[Tuple[str, ...], None, None]]]:
        raise NotImplemented

