#!/usr/bin/env python
# $Id$

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2012 by David J. Goodger
# License: GPL 2 (see __init__.py)

"""
Concrete polyiamonds (orders 1 through 5) puzzles.
"""

from puzzler.puzzles.polyiamonds import (
    Polyiamonds12345, OneSidedPolyiamonds12345)


class Polyiamonds12345ElongatedHexagon9x1(Polyiamonds12345):

    """34,097 solutions"""

    height = 2
    width = 10

    def coordinates(self):
        return self.coordinates_elongated_hexagon(9, 1)

    def customize_piece_data(self):
        self.piece_data['P5'][-1]['flips'] = None
        self.piece_data['P5'][-1]['rotations'] = (0,1,2)


class Polyiamonds12345ElongatedHexagon5x2Ring(Polyiamonds12345):

    """
    10,254 solutions

    Discovered by Dan Klarskov
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

    """1,145 solutions"""

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

    """1,217 solutions"""

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

    """2,906 solutions"""

    height = 2
    width = 11

    def coordinates(self):
        return self.coordinates_butterfly(10, 1)

    def customize_piece_data(self):
        self.piece_data['P5'][-1]['flips'] = None
        self.piece_data['P5'][-1]['rotations'] = (0,1,2)


class Polyiamonds12345Peanut(Polyiamonds12345):

    """
    362,047 solutions

    Discovered by Dan Klarskov
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

    """126,151 solutions"""

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
    878,738 solutions

    Discovered by Dan Klarskov
    """

    width = 6

    holes = set(((0,0,0), (6,0,0)))


class Polyiamonds12345Snowflake1(Polyiamonds12345):

    """
    9,930 solutions

    Discovered by Dan Klarskov
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

    """1,788 solutions"""

    holes = set((
        (-1,4,1), (1,1,0), (1,6,0), (4,-1,1), (4,4,1), (6,1,0),
        (2,2,1), (2,3,0), (3,2,1), (3,3,0)))

    def customize_piece_data(self):
        self.piece_data['P5'][-1]['flips'] = None
        self.piece_data['P5'][-1]['rotations'] = (0,1,2)


class Polyiamonds12345Snowflake3(Polyiamonds12345Snowflake2):

    """670 solutions"""

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
    92,778 solutions

    Discovered by Dan Klarskov
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


class Polyiamonds12345X1(Polyiamonds12345):

    """many solutions"""

    height = 6
    width = 8

    holes = set(((2,5,1), (3,3,1), (4,2,0), (5,0,0)))

    def coordinates(self):
        for coord in self.coordinates_butterfly(5, 3):
            if coord not in self.holes:
                yield coord


class OneSidedPolyiamonds12345Hexagon1(OneSidedPolyiamonds12345):

    """3,710,485 solutions"""
    # w/o duplicate control: 15,256,848 (103,760,913 searches)

    height = 6
    width = 6

    holes = set(((3,2,0), (2,3,1)))

    t4_offsets = (
        (0,3,0), (0,4,0), (1,2,0), (1,3,0), (1,4,0), (2,1,0), (3,0,0))

    def coordinates(self):
        coords = set(self.coordinates_hexagon(3)) - self.holes
        return sorted(coords)

    def build_matrix(self):
        keys = sorted(self.pieces.keys())
        t_coords, t_aspect = self.pieces['T4'][0]
        for offset in self.t4_offsets:
            translated = t_aspect.translate(offset)
            self.build_matrix_row('T4', translated)
        keys.remove('T4')
        self.build_regular_matrix(keys)


class OneSidedPolyiamonds12345Hexagon2(OneSidedPolyiamonds12345Hexagon1):

    """4,833,439 solutions"""
    # w/o duplicate control: 19,221,672 (152,631,658 searches)

    holes = set(((3,1,1), (2,4,0)))

    t4_offsets = (
        (0,3,0), (0,4,0), (1,2,0), (1,3,0), (2,1,0), (2,2,0), (3,0,0))


class OneSidedPolyiamonds12345SemiRegularHexagon4x2(OneSidedPolyiamonds12345):

    """many solutions"""

    height = 6
    width = 6

    def coordinates(self):
        return self.coordinates_semiregular_hexagon(4, 2)


class OneSidedPolyiamonds12345X1(OneSidedPolyiamonds12345):

    """many solutions"""

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
