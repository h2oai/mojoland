#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
import sys
import mojoland
assert sys.version_info[0] == 3, "Python3 is required"

if __name__ == "__main__":
    cnsr = mojoland.Connoisseur()
    for recipe in mojoland.list_recipes():
        cnsr.degustate(recipe)
