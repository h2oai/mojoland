#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
import shutil
import sys

import h2o
from mojoland import IrisGbmRecipe

assert sys.version_info[0] == 3, "Python3 is expected"
h2o.init()

igr = IrisGbmRecipe()
shutil.rmtree(igr._mojo_dirname())
igr.make()
