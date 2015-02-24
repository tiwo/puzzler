#!/usr/bin/env python
# -*- coding: utf-8 -*-
# $Id$

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2015 by David J. Goodger
# License: GPL 2 (see __init__.py)

"""
Concrete quasi-polytrigs (order 1-3) puzzles.
"""

from puzzler.puzzles.polytwigs import (
    QuasiPolytwigs123, OneSidedQuasiPolytwigs123)


class QuasiPolytwigs123RoundedRectangle9x2(QuasiPolytwigs123):

    """many solutions"""

    width = 10
    height = 6

    svg_rotation = 0

    def coordinates(self):
        return self.coordinates_rounded_rectangle(9, 2)

    def customize_piece_data(self):
        self.piece_data['P13'][-1]['flips'] = None
        self.piece_data['P13'][-1]['rotations'] = (0, 1, 2)


class QuasiPolytwigs123HexagonRing1(QuasiPolytwigs123):

    """many solutions"""

    width = 6
    height = 6

    holes = set(((1,2,1), (4,2,1)))

    def coordinates(self):
        coords = (
            set(self.coordinates_hexagon(3))
            - set(self.coordinates_hexagon_unbordered(2, offset=(1,1,0)))
            - self.holes)
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P13'][-1]['flips'] = None
        self.piece_data['P13'][-1]['rotations'] = (0, 1, 2)


class QuasiPolytwigs123HexagonRing2(QuasiPolytwigs123HexagonRing1):

    """many solutions"""

    holes = set(((1,4,1), (2,4,1)))

    def customize_piece_data(self):
        self.piece_data['P13'][-1]['flips'] = None


class QuasiPolytwigs123HexagonRing3(QuasiPolytwigs123HexagonRing2):

    """many solutions"""

    holes = set(((1,4,0), (2,4,2)))

    def customize_piece_data(self):
        self.piece_data['P13'][-1]['flips'] = None


class QuasiPolytwigs123HexagonRing4(QuasiPolytwigs123HexagonRing1):

    """many solutions"""

    holes = set(((2,4,1), (3,4,2)))

    svg_rotation = 0

    def customize_piece_data(self):
        self.piece_data['P13'][-1]['flips'] = None


class QuasiPolytwigs123_5x3ParallelogramRing(QuasiPolytwigs123):

    """many solutions"""

    width = 6
    height = 4

    def coordinates(self):
        coords = (
            set(self.coordinates_bordered(5, 3))
            - set(self.coordinates_unbordered(3, 1, offset=(1,1,0))))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P13'][-1]['rotations'] = (0, 1, 2)


class QuasiPolytwigs123_6x3TrapezoidRing(QuasiPolytwigs123):

    """many solutions"""

    width = 7
    height = 4

    def coordinates(self):
        coords = (
            set(self.coordinates_trapezoid(6, 3))
            - set(self.coordinates_trapezoid_unbordered(3, 1, offset=(1,1,0))))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P13'][-1]['flips'] = None
