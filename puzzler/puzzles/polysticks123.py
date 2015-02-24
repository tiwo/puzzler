#!/usr/bin/env python
# $Id$

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2015 by David J. Goodger
# License: GPL 2 (see __init__.py)

"""
Concrete polystick (orders 1 through 3) puzzles.
"""

from puzzler import coordsys
from puzzler.puzzles.polysticks import Polysticks123


class Polysticks123_4x4ClippedCorners1(Polysticks123):

    """
    21 solutions
    """

    width = 4
    height = 4

    holes = set(((0,0,0), (0,0,1), (2,3,0), (3,2,1)))

    """
    no solutions:
    
    holes = set(((1,1,0), (1,1,1), (1,2,0), (2,1,1)))

    holes = set(((0,1,1), (1,0,0), (1,3,0), (3,1,1)))
    """

    def coordinates(self):
        for coord in self.coordinates_bordered(self.width, self.height):
            if coord not in self.holes:
                yield coord

    def customize_piece_data(self):
        self.piece_data['L3'][-1]['flips'] = None
        self.piece_data['L3'][-1]['rotations'] = (0, 1)


class Polysticks123_4x4ClippedCorners2(Polysticks123_4x4ClippedCorners1):

    """
    132 solutions
    """

    holes = set(((0,3,0), (0,2,1), (2,3,0), (3,2,1)))

    def customize_piece_data(self):
        self.piece_data['L3'][-1]['flips'] = None
