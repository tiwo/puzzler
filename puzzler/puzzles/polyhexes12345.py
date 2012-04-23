#!/usr/bin/env python
# $Id$

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2012 by David J. Goodger
# License: GPL 2 (see __init__.py)

"""
Concrete polyhex (order 1 through 5) puzzles.
"""

from puzzler.puzzles import polyhexes
from puzzler.puzzles.polyhexes import Polyhexes12345, OneSidedPolyhexes12345


class Polyhexes12345_3x50(Polyhexes12345):

    """0 solutions?"""

    height = 3
    width = 50

    def customize_piece_data(self):
        self.piece_data['P4'][-1]['flips'] = None
        self.piece_data['P4'][-1]['rotations'] = (0,1,2)


class Polyhexes12345_5x30(Polyhexes12345_3x50):

    """? solutions"""

    height = 5
    width = 30


class Polyhexes12345_6x25(Polyhexes12345_3x50):

    """? solutions"""

    height = 6
    width = 25


class Polyhexes12345_10x15(Polyhexes12345_3x50):

    """? solutions"""

    height = 10
    width = 15


class Polyhexes12345HexagonRing1(Polyhexes12345):

    """
    many solutions

    Equivalent to `Kadon's Hexnut puzzle`__, and subdivided similarly to the
    featured solution by Michael Keller, with the pentahexes in an outer ring
    and the order 1 through 4 polyhexes in an inner ring.

    __ http://gamepuzzles.com/esspoly2.htm#HN
    """

    height = 15
    width = 15

    hole = set(Polyhexes12345.coordinates_hexagon(3, offset=(5,5)))

    def coordinates(self):
        coords = set(self.coordinates_hexagon(8)) - self.hole
        inner_ring = (
            set(self.coordinates_hexagon(5, offset=(3,3))) - self.hole
            - set(((3,7), (11,7))))
        self.pentahex_coords = sorted(coords - inner_ring)
        self.polyhex_1234_coords = sorted(inner_ring)
        return sorted(coords)

    def build_matrix(self):
        self.build_regular_matrix(
            (polyhexes.Monohex.piece_data.keys()
             + polyhexes.Dihex.piece_data.keys()
             + sorted(polyhexes.Trihexes.piece_data.keys())
             + sorted(polyhexes.Tetrahexes.piece_data.keys())),
            self.polyhex_1234_coords)
        self.build_regular_matrix(
            sorted(polyhexes.Pentahexes.piece_data.keys()),
            self.pentahex_coords)

    def customize_piece_data(self):
        self.piece_data['P5'][-1]['flips'] = None
        self.piece_data['P5'][-1]['rotations'] = (0,1,2)


class Polyhexes12345HexagonRing_X1(Polyhexes12345HexagonRing1):

    """
    0 solutions
    """

    def coordinates(self):
        coords = set(self.coordinates_hexagon(8)) - self.hole
        self.monohex_coords = [self.coordinate_offset(5, 5, None)]
        inner_ring = (
            set(self.coordinates_hexagon(5, offset=(3,3))) - self.hole
            - set(((3,7), (11,7))))
        self.pentahex_coords = sorted(coords - inner_ring)
        self.dihex_trihex_coords = sorted(
            inner_ring.intersection(
            set(self.coordinates_parallelogram(6, 2, offset=(6,3)))))
        self.tetrahex_coords = sorted(
            inner_ring - set(self.dihex_trihex_coords)
            - set(self.monohex_coords))
        assert coords == set(
            self.monohex_coords + self.dihex_trihex_coords
            + self.tetrahex_coords + self.pentahex_coords)
        return sorted(coords)

    def build_matrix(self):
        self.build_regular_matrix(
            polyhexes.Monohex.piece_data.keys(), self.monohex_coords)
        self.build_regular_matrix(
            (polyhexes.Dihex.piece_data.keys()
             + sorted(polyhexes.Trihexes.piece_data.keys())),
            self.dihex_trihex_coords)
        self.build_regular_matrix(
            sorted(polyhexes.Tetrahexes.piece_data.keys()),
            self.tetrahex_coords)
        self.build_regular_matrix(
            sorted(polyhexes.Pentahexes.piece_data.keys()),
            self.pentahex_coords)


class Polyhexes12345HexagonRing_X2(Polyhexes12345HexagonRing1):

    """0 solutions"""

    def coordinates(self):
        coords = set(self.coordinates_hexagon(8)) - self.hole
        inner_ring = (
            set(self.coordinates_hexagon(5, offset=(3,3))) - self.hole
            - set(((3,7), (11,3))))
        self.pentahex_coords = sorted(coords - inner_ring)
        self.polyhex_123_coords = sorted(
            inner_ring.intersection(
            set(self.coordinates_trapezoid(6, 15))))
        self.tetrahex_coords = sorted(
            inner_ring - set(self.polyhex_123_coords))
        assert coords == set(
            self.polyhex_123_coords + self.tetrahex_coords
            + self.pentahex_coords)
        return sorted(coords)

    def build_matrix(self):
        self.build_regular_matrix(
            (polyhexes.Monohex.piece_data.keys()
             + polyhexes.Dihex.piece_data.keys()
             + sorted(polyhexes.Trihexes.piece_data.keys())),
            self.polyhex_123_coords)
        self.build_regular_matrix(
            sorted(polyhexes.Tetrahexes.piece_data.keys()),
            self.tetrahex_coords)
        self.build_regular_matrix(
            sorted(polyhexes.Pentahexes.piece_data.keys()),
            self.pentahex_coords)


class Polyhexes12345SemiRegularHexagon15x2(Polyhexes12345):

    """many solutions"""

    height = 16
    width = 16

    def coordinates(self):
        return self.coordinates_semi_regular_hexagon(15, 2)

    def customize_piece_data(self):
        self.piece_data['P4'][-1]['flips'] = None
        self.piece_data['P4'][-1]['rotations'] = (0, 1)


class Polyhexes12345Triangle(Polyhexes12345):

    """many solutions"""

    height = 17
    width = 17

    def coordinates(self):
        return sorted(
            set(self.coordinates_triangle(17))
            - set(self.coordinates_triangle(2, offset=(5,5))))

    def customize_piece_data(self):
        self.piece_data['P4'][-1]['flips'] = None
        self.piece_data['P4'][-1]['rotations'] = (0, 1)


class Polyhexes12345Trapezoid17x15(Polyhexes12345):

    """many solutions"""

    width = 17
    height = 15

    def coordinates(self):
        return self.coordinates_trapezoid(self.width, self.height)

    def customize_piece_data(self):
        self.piece_data['P4'][-1]['flips'] = None


class Polyhexes12345Trapezoid18x12(Polyhexes12345Trapezoid17x15):

    """many solutions"""

    width = 18
    height = 12


class Polyhexes12345Trapezoid32x5(Polyhexes12345Trapezoid17x15):

    """many solutions"""

    width = 32
    height = 5


class OneSidedPolyhexes12345Hexagon(OneSidedPolyhexes12345):

    """many solutions"""

    width = 17
    height = 17

    def coordinates(self):
        return self.coordinates_hexagon(9)


class OneSidedPolyhexes12345_31x7(OneSidedPolyhexes12345):

    """many solutions"""

    width = 31
    height = 7


class OneSidedPolyhexes12345Trapezoid22x14(OneSidedPolyhexes12345):

    """many solutions"""

    width = 22
    height = 14

    def coordinates(self):
        return self.coordinates_trapezoid(self.width, self.height)
