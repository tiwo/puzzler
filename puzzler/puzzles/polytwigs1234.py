#!/usr/bin/env python
# -*- coding: utf-8 -*-
# $Id$

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2012 by David J. Goodger
# License: GPL 2 (see __init__.py)

"""
Concrete polytwig (orders 1 through 4) puzzles.
"""

from puzzler.puzzles.polytwigs import Polytwigs1234, OneSidedPolytwigs1234


class Polytwigs1234Hex1(Polytwigs1234):

    """1175 solutions"""

    height = 4
    width = 4

    svg_rotation = 0

    holes = ((1,1,0), (1,2,0))

    def coordinates(self):
        for coord in self.coordinates_hexagon(2):
            if coord not in self.holes:
                yield coord

    def customize_piece_data(self):
        self.piece_data['P4'][-1]['flips'] = None
        self.piece_data['P4'][-1]['rotations'] = (0, 1, 2)


class Polytwigs1234Hex2(Polytwigs1234Hex1):

    """1506 solutions"""

    holes = ((0,2,0), (2,1,0))


class Polytwigs1234Hex3(Polytwigs1234Hex1):

    """2019 solutions"""

    holes = ((1,2,1), (2,2,2))


class Polytwigs1234Hex4(Polytwigs1234Hex1):

    """2007 solutions"""

    holes = ((1,1,2), (1,2,1))


class Polytwigs1234Hex5(Polytwigs1234Hex1):

    """958 solutions"""

    holes = ((1,2,2), (2,1,1))


class Polytwigs1234Hex6(Polytwigs1234Hex1):

    """962 solutions"""

    holes = ((1,2,2), (1,1,1))


class Polytwigs1234UnborderedTrapezoid5x4(Polytwigs1234):

    """0 solutions"""

    height = 4
    width = 5

    def coordinates(self):
        return self.coordinates_trapezoid_unbordered(5, 4)

    def customize_piece_data(self):
        self.piece_data['P4'][-1]['flips'] = None


class Polytwigs1234InsetRectangle4x2(Polytwigs1234):

    """many solutions"""

    height = 4
    width = 5

    svg_rotation = 0

    def coordinates(self):
        return self.coordinates_inset_rectangle(4, 2)

    def customize_piece_data(self):
        self.piece_data['P4'][-1]['flips'] = None


class OneSidedPolytwigs1234Trapezoid5x2(OneSidedPolytwigs1234):

    """many solutions"""

    height = 3
    width = 6

    def coordinates(self):
        return self.coordinates_trapezoid(5, 2)

    def customize_piece_data(self):
        OneSidedPolytwigs1234.customize_piece_data(self)
        self.piece_data['P4'][-1]['flips'] = None


class OneSidedPolytwigs1234ElongatedHexagon3x2_1(OneSidedPolytwigs1234):

    """many solutions"""

    height = 4
    width = 5

    holes = set(((1,1,1), (3,1,1)))

    def coordinates(self):
        for coord in self.coordinates_elongated_hexagon(3, 2):
            if coord not in self.holes:
                yield coord

    def customize_piece_data(self):
        OneSidedPolytwigs1234.customize_piece_data(self)
        self.piece_data['P4'][-1]['flips'] = None # !!! ineffective!
        self.piece_data['P4'][-1]['rotations'] = (0,1,2)


class OneSidedPolytwigs1234ElongatedHexagon3x2_2(
    OneSidedPolytwigs1234ElongatedHexagon3x2_1):

    """many solutions"""

    holes = set(((1,1,2), (0,2,0)))

    def customize_piece_data(self):
        OneSidedPolytwigs1234.customize_piece_data(self)
        self.piece_data['P4'][-1]['flips'] = None


class OneSidedPolytwigs1234ElongatedHexagon3x2_3(
    OneSidedPolytwigs1234ElongatedHexagon3x2_2):

    """many solutions"""

    holes = set(((2,0,1), (1,2,1)))


class OneSidedPolytwigs1234ElongatedHexagon3x2_4(
    OneSidedPolytwigs1234ElongatedHexagon3x2_1):

    """many solutions"""

    holes = set(((3,0,1), (1,2,1)))

    def customize_piece_data(self):
        OneSidedPolytwigs1234.customize_piece_data(self)
        self.piece_data['P4'][-1]['rotations'] = (0,1,2)


class OneSidedPolytwigs1234ElongatedHexagon3x2_5(
    OneSidedPolytwigs1234ElongatedHexagon3x2_4):

    """many solutions"""

    holes = set(((1,1,2), (3,2,2)))


class OneSidedPolytwigs1234ElongatedHexagon3x2_6(
    OneSidedPolytwigs1234ElongatedHexagon3x2_2):

    """many solutions"""

    holes = set(((2,2,1), (1,2,1)))


class OneSidedPolytwigs1234ElongatedHexagon3x2_7(
    OneSidedPolytwigs1234ElongatedHexagon3x2_2):

    """many solutions"""

    holes = set(((1,3,0), (1,3,2)))


class OneSidedPolytwigs1234ElongatedHexagon3x2_8(
    OneSidedPolytwigs1234ElongatedHexagon3x2_2):

    """many solutions"""

    holes = set(((0,2,0), (3,2,2)))


class OneSidedPolytwigs1234Triangle1(OneSidedPolytwigs1234):

    """many solutions"""

    height = 5
    width = 5

    holes = set(((1,1,2), (1,2,1), (2,1,0)))

    def coordinates(self):
        return sorted(set(self.coordinates_triangle(4)) - self.holes)


class OneSidedPolytwigs1234Triangle2(OneSidedPolytwigs1234Triangle1):

    """many solutions"""

    holes = set(((0,2,0), (2,0,1), (2,2,2)))


class OneSidedPolytwigs1234Triangle3(OneSidedPolytwigs1234Triangle1):

    """many solutions"""

    holes = set(((0,3,0), (1,2,1), (1,3,2)))


class OneSidedPolytwigs1234Triangle4(OneSidedPolytwigs1234Triangle1):

    """many solutions"""

    holes = set(((1,2,0), (1,2,1), (1,2,2)))
