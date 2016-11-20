#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
import csv
import os
from typing import Iterator, List

import h2o

__all__ = ("iris_frame", "iris_data", "stars_frame", "stars_data", "names_frame", "names_data")


#---- Iris -------------------------------------------------------------------------------------------------------------

def iris_frame() -> h2o.H2OFrame:
    frame = h2o.upload_file(_file("iris.csv"))
    assert frame.names == ["Sepal.Length", "Sepal.Width", "Petal.Length", "Petal.Width", "Species"]
    return frame


def iris_data() -> Iterator[List[str]]:
    """Iterator over the data; first row is the header."""
    with open(_file("iris.csv"), "r") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        yield from reader


#---- Stars ------------------------------------------------------------------------------------------------------------

def stars_frame() -> h2o.H2OFrame:
    frame = h2o.upload_file(_file("stars.csv"), col_types={"name2": "string"})
    assert frame.shape == (300, 12)
    assert frame.names == ["name1", "name2", "coordL", "coordB", "spectral_type", "vis_mag", "vmc", "abs_mag", "amc",
                           "prllx", "error", "distance"]
    assert frame["spectral_type"].nlevels() == [175]
    assert frame.type("name1") == "string" and frame.type("name2") == "string"
    return frame


def stars_data() -> Iterator[List[str]]:
    """Iterator over the data; first row is the header."""
    with open(_file("stars.csv"), "r") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        yield from reader


#---- Names ------------------------------------------------------------------------------------------------------------

def names_frame() -> h2o.H2OFrame:
    frame = h2o.upload_file(_file("names.csv"))
    assert frame.shape == (51176, 4)
    assert frame.names == ["name", "sex", "year", "count"]
    assert frame.type("name") == "enum"
    assert frame.type("sex") == "enum"
    assert frame.nlevels() == [1575, 2, 0, 0]
    return frame


def names_data() -> Iterator[List[str]]:
    """Iterator over the data; first row is the header."""
    with open(_file("names.csv"), "r") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for lineno, line in enumerate(reader):
            if lineno % 20 == 0:  # return roughly 2500 entries for testing (including the header)
                yield line



def _file(filename):
    curdir = os.path.dirname(__file__)
    mojodatadir = os.path.abspath(os.path.join(curdir, "..", "..", "..", "mojo-data", "datasets"))
    fullname = os.path.abspath(os.path.join(mojodatadir, filename))
    assert os.path.exists(fullname), "Cannot find dataset %s" % fullname
    return fullname
