#!/usr/bin/env python
# $Id$

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2015 by David J. Goodger
# License: GPL 2 (see __init__.py)

"""
Concrete polyhex (order 1 through 4) puzzles.
"""

from puzzler.puzzles.polyhexes import Polyhexes1234, OneSidedPolyhexes1234


class Polyhexes1234_4x10(Polyhexes1234):

    """3,665,348 solutions"""

    height = 4
    width = 10

    def customize_piece_data(self):
        self.piece_data['P4'][-1]['flips'] = None
        self.piece_data['P4'][-1]['rotations'] = (0,1,2)


class Polyhexes1234_5x8(Polyhexes1234):

    """7,578,295 solutions"""

    height = 5
    width = 8

    def customize_piece_data(self):
        self.piece_data['P4'][-1]['flips'] = None
        self.piece_data['P4'][-1]['rotations'] = (0,1,2)


class Polyhexes1234_6x7(Polyhexes1234):

    """
    3,832,702 solutions

    Design by Dan Klarskov.
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


class Polyhexes1234ElongatedHexagon13x2(Polyhexes1234):

    """1,389,980 solutions"""

    height = 3
    width = 14

    def coordinates(self):
        return self.coordinates_elongated_hexagon(13, 2)

    def customize_piece_data(self):
        self.piece_data['P4'][-1]['flips'] = None
        self.piece_data['P4'][-1]['rotations'] = (0,1,2)


class Polyhexes1234ElongatedHexagon3x5(Polyhexes1234):

    """
    many solutions

    Design by Dan Klarskov.
    """

    height = 9
    width = 7

    holes = set(((2,5), (3,3), (4,4)))

    svg_rotation = 90

    def coordinates(self):
        coords = set(self.coordinates_elongated_hexagon(3, 5)) - self.holes
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P4'][-1]['flips'] = None


class Polyhexes1234IrregularHexagon1(Polyhexes1234):

    """
    37,293,445 solutions

    Design by Dan Klarskov.
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


class Polyhexes1234IrregularHexagon2(Polyhexes1234):

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


class Polyhexes1234Trapezoid9x8(Polyhexes1234):

    """
    1,310,969 many solutions

    Design by Dan Klarskov.
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


class Polyhexes1234Triangle(Polyhexes1234):

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


class Polyhexes1234Triangle2(Polyhexes1234):

    """851,458 solutions"""

    height = 9
    width = 9

    def coordinates(self):
        coords = (
            set(self.coordinates_triangle(9))
            - set(self.coordinates_trapezoid(3, 2, offset=(0,6))))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P4'][-1]['flips'] = None


class Polyhexes1234TrilobedCrown(Polyhexes1234):

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


class Polyhexes1234JaggedHexagon1(Polyhexes1234):

    """
    213,477 solutions

    Design by Dan Klarskov.
    """

    height = 9
    width = 9

    holes = set(((3,5), (4,3), (5,4)))

    def coordinates(self):
        coords = (
            set(list(self.coordinates_hexagram(3))
                + list(self.coordinates_hexagon(4, offset=(1,1))))
            - self.holes)
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P4'][-1]['flips'] = None
        self.piece_data['P4'][-1]['rotations'] = (0, 1)


class Polyhexes1234JaggedHexagon2(Polyhexes1234JaggedHexagon1):

    """
    70,634 solutions

    Design by Kate Jones.
    """

    holes = set(((3,6), (3,3), (6,3)))


class Polyhexes1234JaggedHexagon3(Polyhexes1234JaggedHexagon1):

    """
    247,392 solutions

    Design by Kate Jones.
    """

    holes = set(((2,4), (4,6), (6,2)))


class Polyhexes1234KnobbedHexagon1(Polyhexes1234):

    """
    17,683 solutions

    Design by Dan Klarskov.
    """

    height = 9
    width = 9

    holes = set(((3,5), (4,3), (5,4)))

    extras = ((0,4), (0,8), (4,0), (4,8), (8,0), (8,4))

    def coordinates(self):
        coords = (
            set(self.coordinates_hexagon(4, offset=(1,1)))
            - self.holes)
        for x, y in self.extras:
            coords.add(self.coordinate_offset(x, y, None))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P4'][-1]['flips'] = None
        self.piece_data['P4'][-1]['rotations'] = (0, 1)


class Polyhexes1234KnobbedHexagon2(Polyhexes1234KnobbedHexagon1):

    """9,398 solutions"""

    holes = set(((3,6), (3,3), (6,3)))


class Polyhexes1234KnobbedHexagon3(Polyhexes1234KnobbedHexagon1):

    """12,714 solutions"""

    holes = set(((2,4), (4,6), (6,2)))


class Polyhexes1234KnobbedHexagon4(Polyhexes1234KnobbedHexagon1):

    """many solutions"""

    holes = set()

    extras = ((0,4), (4,8), (8,0),)

    svg_rotation = -30


class Polyhexes1234KnobbedHexagon5(Polyhexes1234KnobbedHexagon1):

    """many solutions"""

    holes = set()

    extras = ((0,6), (6,0), (6,6),)


class Polyhexes1234IrregularHexagon3(Polyhexes1234):

    """655,208 solutions"""

    height = 9
    width = 8

    holes = set(Polyhexes1234.coordinates_hexagon(2, offset=(2,2)))
    holes.add((2,5))
    holes.update(Polyhexes1234.coordinates_triangle(2))
    holes.update(Polyhexes1234.coordinates_triangle(2, offset=(8,0)))

    def coordinates(self):
        for coord in self.coordinates_trapezoid(10,9):
            if coord not in self.holes:
                yield coord

    def customize_piece_data(self):
        self.piece_data['P4'][-1]['flips'] = None


class Polyhexes1234IrregularHexagon4(Polyhexes1234):

    """1,361,945 solutions"""

    width = 9
    height = 7

    holes = set(Polyhexes1234.coordinates_hexagon(2, offset=(2,2)))
    holes.update(((0,0), (9,0)))

    def coordinates(self):
        for coord in self.coordinates_trapezoid(10,7):
            if coord not in self.holes:
                yield coord

    def customize_piece_data(self):
        self.piece_data['P4'][-1]['flips'] = None


class Polyhexes1234IrregularHexagon5(Polyhexes1234):

    """many solutions"""

    width = 7
    height = 8

    holes = set(Polyhexes1234.coordinates_triangle(3))
    holes.update(Polyhexes1234.coordinates_triangle(3, offset=(7,0)))

    def coordinates(self):
        for coord in self.coordinates_trapezoid(10,8):
            if coord not in self.holes:
                yield coord

    def customize_piece_data(self):
        self.piece_data['P4'][-1]['flips'] = None


class Polyhexes1234ElongatedHexagon2x6Ring(Polyhexes1234):

    """659,517 solutions"""

    width = 7
    height = 11

    hole = set(Polyhexes1234.coordinates_hexagon(2, offset=(2,4)))

    svg_rotation = 90

    def coordinates(self):
        for coord in self.coordinates_elongated_hexagon(2, 6):
            if coord not in self.hole:
                yield coord

    def customize_piece_data(self):
        self.piece_data['P4'][-1]['flips'] = None
        self.piece_data['P4'][-1]['rotations'] = (0,1,2)


class Polyhexes1234DiamondRing(Polyhexes1234):

    """83,837 solutions"""

    width = 7
    height = 7

    hole = set(Polyhexes1234.coordinates_parallelogram(3, 3, offset=(2,2)))

    svg_rotation = 30

    def coordinates(self):
        for coord in self.coordinates_parallelogram(7, 7):
            if coord not in self.hole:
                yield coord

    def customize_piece_data(self):
        self.piece_data['P4'][-1]['flips'] = None
        self.piece_data['P4'][-1]['rotations'] = (0,1,2)


class Polyhexes1234HexagonRing1(Polyhexes1234):

    """
    11,417 solutions

    Equivalent to the inner ring of the featured solution `Kadon's Hexnut
    puzzle <http://gamepuzzles.com/esspoly2.htm#HN>`__.  See
    `polyhexes12345.Polyhexes12345HexagonRing1` for the full puzzle.
    """

    width = 9
    height = 9

    holes = (
        set(Polyhexes1234.coordinates_hexagon(3, offset=(2,2)))
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
        set(Polyhexes1234.coordinates_hexagon(3, offset=(2,2)))
        .union(((1,4), (7,4))))


class Polyhexes1234StaggeredRectangle8x5(Polyhexes1234):

    """
    many solutions

    Design by Dan Klarskov.
    """

    width = 8
    height = 8

    svg_rotation = -30

    def coordinates(self):
        return self.coordinates_staggered_rectangle(8, 5)

    def customize_piece_data(self):
        self.piece_data['P4'][-1]['rotations'] = (0,1,2)


class Polyhexes1234StaggeredRectangle10x4(Polyhexes1234):

    """many solutions"""

    width = 10
    height = 8

    svg_rotation = -30

    def coordinates(self):
        return self.coordinates_staggered_rectangle(10, 4)

    def customize_piece_data(self):
        self.piece_data['P4'][-1]['rotations'] = (0,1,2)


class Polyhexes1234StaggeredRectangle5x8(Polyhexes1234):

    """
    many solutions

    Design by Dan Klarskov.
    """

    width = 5
    height = 10

    svg_rotation = -30

    def coordinates(self):
        return self.coordinates_staggered_rectangle(5, 8)

    def customize_piece_data(self):
        self.piece_data['P4'][-1]['flips'] = None


class Polyhexes1234StaggeredRectangle4x10(Polyhexes1234):

    """many solutions"""

    width = 4
    height = 11

    svg_rotation = -30

    def coordinates(self):
        return self.coordinates_staggered_rectangle(4, 10)

    def customize_piece_data(self):
        self.piece_data['P4'][-1]['rotations'] = (0,1,2)


class OneSidedPolyhexes1234X1(OneSidedPolyhexes1234):

    """many solutions"""

    height = 13
    width = 11

    holes = set(
        tuple(OneSidedPolyhexes1234.coordinates_butterfly(2, 2, offset=(4,5)))
        + ((0,8), (0,9), (1,8), (9,4), (10,3), (10,4)))

    svg_rotation = 60

    def coordinates(self):
        for coord in self.coordinates_butterfly(8, 6):
            if coord not in self.holes:
                yield coord

    def customize_piece_data(self):
        OneSidedPolyhexes1234.customize_piece_data(self)
        self.piece_data['P4'][-1]['rotations'] = (0,1,2)
