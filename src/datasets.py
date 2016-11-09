#!/usr/bin/env python3
import os
import h2o

__all = ("iris", )


def iris():
    frame = h2o.upload_file(_file("iris.csv"))
    assert frame.names == ["Sepal.Length", "Sepal.Width", "Petal.Length",
                           "Petal.Width", "Species"]
    return frame


def _file(filename):
    fullname = os.path.abspath(os.path.join("..", "datasets", filename))
    assert os.path.exists(fullname), "Cannot find dataset %s" % fullname
    return fullname
