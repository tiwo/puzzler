#!/usr/bin/env python
# -*- coding: utf-8 -*-
# $Id$

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2015 by David J. Goodger
# License: GPL 2 (see __init__.py)

"""
Concrete tetratwig puzzles.
"""

from puzzler.puzzles.polytwigs import Tetratwigs, OneSidedTetratwigs


class Tetratwigs3x1(Tetratwigs):

    """0 solutions"""

    height = 2
    width = 4

    def coordinates(self):
        return self.coordinates_bordered(3, 1)


class TetratwigsArch(Tetratwigs):

    """2 solutions"""

    height = 3
    width = 4

    svg_rotation = 0

    def coordinates(self):
        return self.coordinates_vertically_staggered_rectangle(3, 1)

    def customize_piece_data(self):
        self.piece_data['P4'][-1]['flips'] = None


class OneSidedTetratwigsButterfly(OneSidedTetratwigs):

    """0 solutions"""

    height = 4
    width = 4

    def coordinates(self):
        return self.coordinates_inset_rectangle(3, 2)
    

class OneSidedTetratwigs3x2_1(OneSidedTetratwigs):

    """0 solutions"""

    height = 3
    width = 4

    holes = set(((0,1,0), (1,1,0), (2,1,0)))

    def coordinates(self):
        for coord in self.coordinates_bordered(3, 2):
            if coord not in self.holes:
                yield coord


class OneSidedTetratwigs3x2_2(OneSidedTetratwigs3x2_1):

    """0 solutions"""

    holes = set(((1,1,0), (1,1,2), (2,1,2)))


class OneSidedTetratwigsTriangle(OneSidedTetratwigs):

    height = 4
    width = 4

    def coordinates(self):
        for coord in self.coordinates_triangle(3):
            if coord not in self.holes:
                yield coord


class OneSidedTetratwigsTriangle_1(OneSidedTetratwigsTriangle):

    """2 solutions"""

    holes = set(((1,1,0), (1,1,1), (1,1,2)))

    def customize_piece_data(self):
        OneSidedTetratwigs.customize_piece_data(self)
        self.piece_data['W4'][-1]['rotations'] = (4, 5)


class OneSidedTetratwigsTriangle_2(OneSidedTetratwigsTriangle):

    """1 solution"""

    holes = set(((0,2,0), (1,1,1), (1,2,2)))

    def customize_piece_data(self):
        OneSidedTetratwigs.customize_piece_data(self)
        self.piece_data['W4'][-1]['rotations'] = (3,)


class OneSidedTetratwigsTriangle_3(OneSidedTetratwigsTriangle):

    """2 solutions"""

    holes = set(((1,0,1), (1,1,1), (2,0,1)))


class OneSidedTetratwigsTriangle_4(OneSidedTetratwigsTriangle):

    """1 solution"""

    holes = set(((0,1,0), (1,2,2), (2,1,2)))


class OneSidedTetratwigsTriangle_5(OneSidedTetratwigsTriangle):

    """0 solutions"""

    holes = set(((0,2,0), (1,0,1), (2,1,2)))


class OneSidedTetratwigsArch(OneSidedTetratwigs):

    height = 4
    width = 4

    svg_rotation = 0

    def coordinates(self):
        for coord in self.coordinates_vertically_staggered_rectangle(3, 2):
            if coord not in self.holes:
                yield coord


class OneSidedTetratwigsArch_1(OneSidedTetratwigsArch):

    """1 solution"""

    holes = set(((0,2,0), (1,1,0), (2,1,0)))

    def customize_piece_data(self):
        OneSidedTetratwigs.customize_piece_data(self)
        self.piece_data['W4'][-1]['rotations'] = (3,4,5)


class OneSidedTetratwigsArch_2(OneSidedTetratwigsArch):

    """1 solution"""

    holes = set(((1,2,1), (1,1,0), (2,2,2)))

    def customize_piece_data(self):
        OneSidedTetratwigs.customize_piece_data(self)
        self.piece_data['W4'][-1]['rotations'] = (3,)


class OneSidedTetratwigsArch_3(OneSidedTetratwigsArch):

    """1 solution"""

    holes = set(((1,2,1), (1,1,0), (2,1,0)))


class OneSidedTetratwigsArch_4(OneSidedTetratwigsArch):

    """1 solution"""

    holes = set(((1,1,0), (2,1,0), (2,2,2)))


class OneSidedTetratwigsArch_5(OneSidedTetratwigsArch):

    """0 solutions"""

    holes = set(((0,2,0), (1,2,0), (2,1,0)))
