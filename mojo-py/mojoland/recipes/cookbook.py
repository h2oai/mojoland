#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
from typing import Iterator, Tuple

import mojoland

Commands = Iterator[Tuple[str, ...]]


def v0_simple_params() -> Commands:
    yield ("isSupervised", )
    yield ("nfeatures", )
    yield ("nclasses", )
    yield ("getModelCategory", )
    yield ("getUUID", )
    yield ("getHeader", )
    yield ("getModelCategories", )
    yield ("getNumCols", )
    yield ("getResponseName", )
    yield ("getResponseIdx", )
    yield ("getNumResponseClasses", )
    yield ("isClassifier", )
    yield ("isAutoEncoder", )
    yield ("getDomainValues~", )
    yield ("getPredsSize~", )
    yield ("getNames", )


def v0_multi_params(mojo: "mojoland.MojoModel") -> Commands:
    for mc in model_categories:
        yield ("getPredsSize~m", mc)
    for i in range(-1, mojo.nfeatures + 2):
        yield ("getNumClasses", i)
        yield ("getDomainValues~i", i)
    for n in mojo.colnames + ["foo", "", "null"]:
        yield ("getDomainValues~s", n)
        yield ("getColIdx", n)
    for i, domain in enumerate(mojo.domains):
        if domain is not None:
            for d in domain + ["oof", "", "~@~!~#~$~", "None"]:
                yield ("mapEnum", i, d)


#-----------------------------------------------------------------------------------------------------------------------
# Constants
#-----------------------------------------------------------------------------------------------------------------------

model_categories = ["Multinomial", "Binomial", "Regression", "Clustering", "AutoEncoder", "DimReduction"]
