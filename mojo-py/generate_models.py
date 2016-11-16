#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
import os
import shutil
import sys

import h2o
from mojoland import IrisGbmRecipe

assert sys.version_info[0] == 3, "Python3 is expected"
h2o.init()

igr = IrisGbmRecipe()
dirname = igr._mojo_dirname()
if os.path.exists(dirname):
    shutil.rmtree(dirname)
igr.make()
