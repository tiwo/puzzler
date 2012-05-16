#!/usr/bin/env python
# $Id$

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2012 by David J. Goodger
# License: GPL 2 (see __init__.py)

"""
Concrete hexahex puzzles.

All puzzles which include the O06 piece must have at least one single-hexagon
hole.
"""

from puzzler.puzzles.polyhexes import Hexahexes, OneSidedHexahexes
from puzzler.coordsys import Hexagonal2DCoordSet


class HexahexesTriangle(Hexahexes):

    """Abstract base class"""

    width = 31
    height = 31

    holes = set()

    def coordinates(self):
        coords = set(self.coordinates_triangle(31)) - self.holes
        return sorted(coords)


class HexahexesTriangle1(HexahexesTriangle):

    """
    many solutions

    Design from Andrew Clarke's Poly Pages.
    """

    holes = set(((10,10), (5,5), (5,20), (20,5)))

    _find_known_solution = True

    if _find_known_solution:
        # Find a known solution (from Andrew Clarke's Poly Pages).
        # Fix pieces in known positions:
        restrictions = {
            #name: [(aspect, offset), ...],
            'O06': [(0, ( 4,  4))],
            'A06': [(0, (28,  0))],
            'I06': [(1, (11, 14))],
            'C06': [(3, ( 0,  3))],
            'C16': [(5, (33,  2))],
            'E06': [(4, ( 6,  4))],
            'M36': [(4, ( 9, 18))],
            'M46': [(2, ( 8, 11))],
            'N06': [(4, (17,  8))],
            'S06': [(5, ( 3,  0))],
            'S16': [(2, ( 7, 10))],
            'S26': [(1, (10,  7))],
            'T06': [(0, ( 2, 16))],
            'T16': [(4, (15,  0))],
            'T56': [(2, ( 7,  1))],
            'U06': [(2, ( 6,  0))],
            'U16': [(1, ( 1, 21))],
            'V06': [(1, (25,  0))],
            'X06': [(2, ( 3, 17))],
            'X16': [(0, ( 0, 23))],
            'Y06': [(3, (13,  4))],
            'Y16': [(4, ( 4, 14))],
            'Y26': [(2, ( 7,  8))],
            'Y66': [(2, (23,  0))],
            'Z06': [(0, ( 1, 12))],
            }

        def build_matrix(self):
            self.build_restricted_matrix()

    else:
        # General case

        def customize_piece_data(self):
            self.piece_data['P06'][-1]['rotations'] = (0, 1)
            self.piece_data['P06'][-1]['flips'] = None


class HexahexesTriangle2(HexahexesTriangle):

    """ solutions"""

    width = 30
    height = 30

    holes = set(((10,10), (0,0), (0,30), (30,0)))

    _find_known_solution = True

    if _find_known_solution:
        # Find a known solution (from Andrew Clarke's Poly Pages).
        # Fix pieces in known positions:
        restrictions = {
            #name: [(aspect, offset), ...],
            'O06': [(0, ( 9,  9))],
            'A06': [(0, (22,  1))],
            'I06': [(1, (11,  0))],
            'C06': [(4, (10,  3))],
            'C16': [(3, (12,  5))],
            'E06': [(1, ( 0, 18))],
            'M36': [(3, (18,  9))],
            'M46': [(2, (12,  8))],
            'N06': [(0, ( 0, 12))],
            'S06': [(3, ( 5, 14))],
            'S16': [(5, (11, 12))],
            'S26': [(2, ( 8, 18))],
            'T06': [(0, ( 2,  3))],
            'T16': [(2, ( 5, 21))],
            'T56': [(1, (16, 11))],
            'U06': [(0, ( 3, 18))],
            'U16': [(1, (19,  4))],
            'V06': [(0, ( 0, 27))],
            'X06': [(1, (14,  1))],
            'X16': [(0, (18,  5))],
            'Y06': [(3, ( 2, 15))],
            'Y16': [(0, (10,  6))],
            'Y26': [(2, (17,  7))],
            'Y66': [(0, ( 0, 25))],
            'Z06': [(2, ( 1,  5))],
            }

        def build_matrix(self):
            self.build_restricted_matrix()

    else:
        # General case

        def customize_piece_data(self):
            self.piece_data['P06'][-1]['rotations'] = (0, 1)
            self.piece_data['P06'][-1]['flips'] = None


class HexahexesTriangle3(HexahexesTriangle):

    """ solutions"""

    holes = set(((10,10), (9,9), (9,12), (12,9)))

    def customize_piece_data(self):
        self.piece_data['P06'][-1]['rotations'] = (0, 1)
        self.piece_data['P06'][-1]['flips'] = None


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
