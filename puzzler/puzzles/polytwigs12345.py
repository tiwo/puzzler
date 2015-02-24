#!/usr/bin/env python
# -*- coding: utf-8 -*-
# $Id$

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2015 by David J. Goodger
# License: GPL 2 (see __init__.py)

"""
Concrete polytwig (orders 1 through 5) puzzles.
"""

from puzzler.puzzles.polytwigs import Polytwigs12345, OneSidedPolytwigs12345


class Polytwigs12345InsetRectangle5x5(Polytwigs12345):

    """many solutions"""

    height = 8
    width = 6

    svg_rotation = 0

    def coordinates(self):
        return self.coordinates_inset_rectangle(5, 5)

    def customize_piece_data(self):
        self.piece_data['R5'][-1]['flips'] = None
        self.piece_data['R5'][-1]['rotations'] = (0,1,2)


class Polytwigs12345_6x4(Polytwigs12345):

    """
    Abstract superclass for 6x4 parallelogram, subclass must provide 3 holes.
    """

    height = 5
    width = 7

    # subclass must override; provide a set of 3 coordinates
    holes = None

    def coordinates(self):
        for coord in Polytwigs12345.coordinates(self):
            if coord not in self.holes:
                yield coord

    def customize_piece_data(self):
        self.piece_data['R5'][-1]['flips'] = None
        self.piece_data['R5'][-1]['rotations'] = (0,1,2)


class Polytwigs12345_6x4_1(Polytwigs12345_6x4):

    """many solutions"""

    holes = set(((4,1,2), (3,2,2), (2,3,2)))


class Polytwigs12345_6x4_2(Polytwigs12345_6x4):

    """many solutions"""

    holes = set(((1,2,0), (3,2,2), (4,2,0)))


class Polytwigs12345_6x4_3(Polytwigs12345_6x4):

    """many solutions"""

    holes = set(((2,2,0), (3,2,2), (3,2,0)))


class Polytwigs12345_6x4_4(Polytwigs12345_6x4):

    """many solutions"""

    holes = set(((3,1,1), (3,2,2), (3,2,1)))


class Polytwigs12345_6x4_5(Polytwigs12345_6x4):

    """many solutions"""

    holes = set(((2,2,2), (3,2,2), (4,2,2)))


class Polytwigs12345_6x4_6(Polytwigs12345_6x4):

    """many solutions"""

    holes = set(((2,1,1), (3,2,2), (4,2,1)))


class Polytwigs12345_6x4_7(Polytwigs12345_6x4):

    """many solutions"""

    holes = set(((2,1,2), (3,2,2), (4,3,2)))


class Polytwigs12345_6x4_8(Polytwigs12345_6x4):

    """many solutions"""

    holes = set(((1,2,2), (3,2,2), (5,2,2)))


class Polytwigs12345_6x4_9(Polytwigs12345_6x4):

    """many solutions"""

    holes = set(((1,1,2), (3,2,2), (5,3,2)))


class Polytwigs12345_6x4_10(Polytwigs12345_6x4):

    """many solutions"""

    holes = set(((3,0,1), (3,2,2), (3,3,1)))


class Polytwigs12345_6x4_11(Polytwigs12345_6x4):

    """many solutions"""

    holes = set(((4,0,1), (3,2,2), (2,3,1)))


class Polytwigs12345_6x4_12(Polytwigs12345_6x4):

    """many solutions"""

    holes = set(((5,0,1), (3,2,2), (1,3,1)))


class Polytwigs12345_6x4_13(Polytwigs12345_6x4):

    """many solutions"""

    holes = set(((2,0,1), (3,2,2), (4,3,1)))


class Polytwigs12345_6x4_14(Polytwigs12345_6x4):

    """many solutions"""

    holes = set(((1,0,1), (3,2,2), (5,3,1)))


class Polytwigs12345_6x4_15(Polytwigs12345_6x4):

    """many solutions"""

    holes = set(((1,2,1), (3,2,2), (5,1,1)))


class Polytwigs12345TrapezoidRing9x3(Polytwigs12345):

    """many solutions"""

    height = 4
    width = 10

    def coordinates(self):
        hole = set(self.coordinates_unbordered(6, 1, (1, 1, 0)))
        for coord in self.coordinates_trapezoid(9, 3):
            if coord not in hole:
                yield coord

    def customize_piece_data(self):
        self.piece_data['R5'][-1]['flips'] = None


class Polytwigs12345ElongatedHexagon4x3(Polytwigs12345):

    """many solutions"""

    height = 6
    width = 7

    def coordinates(self):
        for coord in self.coordinates_elongated_hexagon(4, 3):
            if coord != (3,2,1):
                yield coord

    def customize_piece_data(self):
        self.piece_data['R5'][-1]['flips'] = None
        self.piece_data['R5'][-1]['rotations'] = (0,1,2)


class Polytwigs12345Butterfly8x2_1(Polytwigs12345):

    """many solutions"""

    height = 4
    width = 10

    holes = set(((4,1,1), (5,1,1)))

    def coordinates(self):
        for coord in self.coordinates_butterfly(8, 2):
            if coord not in self.holes:
                yield coord

    def customize_piece_data(self):
        self.piece_data['R5'][-1]['flips'] = None
        self.piece_data['R5'][-1]['rotations'] = (0,1,2)


class Polytwigs12345Butterfly8x2_2(Polytwigs12345Butterfly8x2_1):

    """many solutions"""

    holes = set(((3,1,1), (6,1,1)))


class Polytwigs12345Butterfly8x2_3(Polytwigs12345Butterfly8x2_1):

    """many solutions"""

    holes = set(((2,1,1), (7,1,1)))


class Polytwigs12345Butterfly8x2_4(Polytwigs12345Butterfly8x2_1):

    """many solutions"""

    holes = set(((1,1,1), (8,1,1)))


class OneSidedPolytwigs12345Butterfly12x2(OneSidedPolytwigs12345):

    """many solutions"""

    height = 4
    width = 14

    def coordinates(self):
        return self.coordinates_butterfly(12, 2)


class OneSidedPolytwigs12345_12x3_1(OneSidedPolytwigs12345):

    """many solutions"""

    height = 4
    width = 13

    holes = set(((5,1,1), (6,1,1), (7,1,1)))

    def coordinates(self):
        for coord in self.coordinates_bordered(12, 3):
            if coord not in self.holes:
                yield coord


class OneSidedPolytwigs12345_12x3_2(OneSidedPolytwigs12345_12x3_1):

    """many solutions"""

    holes = set(((4,1,1), (6,1,1), (8,1,1)))


class OneSidedPolytwigs12345_12x3_3(OneSidedPolytwigs12345_12x3_1):

    """many solutions"""

    holes = set(((3,1,1), (6,1,1), (9,1,1)))


class OneSidedPolytwigs12345_12x3_4(OneSidedPolytwigs12345_12x3_1):

    """many solutions"""

    holes = set(((2,1,1), (6,1,1), (10,1,1)))


class OneSidedPolytwigs12345_12x3_5(OneSidedPolytwigs12345_12x3_1):

    """many solutions"""

    holes = set(((1,1,1), (6,1,1), (11,1,1)))


class OneSidedPolytwigs12345_12x3_6(OneSidedPolytwigs12345_12x3_1):

    """many solutions"""

    holes = set(((6,0,1), (6,1,1), (6,2,1)))


class OneSidedPolytwigs12345Trapezoid13x3_1(OneSidedPolytwigs12345):

    """many solutions"""

    height = 4
    width = 14

    holes = set(((5,2,0), (6,1,1), (6,2,2)))

    def coordinates(self):
        for coord in self.coordinates_trapezoid(13, 3):
            if coord not in self.holes:
                yield coord


class OneSidedPolytwigs12345Trapezoid13x3_2(
    OneSidedPolytwigs12345Trapezoid13x3_1):

    """many solutions"""

    holes = set(((6,1,0), (6,1,1), (6,1,2)))


class OneSidedPolytwigs12345Trapezoid13x3_3(
    OneSidedPolytwigs12345Trapezoid13x3_1):

    """many solutions"""

    holes = set(((5,1,1), (6,1,1), (7,1,1)))


class OneSidedPolytwigs12345Trapezoid13x3_4(
    OneSidedPolytwigs12345Trapezoid13x3_1):

    """many solutions"""

    holes = set(((4,1,1), (6,1,1), (8,1,1)))


class OneSidedPolytwigs12345Trapezoid13x3_5(
    OneSidedPolytwigs12345Trapezoid13x3_1):

    """many solutions"""

    holes = set(((3,1,1), (6,1,1), (9,1,1)))


class OneSidedPolytwigs12345Trapezoid13x3_6(
    OneSidedPolytwigs12345Trapezoid13x3_1):

    """many solutions"""

    holes = set(((2,1,1), (6,1,1), (10,1,1)))
