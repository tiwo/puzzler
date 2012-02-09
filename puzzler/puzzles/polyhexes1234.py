#!/usr/bin/env python
# $Id$

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2012 by David J. Goodger
# License: GPL 2 (see __init__.py)

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


class Polyhex1234_6x7(Polyhex1234):

    """? (many) solutions"""

    height = 6
    width = 7

    check_for_duplicates = False

    hole = set(((3,2), (3,3)))

    def coordinates(self):
        for coord in self.coordinates_parallelogram(self.width, self.height):
            if coord not in self.hole:
                yield coord

    def customize_piece_data(self):
        self.piece_data['P4'][-1]['rotations'] = (0,1,2)
