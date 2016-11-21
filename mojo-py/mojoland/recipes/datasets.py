#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
import csv
import os
from typing import Iterator, List

import h2o

__all__ = ("iris_frame", "iris_data",
           "stars_frame", "stars_data",
           "names_frame", "names_data",
           "eyestate_frame", "eyestate_data",
           "cars_frame", "cars_data",
           "missing_frame", "missing_data",
           "titanic_frame", "titanic_data",
           )


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


#---- Eyestate ---------------------------------------------------------------------------------------------------------

def eyestate_frame() -> h2o.H2OFrame:
    frame = h2o.upload_file(_file("eyestate.csv"), col_types={"eyeDetection": "enum"})
    assert frame.shape == (14980, 15)
    assert frame.names == ["AF3", "F7", "F3", "FC5", "T7", "P7", "O1", "O2", "P8", "T8", "FC6", "F4", "F8", "AF4",
                           "eyeDetection"]
    assert frame["eyeDetection"].nlevels() == [2]
    return frame


def eyestate_data() -> Iterator[List[str]]:
    """Iterator over the data; first row is the header."""
    with open(_file("eyestate.csv"), "r") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for lineno, line in enumerate(reader):
            if lineno % 7 == 0:  # return roughly 2100 entries for testing (including the header)
                yield line


#---- Cars -------------------------------------------------------------------------------------------------------------

def cars_frame() -> h2o.H2OFrame:
    frame = h2o.upload_file(_file("cars.csv"))
    assert frame.shape == (406, 8)
    assert frame.names == ["name", "mpg", "cylinders", "displacement", "power", "weight", "acceleration", "year"]
    return frame


def cars_data() -> Iterator[List[str]]:
    """Iterator over the data; first row is the header."""
    with open(_file("cars.csv"), "r") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        yield from reader


#---- Cars -------------------------------------------------------------------------------------------------------------

def missing_frame() -> h2o.H2OFrame:
    frame = h2o.upload_file(_file("missing.csv"))
    assert frame.shape == (40, 3)
    assert frame.names == ["xCat", "xNum", "response"]
    return frame


def missing_data() -> Iterator[List[str]]:
    """Iterator over the data; first row is the header."""
    with open(_file("missing.csv"), "r") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        yield from reader


#---- Titanic ----------------------------------------------------------------------------------------------------------

def titanic_frame() -> h2o.H2OFrame:
    frame = h2o.upload_file(_file("titanic.csv"), col_types={"pclass": "enum", "survived": "enum", "ticket": "string",
                                                             "boat": "enum"})
    assert frame.shape == (1309, 14)
    assert frame.names == ["pclass", "survived", "name", "sex", "age", "sibsp", "parch", "ticket", "fare", "cabin",
                           "embarked", "boat", "body", "home.dest"]
    return frame


def titanic_data() -> Iterator[List[str]]:
    """Iterator over the data; first row is the header."""
    with open(_file("titanic.csv"), "r") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        yield from reader


#-----------------------------------------------------------------------------------------------------------------------

def _file(filename):
    curdir = os.path.dirname(__file__)
    mojodatadir = os.path.abspath(os.path.join(curdir, "..", "..", "..", "mojo-data", "datasets"))
    fullname = os.path.abspath(os.path.join(mojodatadir, filename))
    assert os.path.exists(fullname), "Cannot find dataset %s" % fullname
    return fullname
