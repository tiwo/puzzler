#!/usr/bin/env python
# -*- coding: utf-8 -*-
# $Id$

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2015 by David J. Goodger
# License: GPL 2 (see __init__.py)

"""
Concrete polyomino (orders 2 through 4) puzzles.
"""

from puzzler.puzzles.polyominoes import Polyominoes234, OneSidedPolyominoes234


class OneSidedPolyominoes234Square(OneSidedPolyominoes234):

    """7,252 solutions"""

    width = 6
    height = 6

    def build_matrix(self):
        keys = sorted(self.pieces.keys())
        coords, aspect = self.pieces['I3'][0]
        for y in range(2):
            for x in range(3):
                translated = aspect.translate((x, y))
                self.build_matrix_row('I3', translated)
        keys.remove('I3')
        self.build_regular_matrix(keys)


class OneSidedPolyominoes234Octagon(OneSidedPolyominoes234):

    """1,023 solutions"""

    width = 7
    height = 7

    holes = set(((-1,3), (3,-1), (3,7), (7,3), (3,3)))

    def coordinates(self):
        coords = (
            set(self.coordinates_diamond(5, offset=(-1,-1)))
            - self.holes)
        return sorted(coords)

    def build_matrix(self):
        keys = sorted(self.pieces.keys())
        coords, aspect = self.pieces['I4'][0]
        for offset in ((2,0), (1,1)):
            translated = aspect.translate(offset)
            self.build_matrix_row('I4', translated)
        keys.remove('I4')
        self.build_regular_matrix(keys)
