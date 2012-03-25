#!/usr/bin/env python
# $Id$

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2012 by David J. Goodger
# License: GPL 2 (see __init__.py)

"""
Concrete tetrahex puzzles.
"""

from puzzler.puzzles.polyhexes import Tetrahexes


class Tetrahexes4x7(Tetrahexes):

    """9 solutions"""

    height = 4
    width = 7

    def customize_piece_data(self):
        self.piece_data['P4'][-1]['rotations'] = (0, 1, 2)
        

class Tetrahexes7x7Triangle(Tetrahexes):

    """0 solutions"""

    height = 7
    width = 7

    def coordinates(self):
        for y in range(self.height):
            for x in range(self.width):
                if x + y < self.height:
                    yield (x, y)


class Tetrahexes3x10Clipped(Tetrahexes):

    """2 solutions"""

    height = 3
    width = 10

    def coordinates(self):
        max = self.width + self.height - 2
        for y in range(self.height):
            for x in range(self.width):
                if (x + y != 0) and (x + y != max):
                    yield (x, y)

    def customize_piece_data(self):
        self.piece_data['P4'][-1]['flips'] = None
        self.piece_data['P4'][-1]['rotations'] = (0, 1, 2)


class TetrahexesCoin(Tetrahexes):

    """4 solutions"""

    height = 5
    width = 7

    def coordinates(self):
        max = self.width + self.height - 3
        for y in range(self.height):
            for x in range(self.width):
                if (x + y > 1) and (x + y < max) and not (x == 3 and y == 2):
                    yield (x, y)

    def customize_piece_data(self):
        self.piece_data['P4'][-1]['flips'] = None
        self.piece_data['P4'][-1]['rotations'] = (0, 1, 2)
