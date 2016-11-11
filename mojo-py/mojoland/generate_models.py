#!/usr/bin/env python3

import sys

import h2o

assert sys.version_info[0] == 3, "Python3 is expected"

h2o.connect()
models_info = h2o.api("GET /4/modelsinfo")["models"]
models_with_mojo = [mi["algo"] for mi in models_info if mi["have_mojo"]]
print(models_with_mojo)
