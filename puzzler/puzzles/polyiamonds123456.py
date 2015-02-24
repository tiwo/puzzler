#!/usr/bin/env python
# $Id$

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2015 by David J. Goodger
# License: GPL 2 (see __init__.py)

"""
Concrete polyiamonds (orders 1 through 6) puzzles.
"""

from puzzler.puzzles.polyiamonds import (
    Polyiamonds123456, OneSidedPolyiamonds123456)


class Polyiamonds123456ElongatedHexagon3x5(Polyiamonds123456):

    """many solutions"""

    height = 10
    width = 8

    def coordinates(self):
        return self.coordinates_elongated_hexagon(3, 5)

    def customize_piece_data(self):
        self.piece_data['P5'][-1]['flips'] = None
        self.piece_data['P5'][-1]['rotations'] = (0,1,2)


class OneSidedPolyiamonds123456SemiRegularHexagon11x1(
    OneSidedPolyiamonds123456):

    """many solutions"""

    height = 12
    width = 12

    def coordinates(self):
        return self.coordinates_semiregular_hexagon(11, 1)
