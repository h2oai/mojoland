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
import argparse
import sys
assert sys.version_info[0] == 3, "Python 3 is required"

if __name__ == "__main__":
    import mojoland
    parser = argparse.ArgumentParser(description="Taste all mojo recipes.")
    parser.add_argument("--creative", help="Enabling baking new mojos / nibbles.", action="store_true")
    args = parser.parse_args()

    connoisseur = mojoland.Connoisseur()
    connoisseur.can_bake = args.creative

    for recipe in mojoland.list_recipes():
        connoisseur.degustate(recipe)
