#!/usr/bin/env python3
import csv
import os
import h2o

__all__ = ("iris_frame", "iris_data")


def iris_frame():
    frame = h2o.upload_file(_file("iris.csv"))
    assert frame.names == ["Sepal.Length", "Sepal.Width", "Petal.Length",
                           "Petal.Width", "Species"]
    return frame


def iris_data():
    with open(_file("iris.csv"), "r") as csvfile:
        next(csvfile)  # skip the header
        reader = csv.reader(csvfile, delimiter=",")
        yield from reader



def _file(filename):
    curdir = os.path.dirname(__file__)
    mojodatadir = os.path.abspath(os.path.join(curdir, "..", "..", "..", "mojo-data", "datasets"))
    fullname = os.path.abspath(os.path.join(mojodatadir, filename))
    assert os.path.exists(fullname), "Cannot find dataset %s" % fullname
    return fullname
