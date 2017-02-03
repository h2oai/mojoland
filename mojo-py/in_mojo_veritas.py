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
assert sys.version_info >= (3, 5), "Python 3.5+ is required"

if __name__ == "__main__":
    import mojoland
    parser = argparse.ArgumentParser(description="Taste all mojo recipes.")
    parser.add_argument("--creative", help="Enable baking new mojos / nibbles.", action="store_true")
    parser.add_argument("--recipe", help="Taste this specific recipe (if not given, all recipes will be tasted)")
    parser.add_argument("--backend", help="Which backend to use for testing: python / java", default="java",
                        choices=["java", "python"])
    args = parser.parse_args()

    connoisseur = mojoland.Connoisseur(backend=args.backend.lower())
    connoisseur.can_bake = args.creative

    recipes = mojoland.list_recipes()
    if args.recipe:
        recipes = [rcp for rcp in recipes if rcp.__name__ == args.recipe + "Recipe"]
        if not recipes:
            raise ValueError("Unknown recipe %s;\nValid recipes are: %s" %
                             (args.recipe, ", ".join(rcp.__name__[:-6] for rcp in mojoland.list_recipes())))

    for recipe in recipes:
        connoisseur.degustate(recipe)
