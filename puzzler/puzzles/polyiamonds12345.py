#!/usr/bin/env python
# $Id$

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2015 by David J. Goodger
# License: GPL 2 (see __init__.py)

"""
Concrete polyiamonds (orders 1 through 5) puzzles.
"""

from puzzler.puzzles.polyiamonds import (
    Polyiamonds12345, OneSidedPolyiamonds12345)


class Polyiamonds12345ElongatedHexagon9x1(Polyiamonds12345):

    """23,168 solutions"""

    height = 2
    width = 10

    def coordinates(self):
        return self.coordinates_elongated_hexagon(9, 1)

    def customize_piece_data(self):
        self.piece_data['P5'][-1]['flips'] = None
        self.piece_data['P5'][-1]['rotations'] = (0,1,2)


class Polyiamonds12345ElongatedHexagon5x2Ring(Polyiamonds12345):

    """
    6,852 solutions

    Design by Dan Klarskov
    """

    height = 4
    width = 7

    def coordinates(self):
        coords = (
            set(self.coordinates_elongated_hexagon(5, 2))
            - set(self.coordinates_elongated_hexagon(2, 1, offset=(2,1,0))))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P5'][-1]['flips'] = None
        self.piece_data['P5'][-1]['rotations'] = (0,1,2)


class Polyiamonds12345StackedElongatedHexagons5x1_1(Polyiamonds12345):

    """792 solutions"""

    height = 4
    width = 7

    def coordinates(self):
        coords = (
            set(list(self.coordinates_elongated_hexagon(5, 1, offset=(1,0,0)))
                + list(self.coordinates_elongated_hexagon(5, 1,
                                                          offset=(0,2,0))))
            - set(self.coordinates_butterfly(2, 1, offset=(2,1,0))))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P5'][-1]['flips'] = None
        self.piece_data['P5'][-1]['rotations'] = (0,1,2)


class Polyiamonds12345StackedElongatedHexagons5x1_2(Polyiamonds12345):

    """784 solutions"""

    height = 4
    width = 7

    holes = set(((2,1,1), (2,2,0), (3,1,1), (3,2,0), (4,1,1), (4,2,0)))
    
    def coordinates(self):
        coords = (
            set(list(self.coordinates_elongated_hexagon(5, 1, offset=(1,0,0)))
                + list(self.coordinates_elongated_hexagon(5, 1,
                                                          offset=(0,2,0))))
            - self.holes)
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P5'][-1]['flips'] = None
        self.piece_data['P5'][-1]['rotations'] = (0,1,2)


class Polyiamonds12345Butterfly10x1(Polyiamonds12345):

    """2,000 solutions"""

    height = 2
    width = 11

    def coordinates(self):
        return self.coordinates_butterfly(10, 1)

    def customize_piece_data(self):
        self.piece_data['P5'][-1]['flips'] = None
        self.piece_data['P5'][-1]['rotations'] = (0,1,2)


class Polyiamonds12345Peanut(Polyiamonds12345):

    """
    240,892 solutions

    Design by Dan Klarskov
    """

    height = 6
    width = 5

    holes = set(((0,2,1), (0,3,0), (4,2,1), (4,3,0)))

    def coordinates(self):
        coords = set(self.coordinates_elongated_hexagon(2, 3)) - self.holes
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P5'][-1]['flips'] = None
        self.piece_data['P5'][-1]['rotations'] = (0,1,2)


class Polyiamonds12345Trapezoid1(Polyiamonds12345):

    """98,807 solutions"""

    height = 4
    width = 7

    holes = set(((2,1,1), (2,2,0)))

    def coordinates(self):
        coords = set(self.coordinates_trapezoid(7, 4)) - self.holes
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P5'][-1]['flips'] = None


class Polyiamonds12345IrregularHexagon1(Polyiamonds12345Trapezoid1):

    """
    611,834 solutions

    Design by Dan Klarskov
    """

    width = 6

    holes = set(((0,0,0), (6,0,0)))


class Polyiamonds12345Snowflake1(Polyiamonds12345):

    """
    6,757 solutions

    Design by Dan Klarskov
    """

    height = 6
    width = 6

    holes = set((
        (-1,4,1), (1,1,0), (1,6,0), (4,-1,1), (4,4,1), (6,1,0),
        (2,4,0), (2,2,1), (3,2,0), (3,2,1)))

    def coordinates(self):
        coords = (
            set(self.coordinates_hexagram(2, offset=(-1, -1, 0))) - self.holes)
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P5'][-1]['flips'] = None


class Polyiamonds12345Snowflake2(Polyiamonds12345Snowflake1):

    """1,240 solutions"""

    holes = set((
        (-1,4,1), (1,1,0), (1,6,0), (4,-1,1), (4,4,1), (6,1,0),
        (2,2,1), (2,3,0), (3,2,1), (3,3,0)))

    def customize_piece_data(self):
        self.piece_data['P5'][-1]['flips'] = None
        self.piece_data['P5'][-1]['rotations'] = (0,1,2)


class Polyiamonds12345Snowflake3(Polyiamonds12345Snowflake2):

    """466 solutions"""

    holes = set((
        (-1,4,1), (1,1,0), (1,6,0), (4,-1,1), (4,4,1), (6,1,0),
        (3,1,1), (3,2,0), (2,3,1), (2,4,0)))


class Polyiamonds12345Snowflake_x1(Polyiamonds12345Snowflake2):

    """0 solutions"""

    holes = set((
        (-1,4,1), (1,1,0), (1,6,0), (4,-1,1), (4,4,1), (6,1,0),
        (2,2,0), (1,3,1), (4,2,0), (3,3,1)))


class Polyiamonds12345Bat(Polyiamonds12345):

    """
    61,251 solutions

    Design by Dan Klarskov
    """

    height = 5
    width = 5

    svg_rotation = 30

    def coordinates(self):
        coords = set(
            list(self.coordinates_parallelogram(3, 3))
            + list(self.coordinates_parallelogram(3, 3, offset=(1,1,0)))
            + list(self.coordinates_parallelogram(3, 3, offset=(2,2,0))))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P5'][-1]['flips'] = None
        self.piece_data['P5'][-1]['rotations'] = (0, 1, 2)


class Polyiamonds12345Snake(Polyiamonds12345):

    """
    2,268 solutions

    Design by Dan Klarskov
    """

    width = 14
    height = 7

    svg_rotation = 30

    def coordinates(self):
        coords = set()
        for i in range(6):
            coords.update(self.coordinates_parallelogram(2, 2, offset=(i,i,0)))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P5'][-1]['flips'] = None
        self.piece_data['P5'][-1]['rotations'] = (0, 1, 2)


class Polyiamonds12345Bird1(Polyiamonds12345):

    """
    42,665 solutions

    Design by Dan Klarskov
    """

    width = 6
    height = 6

    svg_rotation = 30

    def coordinates(self):
        coords = set(
            list(self.coordinates_parallelogram(4, 2, offset=(0,1,0)))
            + list(self.coordinates_parallelogram(2, 2, offset=(3,4,0)))
            + list(self.coordinates_elongated_hexagon(3, 1, offset=(2,2,0)))
            + list(self.coordinates_hexagon(1, offset=(2,0,0))))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P5'][-1]['flips'] = None


class Polyiamonds12345Crab(Polyiamonds12345):

    """
    8,698 solutions

    Design by Dan Klarskov
    """

    width = 8
    height = 6

    holes = set(((2,0,0), (7,0,0)))

    def coordinates(self):
        coords = set(
            list(self.coordinates_semiregular_hexagon(1, 2))
            + list(self.coordinates_semiregular_hexagon(1, 2, offset=(5,0,0)))
            + list(self.coordinates_triangle(4, offset=(2,2,0))))
        coords -= self.holes
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P5'][-1]['flips'] = None


class Polyiamonds12345Dog1(Polyiamonds12345):

    """
    28,614 solutions

    Inspired by a design by Dan Klarskov
    """

    width = 6
    height = 6

    holes = set(((2,4,0), (3,1,1)))

    extras = ((0,5,1), (3,0,0))

    svg_rotation = 90

    def coordinates(self):
        coords = set(
            list(self.coordinates_elongated_hexagon(1, 3, offset=(1,0,0)))
            + list(self.coordinates_hexagon(2, offset=(2,1,0)))
            + [self.coordinate_offset(x, y, z, None)
               for x, y, z in self.extras])
        coords -= self.holes
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P5'][-1]['flips'] = None


class Polyiamonds12345X1(Polyiamonds12345):

    """1,182 solutions"""

    height = 6
    width = 8

    holes = set(((2,5,1), (3,3,1), (4,2,0), (5,0,0)))

    def coordinates(self):
        for coord in self.coordinates_butterfly(5, 3):
            if coord not in self.holes:
                yield coord

    def customize_piece_data(self):
        self.piece_data['P5'][-1]['flips'] = None
        self.piece_data['P5'][-1]['rotations'] = (0, 1, 2)


class Polyiamonds12345ElongatedHexOnHex1(Polyiamonds12345):

    """
    2,810 solutions

    Design by Dan Klarskov
    """

    width = 8
    height = 4

    holes = set(((4,1,0), (3,2,1)))

    def coordinates(self):
        coords = set(
            list(self.coordinates_elongated_hexagon(7, 1, offset=(0,1,0)))
            + list(self.coordinates_hexagon(2, offset=(2,0,0))))
        coords -= self.holes
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P5'][-1]['flips'] = None
        self.piece_data['P5'][-1]['rotations'] = (0, 1, 2)


class Polyiamonds12345ElongatedHexOnHex2(Polyiamonds12345ElongatedHexOnHex1):

    """310 solutions"""

    holes = set(((4,0,1), (3,3,0)))


class OneSidedPolyiamonds12345Hexagon1(OneSidedPolyiamonds12345):

    """5,085,616 solutions"""

    height = 6
    width = 6

    holes = set(((3,2,0), (2,3,1)))

    def coordinates(self):
        coords = set(self.coordinates_hexagon(3)) - self.holes
        return sorted(coords)

    def customize_piece_data(self):
        OneSidedPolyiamonds12345.customize_piece_data(self)
        self.piece_data['P5'][-1]['rotations'] = (0, 1, 2)


class OneSidedPolyiamonds12345Hexagon2(OneSidedPolyiamonds12345Hexagon1):

    """6,407,224 solutions"""

    holes = set(((3,1,1), (2,4,0)))


class OneSidedPolyiamonds12345SemiRegularHexagon4x2(OneSidedPolyiamonds12345):

    """56,524,164 solutions"""

    height = 6
    width = 6

    def coordinates(self):
        return self.coordinates_semiregular_hexagon(4, 2)

    def customize_piece_data(self):
        OneSidedPolyiamonds12345.customize_piece_data(self)
        self.piece_data['P5'][-1]['rotations'] = (0, 1, 2)


class OneSidedPolyiamonds12345X1(OneSidedPolyiamonds12345):

    """142,128 solutions"""

    height = 8
    width = 8

    holes = set((
        (-1,7,1), (3,0,0), (4,7,1), (8,0,0),
        (1,7,1), (2,6,1), (2,7,0), (2,7,1),
        (5,0,0), (5,0,1), (5,1,0), (6,0,0)))

    def coordinates(self):
        for coord in self.coordinates_butterfly(6, 4, offset=(-1,0,0)):
            if coord not in self.holes:
                yield coord

    def customize_piece_data(self):
        OneSidedPolyiamonds12345.customize_piece_data(self)
        self.piece_data['P5'][-1]['rotations'] = (0, 1, 2)
