#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
Primary script for running the mojo stability test harness.

Running this script will go through all the recipes, and then for each recipe
either create the latest mojo model if it doesn't exist yet, or load the model
from the saved mojo file. Then it will proceed to testing all "nibbles" of the
model against the saved results if they exist, and if they don't they will be
created and saved too.
"""
import sys
import mojoland
assert sys.version_info[0] == 3, "Python 3 is required"

if __name__ == "__main__":
    cnsr = mojoland.Connoisseur()
    for recipe in mojoland.list_recipes():
        cnsr.degustate(recipe)
