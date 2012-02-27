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

    """3,665,348 solutions"""

    height = 4
    width = 10

    def customize_piece_data(self):
        self.piece_data['P4'][-1]['flips'] = None
        self.piece_data['P4'][-1]['rotations'] = (0,1,2)


class Polyhex1234_5x8(Polyhex1234):

    """7,578,295 solutions"""

    height = 5
    width = 8

    def customize_piece_data(self):
        self.piece_data['P4'][-1]['flips'] = None
        self.piece_data['P4'][-1]['rotations'] = (0,1,2)


class Polyhex1234_6x7(Polyhex1234):

    """
    3,832,702 solutions

    Discovered by Dan Klarskov.
    """

    height = 6
    width = 7

    hole = set(((3,2), (3,3)))

    def coordinates(self):
        for coord in self.coordinates_parallelogram(self.width, self.height):
            if coord not in self.hole:
                yield coord

    def customize_piece_data(self):
        self.piece_data['P4'][-1]['rotations'] = (0,1,2)


class Polyhexes1234ElongatedHexagon13x2(Polyhex1234):

    """1,389,980 solutions"""

    height = 3
    width = 14

    def coordinates(self):
        return self.coordinates_elongated_hexagon(13, 2)

    def customize_piece_data(self):
        self.piece_data['P4'][-1]['flips'] = None
        self.piece_data['P4'][-1]['rotations'] = (0,1,2)


class Polyhexes1234IrregularHexagon1(Polyhex1234):

    """
    37,293,445 solutions

    Discovered by Dan Klarskov.
    """

    width = 8
    height = 7

    holes = set(((0,0), (8,0)))

    def coordinates(self):
        for coord in self.coordinates_trapezoid(9, 7):
            if coord not in self.holes:
                yield coord

    def customize_piece_data(self):
        self.piece_data['P4'][-1]['flips'] = None


class Polyhexes1234IrregularHexagon2(Polyhex1234):

    """14,211,672 solutions"""

    height = 4
    width = 11

    holes = set(((0,0), (11,0)))

    def coordinates(self):
        for coord in self.coordinates_trapezoid(12, 4):
            if coord not in self.holes:
                yield coord

    def customize_piece_data(self):
        self.piece_data['P4'][-1]['flips'] = None


class Polyhexes1234Trapezoid9x8(Polyhex1234):

    """
    1,310,969 many solutions

    Discovered by Dan Klarskov.
    """

    height = 8
    width = 9

    holes = set(((2,3), (2,4), (3,2), (3,3)))

    def coordinates(self):
        for coord in self.coordinates_trapezoid(9, 8):
            if coord not in self.holes:
                yield coord

    def customize_piece_data(self):
        self.piece_data['P4'][-1]['flips'] = None


class Polyhexes1234Triangle(Polyhex1234):

    """427,731 solutions"""

    height = 9
    width = 9

    holes = set(((2,2), (2,3), (3,2), (3,3), (4,2)))

    def coordinates(self):
        for coord in self.coordinates_triangle(9):
            if coord not in self.holes:
                yield coord

    def customize_piece_data(self):
        self.piece_data['P4'][-1]['flips'] = None


class Polyhexes1234TrilobedCrown(Polyhex1234):

    """
    1,349,201 solutions

    Inspired by the `Snowflake puzzle
    <http://www.johnrausch.com/PuzzleWorld/puz/snowflake.htm>`_.
    """

    height = 9
    width = 9

    extras = ((1,4), (7,1), (4,7))

    svg_rotation = -30

    def coordinates(self):
        for coord in self.coordinates_hexagram(3):
            yield coord
        for (x,y) in self.extras:
            yield self.coordinate_offset(x, y, None)

    def customize_piece_data(self):
        self.piece_data['P4'][-1]['flips'] = None
        self.piece_data['P4'][-1]['rotations'] = (0, 1)


class Polyhexes1234IrregularHexagon3(Polyhex1234):

    """655,208 solutions"""

    height = 9
    width = 8

    holes = set(Polyhex1234.coordinates_hexagon(2, offset=(2,2)))
    holes.add((2,5))
    holes.update(Polyhex1234.coordinates_triangle(2))
    holes.update(Polyhex1234.coordinates_triangle(2, offset=(8,0)))

    def coordinates(self):
        for coord in self.coordinates_trapezoid(10,9):
            if coord not in self.holes:
                yield coord

    def customize_piece_data(self):
        self.piece_data['P4'][-1]['flips'] = None


class Polyhexes1234IrregularHexagon4(Polyhex1234):

    """1,361,945 solutions"""

    width = 9
    height = 7

    holes = set(Polyhex1234.coordinates_hexagon(2, offset=(2,2)))
    holes.update(((0,0), (9,0)))

    def coordinates(self):
        for coord in self.coordinates_trapezoid(10,7):
            if coord not in self.holes:
                yield coord

    def customize_piece_data(self):
        self.piece_data['P4'][-1]['flips'] = None


class Polyhexes1234IrregularHexagon5(Polyhex1234):

    """many solutions"""

    width = 7
    height = 8

    holes = set(Polyhex1234.coordinates_triangle(3))
    holes.update(Polyhex1234.coordinates_triangle(3, offset=(7,0)))

    def coordinates(self):
        for coord in self.coordinates_trapezoid(10,8):
            if coord not in self.holes:
                yield coord

    def customize_piece_data(self):
        self.piece_data['P4'][-1]['flips'] = None


class Polyhexes1234ElongatedHexagon2x6Ring(Polyhex1234):

    """659,517 solutions"""

    width = 7
    height = 11

    hole = set(Polyhex1234.coordinates_hexagon(2, offset=(2,4)))

    svg_rotation = 90

    def coordinates(self):
        for coord in self.coordinates_elongated_hexagon(2, 6):
            if coord not in self.hole:
                yield coord

    def customize_piece_data(self):
        self.piece_data['P4'][-1]['flips'] = None
        self.piece_data['P4'][-1]['rotations'] = (0,1,2)


class Polyhexes1234DiamondRing(Polyhex1234):

    """83,837 solutions"""

    width = 7
    height = 7

    hole = set(Polyhex1234.coordinates_parallelogram(3, 3, offset=(2,2)))

    svg_rotation = 30

    def coordinates(self):
        for coord in self.coordinates_parallelogram(7, 7):
            if coord not in self.hole:
                yield coord

    def customize_piece_data(self):
        self.piece_data['P4'][-1]['flips'] = None
        self.piece_data['P4'][-1]['rotations'] = (0,1,2)


class Polyhexes1234HexagonRing1(Polyhex1234):

    """
    11,417 solutions

    Equivalent to the inner ring of the featured solution `Kadon's Hexnut
    puzzle <http://gamepuzzles.com/esspoly2.htm#HN>`__.  See
    `polyhexes12345.Polyhexes12345HexagonRing1` for the full puzzle.
    """

    width = 9
    height = 9

    holes = (
        set(Polyhex1234.coordinates_hexagon(3, offset=(2,2)))
        .union(((0,4), (8,4))))

    def coordinates(self):
        for coord in self.coordinates_hexagon(5):
            if coord not in self.holes:
                yield coord

    def customize_piece_data(self):
        self.piece_data['P4'][-1]['flips'] = None
        self.piece_data['P4'][-1]['rotations'] = (0,1,2)


class Polyhexes1234HexagonRing2(Polyhexes1234HexagonRing1):

    """6,645 solutions"""

    holes = (
        set(Polyhex1234.coordinates_hexagon(3, offset=(2,2)))
        .union(((1,4), (7,4))))
