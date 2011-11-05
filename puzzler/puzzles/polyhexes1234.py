#!/usr/bin/env python
# $Id$

"""
Concrete polyhex (order 1 through 4) puzzles.
"""

from puzzler.puzzles.polyhexes import Polyhex1234


class Polyhex1234_4x10(Polyhex1234):

    """? (many) solutions"""

    height = 4
    width = 10

    duplicate_conditions = ({'rotate_180': True},)


class Polyhex1234_5x8(Polyhex1234):

    """? (many) solutions"""

    height = 5
    width = 8

    duplicate_conditions = ({'rotate_180': True},)
