#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
import csv
import os
from typing import Iterator, List

import h2o

__all__ = ("iris_frame", "iris_data", "stars_frame", "stars_data")


#---- Iris -------------------------------------------------------------------------------------------------------------

def iris_frame() -> h2o.H2OFrame:
    frame = h2o.upload_file(_file("iris.csv"))
    assert frame.names == ["Sepal.Length", "Sepal.Width", "Petal.Length", "Petal.Width", "Species"]
    return frame


def iris_data() -> Iterator[List[str]]:
    with open(_file("iris.csv"), "r") as csvfile:
        next(csvfile)  # skip the header
        reader = csv.reader(csvfile, delimiter=",")
        yield from reader


#---- Stars ------------------------------------------------------------------------------------------------------------

def stars_frame() -> h2o.H2OFrame:
    frame = h2o.upload_file(_file("stars.csv"), col_types={"name2": "string"})
    assert frame.shape == (300, 12)
    assert frame.names == ["name1", "name2", "coordL", "coordB", "spectral_type", "vis_mag", "vmc", "abs_mag", "amc",
                           "prllx", "error", "distance"]
    assert frame["spectral_type"].nlevels() == 175
    assert frame.type("name1") == "string" and frame.type("name2") == "string"
    return frame


def stars_data() -> Iterator[List[str]]:
    with open(_file("stars.csv"), "r") as csvfile:
        next(csvfile)  # skip the header
        reader = csv.reader(csvfile, delimiter=",")
        yield from reader



def _file(filename):
    curdir = os.path.dirname(__file__)
    mojodatadir = os.path.abspath(os.path.join(curdir, "..", "..", "..", "mojo-data", "datasets"))
    fullname = os.path.abspath(os.path.join(mojodatadir, filename))
    assert os.path.exists(fullname), "Cannot find dataset %s" % fullname
    return fullname
