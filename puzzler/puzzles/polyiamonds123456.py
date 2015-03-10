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


class OneSidedPolyiamonds123456Triangle1(OneSidedPolyiamonds123456):

    """many solutions"""

    height = 13
    width = 13

    holes = set(((1,1,0), (1,10,0), (10,1,0)))

    def coordinates(self):
        coords = (
            set(self.coordinates_triangle(self.height))
            - self.holes)
        return sorted(coords)

    def customize_piece_data(self):
        OneSidedPolyiamonds123456.customize_piece_data(self)
        self.piece_data['P5'][-1]['rotations'] = (0,1)


class OneSidedPolyiamonds123456Triangle2(OneSidedPolyiamonds123456Triangle1):

    """many solutions"""

    holes = set(((1,1,1), (1,9,1), (9,1,1)))


class OneSidedPolyiamonds123456Triangle3(OneSidedPolyiamonds123456Triangle1):

    """many solutions"""

    holes = set(((2,2,0), (2,8,0), (8,2,0)))


class OneSidedPolyiamonds123456Triangle4(OneSidedPolyiamonds123456Triangle1):

    """many solutions"""

    holes = set(((2,2,1), (2,7,1), (7,2,1)))


class OneSidedPolyiamonds123456Triangle5(OneSidedPolyiamonds123456Triangle1):

    """many solutions"""

    holes = set(((3,3,0), (3,6,0), (6,3,0)))


class OneSidedPolyiamonds123456Triangle6(OneSidedPolyiamonds123456Triangle1):

    """many solutions"""

    holes = set(((3,3,1), (3,5,1), (5,3,1)))


class OneSidedPolyiamonds123456Triangle7(OneSidedPolyiamonds123456Triangle1):

    """many solutions"""

    holes = set(((0,6,0), (6,0,0), (6,6,0)))


class OneSidedPolyiamonds123456Triangle8(OneSidedPolyiamonds123456Triangle1):

    """many solutions"""

    holes = set(((1,5,1), (5,1,1), (5,5,1)))


class OneSidedPolyiamonds123456Triangle9(OneSidedPolyiamonds123456Triangle1):

    """many solutions"""

    holes = set(((2,5,0), (5,2,0), (5,5,0)))


class OneSidedPolyiamonds123456Triangle10(OneSidedPolyiamonds123456Triangle1):

    """many solutions"""

    holes = set(((3,4,1), (4,3,1), (4,4,1)))
