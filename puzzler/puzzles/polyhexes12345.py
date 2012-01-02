#!/usr/bin/env python
# $Id$

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2012 by David J. Goodger
# License: GPL 2 (see __init__.py)

"""
Concrete polyhex (order 1 through 5) puzzles.
"""

from puzzler.puzzles.polyhexes import Polyhex12345


class Polyhex12345_3x50(Polyhex12345):

    """0 solutions?"""

    height = 3
    width = 50

    duplicate_conditions = ({'rotate_180': True},)


class Polyhex12345_5x30(Polyhex12345):

    """? solutions"""

    height = 5
    width = 30

    duplicate_conditions = ({'rotate_180': True},)


class Polyhex12345_6x25(Polyhex12345):

    """? solutions"""

    height = 6
    width = 25

    duplicate_conditions = ({'rotate_180': True},)


class Polyhex12345_10x15(Polyhex12345):

    """? solutions"""

    height = 10
    width = 15

    duplicate_conditions = ({'rotate_180': True},)
