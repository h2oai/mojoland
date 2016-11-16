#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
import shutil
import sys

from .recipes import IrisGbmRecipe

assert sys.version_info[0] == 3, "Python3 is expected"

igr = IrisGbmRecipe()
shutil.rmtree(igr._mojo_dirname())
igr.make()
