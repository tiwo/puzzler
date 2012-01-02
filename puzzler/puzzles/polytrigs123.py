#!/usr/bin/env python
# $Id$

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2012 by David J. Goodger
# License: GPL 2 (see __init__.py)

"""
Concrete polytrig (orders 1 through 3) puzzles.
"""

from puzzler.puzzles.polytrigs import Polytrigs123, OneSidedPolytrigs123


class Polytrigs123_4x3(Polytrigs123):

    """many solutions."""

    width = 5
    height = 4

    def coordinates(self):
        return self.coordinates_bordered(4, 3)

    def customize_piece_data(self):
        self.piece_data['P3'][-1]['rotations'] = (0,1,2)


class Polytrigs123Trapezoid5x4(Polytrigs123):

    """many solutions."""

    width = 6
    height = 5

    def coordinates(self):
        return self.coordinates_trapezoid(5, 4)

    def customize_piece_data(self):
        self.piece_data['P3'][-1]['flips'] = None


class Polytrigs123Chevron3x2(Polytrigs123):

    """many solutions."""

    width = 6
    height = 5

    def coordinates(self):
        return self.coordinates_chevron(3, 2)


class Polytrigs123Butterfly4x2(Polytrigs123):

    """many solutions."""

    width = 7
    height = 5

    def coordinates(self):
        for coord in self.coordinates_butterfly(4, 2):
            if coord != (2, 3, 0):
                yield coord


class Polytrigs123Trapezoid7x2_1(Polytrigs123):

    """many solutions."""

    width = 8
    height = 3

    hole = set([(2,2,0)])

    def coordinates(self):
        for coord in self.coordinates_trapezoid(7, 2):
            if coord not in self.hole:
                yield coord


class Polytrigs123Trapezoid7x2_2(Polytrigs123Trapezoid7x2_1):

    """many solutions."""

    hole = set([(3,0,0)])


class Polytrigs123Triangle5_1(Polytrigs123):

    """many solutions."""

    width = 6
    height = 5

    hole = set([(2,1,1), (2,1,2)])

    def coordinates(self):
        for coord in self.coordinates_triangle(5):
            if coord not in self.hole:
                yield coord


class Polytrigs123Triangle5_2(Polytrigs123Triangle5_1):

    """many solutions."""

    hole = set([(1,1,0), (2,1,0)])


class Polytrigs123Triangle5_3(Polytrigs123Triangle5_1):

    """many solutions."""

    hole = set([(1,2,0), (0,4,0)])


class Polytrigs123Triangle5_4(Polytrigs123Triangle5_1):

    """many solutions."""

    hole = set([(0,1,0), (3,1,0)])


class Polytrigs123Triangle5_5(Polytrigs123Triangle5_1):

    """many solutions."""

    hole = set([(0,2,0), (2,2,0)])


class Polytrigs123Triangle5_6(Polytrigs123Triangle5_1):

    """many solutions."""

    hole = set([(0,3,0), (1,3,0)])


class Polytrigs123Triangle5_7(Polytrigs123Triangle5_1):

    """many solutions."""

    hole = set([(1,0,0), (3,0,0)])


class Polytrigs123Triangle5_8(Polytrigs123Triangle5_1):

    """many solutions."""

    hole = set([(2,0,0), (1,2,0)])


class OneSidedPolytrigs123Trapezoid10x2(OneSidedPolytrigs123):

    """many solutions."""

    width = 11
    height = 3

    def coordinates(self):
        for coord in self.coordinates_trapezoid(10, 2):
            if coord != (4, 1, 0):
                yield coord

    def customize_piece_data(self):
        OneSidedPolytrigs123.customize_piece_data(self)
        self.piece_data['P3'][-1]['flips'] = None


class OneSidedPolytrigs123Trapezoid7x4(OneSidedPolytrigs123):

    """many solutions."""

    width = 8
    height = 5

    def coordinates(self):
        hole = set([(3,1,1), (3,1,2), (2,2,0), (2,2,1), (3,2,2)])
        for coord in self.coordinates_trapezoid(7, 4):
            if coord not in hole:
                yield coord

    def customize_piece_data(self):
        OneSidedPolytrigs123.customize_piece_data(self)
        #self.piece_data['P3'][-1]['flips'] = None


class OneSidedPolytrigs123Parallelogram9x2(OneSidedPolytrigs123):

    """many solutions."""

    width = 10
    height = 3

    def coordinates(self):
        for coord in self.coordinates_bordered(9, 2):
            if coord != (4, 1, 0):
                yield coord

    def customize_piece_data(self):
        OneSidedPolytrigs123.customize_piece_data(self)
        self.piece_data['P3'][-1]['rotations'] = (0,1,2)


class OneSidedPolytrigs123Parallelogram5x4(OneSidedPolytrigs123):

    """many solutions."""

    width = 6
    height = 5

    def coordinates(self):
        hole = set([(3,1,1), (3,1,2), (2,2,0), (2,2,1), (3,2,2)])
        for coord in self.coordinates_bordered(5, 4):
            if coord not in hole:
                yield coord

    def customize_piece_data(self):
        OneSidedPolytrigs123.customize_piece_data(self)
        #self.piece_data['P3'][-1]['rotations'] = (0,1,2)


class OneSidedPolytrigs123Butterfly6x2(OneSidedPolytrigs123):

    """many solutions."""

    width = 9
    height = 5

    def coordinates(self):
        hole = set(self.coordinates_hexagon_unbordered(1, offset=(3,1,0)))
        for coord in self.coordinates_butterfly(6, 2):
            if coord not in hole:
                yield coord

    def customize_piece_data(self):
        OneSidedPolytrigs123.customize_piece_data(self)
        self.piece_data['P3'][-1]['rotations'] = (0,1,2)
        self.piece_data['P3'][-1]['flips'] = None


class OneSidedPolytrigs123ElongatedHex4x2_1(OneSidedPolytrigs123):

    """many solutions."""

    width = 7
    height = 5

    hole = set([(1,2,0), (2,2,0), (3,2,0), (4,2,0)])

    def coordinates(self):
        for coord in self.coordinates_elongated_hexagon(4, 2):
            if coord not in self.hole:
                yield coord


class OneSidedPolytrigs123ElongatedHex4x2_2(
    OneSidedPolytrigs123ElongatedHex4x2_1):

    """many solutions."""

    hole = set([(2,3,1), (3,3,2), (1,4,0), (2,4,0)])


class OneSidedPolytrigs123ElongatedHex4x2_3(
    OneSidedPolytrigs123ElongatedHex4x2_1):

    """many solutions."""

    hole = set([(3,0,0), (4,0,0), (1,4,0), (2,4,0)])


class OneSidedPolytrigs123ElongatedHex4x2_4(
    OneSidedPolytrigs123ElongatedHex4x2_1):

    """many solutions."""

    hole = set([(0,4,0), (1,4,0), (2,4,0), (3,4,0)])


class OneSidedPolytrigs123ElongatedHex4x2_5(
    OneSidedPolytrigs123ElongatedHex4x2_1):

    """many solutions."""

    hole = set([(3,1,0), (2,2,0), (3,2,0), (2,3,0)])


class OneSidedPolytrigs123ElongatedHex4x2_6(
    OneSidedPolytrigs123ElongatedHex4x2_1):

    """many solutions."""

    hole = set([(2,2,0), (3,2,0), (3,2,1), (3,2,2)])


class OneSidedPolytrigs123ElongatedHex4x2_7(
    OneSidedPolytrigs123ElongatedHex4x2_1):

    """many solutions."""

    hole = set([(2,0,2), (6,0,1), (0,3,1), (5,3,2)])


class OneSidedPolytrigs123ElongatedHex4x2_8(
    OneSidedPolytrigs123ElongatedHex4x2_1):

    """many solutions."""

    hole = set([(2,0,2), (1,1,2), (6,0,1), (6,1,1)])


class OneSidedPolytrigs123ElongatedHex4x2_9(
    OneSidedPolytrigs123ElongatedHex4x2_1):

    """many solutions."""

    hole = set([(3,1,0), (1,2,0), (4,2,0), (2,3,0)])


class OneSidedPolytrigs123ElongatedHex4x2_10(
    OneSidedPolytrigs123ElongatedHex4x2_1):

    """many solutions."""

    hole = set([(3,1,2), (3,1,1), (4,1,2), (4,1,1)])


class OneSidedPolytrigs123ElongatedHex4x2_11(
    OneSidedPolytrigs123ElongatedHex4x2_1):

    """many solutions."""

    hole = set([(3,1,1), (4,1,2), (3,2,1), (3,2,2)])


class OneSidedPolytrigs123Trapezoid8x3_1(OneSidedPolytrigs123):

    """many solutions."""

    width = 9
    height = 4

    hole = set([(3,1,1), (3,1,2), (4,1,1), (4,1,2)])

    def coordinates(self):
        for coord in self.coordinates_trapezoid(8, 3):
            if coord not in self.hole:
                yield coord


class OneSidedPolytrigs123Trapezoid8x3_2(OneSidedPolytrigs123Trapezoid8x3_1):

    """many solutions."""

    hole = set([(2,1,1), (2,1,2), (5,1,1), (5,1,2)])


class OneSidedPolytrigs123Trapezoid8x3_3(OneSidedPolytrigs123Trapezoid8x3_1):

    """many solutions."""

    hole = set([(2,1,1), (3,1,2), (4,1,1), (5,1,2)])


class OneSidedPolytrigs123Trapezoid8x3_4(OneSidedPolytrigs123Trapezoid8x3_1):

    """many solutions."""

    hole = set([(1,1,1), (3,1,2), (4,1,1), (6,1,2)])


class OneSidedPolytrigs123Chevron9x1(OneSidedPolytrigs123):

    """many solutions."""

    width = 11
    height = 3

    hole = set([(9,1,0)])

    def coordinates(self):
        for coord in self.coordinates_chevron(9, 1):
            if coord not in self.hole:
                yield coord
