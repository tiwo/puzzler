#!/usr/bin/env python
# $Id$

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2012 by David J. Goodger
# License: GPL 2 (see __init__.py)

"""
Concrete hexahex puzzles.

All puzzles including the O06 piece must have at least one single-hexagon
hole.
"""

from puzzler.puzzles.polyhexes import Hexahexes, OneSidedHexahexes
from puzzler.coordsys import Hexagonal2DCoordSet


class HexahexesTriangle1(Hexahexes):

    """ solutions"""

    width = 31
    height = 31

    holes = set(((10,10), (9,9), (9,12), (12,9)))

    def coordinates(self):
        coords = set(self.coordinates_triangle(31)) - self.holes
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P06'][-1]['rotations'] = (0, 1)
        self.piece_data['P06'][-1]['flips'] = None


class HexahexesTriangle2(HexahexesTriangle1):

    """ solutions"""

    width = 30
    height = 30

    holes = set(((10,10), (0,0), (0,30), (30,0)))


class HexahexesHexagonRing1(Hexahexes):

    """
    many solutions

    Design from `Kadon's Hexnut II
    <http://www.gamepuzzles.com/esspoly2.htm#HN2>`__
    """

    width = 27
    height = 27

    def coordinates(self):
        coords = (
            set(self.coordinates_hexagon(14))
            - set(self.coordinates_hexagon(5, offset=(9,9))))
        coords.update(
            set(self.coordinates_hexagon(2, offset=(12,12))) - set(((13,13),)))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P06'][-1]['rotations'] = None
        self.piece_data['P06'][-1]['flips'] = None


class HexahexesHexagonRing_x1(Hexahexes):

    """0 solutions: impossible, since O06 requires a hole"""

    width = 27
    height = 27

    extras = set(((9,13), (9,17), (13,9), (13,17), (17,9), (17,13)))

    def coordinates(self):
        coords = (
            set(self.coordinates_hexagon(14))
            - set(self.coordinates_hexagon(5, offset=(9,9))))
        coords.update(
            set(self.coordinate_offset(x, y, None) for x, y in self.extras))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P06'][-1]['rotations'] = None
        self.piece_data['P06'][-1]['flips'] = None
