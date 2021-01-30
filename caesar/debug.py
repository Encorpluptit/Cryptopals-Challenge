#
# EPITECH PROJECT, 2020
# debug
# File description:
# Simple debug function
#

import os
import sys

def debug(*args):
    if os.environ.get("IS_DEBUG_MODE"):
        print(*args, file=sys.stderr)
