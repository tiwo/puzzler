#!/usr/bin/env python
# -*- coding: utf-8 -*-
# $Id$

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2012 by David J. Goodger
# License: GPL 2 (see __init__.py)

"""
Concrete quasi-tritwig puzzles.
"""

from puzzler.puzzles.polytwigs import QuasiTritwigs, OneSidedQuasiTritwigs


class QuasiTritwigs10x1(QuasiTritwigs):

    """many solutions"""

    height = 2
    width = 11

    def coordinates(self):
        return self.coordinates_bordered(10, 1)

    def customize_piece_data(self):
        self.piece_data['P13'][-1]['flips'] = None
        self.piece_data['P13'][-1]['rotations'] = (0, 1, 2)


class QuasiTritwigs6x2(QuasiTritwigs):

    """many solutions"""

    height = 3
    width = 7

    def coordinates(self):
        return self.coordinates_bordered(6, 2)

    def customize_piece_data(self):
        self.piece_data['P13'][-1]['flips'] = None
        self.piece_data['P13'][-1]['rotations'] = (0, 1, 2)


class QuasiTritwigsTriangle1(QuasiTritwigs):

    """many solutions"""

    width = 6
    height = 6

    def coordinates(self):
        coords = (
            set(self.coordinates_triangle(5))
            - set(self.coordinates_triangle_unbordered(3, offset=(1,0,0))))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P13'][-1]['flips'] = None


class QuasiTritwigsTriangle2(QuasiTritwigsTriangle1):

    """many solutions"""

    def coordinates(self):
        coords = (
            set(self.coordinates_triangle(5))
            - set(self.coordinates_inverted_triangle_unbordered(3)))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P13'][-1]['flips'] = None
        self.piece_data['P13'][-1]['rotations'] = (0, 1)


class QuasiTritwigsTriangle3(QuasiTritwigsTriangle2):

    """many solutions"""

    def coordinates(self):
        coords = (
            set(self.coordinates_triangle(5))
            - set(self.coordinates_triangle_unbordered(2))
            - set(self.coordinates_triangle_unbordered(2, offset=(3,0,0)))
            - set(self.coordinates_triangle_unbordered(2, offset=(0,3,0))))
        return sorted(coords)


class QuasiTritwigsTriangle4(QuasiTritwigsTriangle1):

    """many solutions"""

    def coordinates(self):
        coords = (
            set(self.coordinates_triangle(5))
            - set(self.coordinates_triangle_unbordered(3, offset=(0,2,0))))
        return sorted(coords)


class QuasiTritwigsSnowflake1(QuasiTritwigs):

    """many solutions"""

    width = 6
    height = 6

    holes = set(((2,2,2), (2,3,1), (3,2,0)))

    def coordinates(self):
        coords = set(self.coordinates_hexagram(2)) - self.holes
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P13'][-1]['flips'] = None
        self.piece_data['P13'][-1]['rotations'] = (0, 1)


class QuasiTritwigsSnowflake2(QuasiTritwigsSnowflake1):

    """many solutions"""

    holes = set(((2,2,0), (2,3,2), (3,2,1)))


class QuasiTritwigsSnowflake3(QuasiTritwigsSnowflake1):

    """many solutions"""

    holes = set((
        (1,2,1), (1,4,2), (2,1,0), (2,2,1), (2,3,0), (2,4,0), (3,2,2),
        (4,1,2), (4,2,1)))

    hex_offsets = ((0,2,0), (0,4,0), (2,0,0), (2,4,0), (4,0,0), (4,2,0))

    def coordinates(self):
        coords = set(self.coordinates_hexagon(2, offset=(1,1,0)))
        for offset in self.hex_offsets:
            for coord in self.coordinates_bordered(1, 1, offset=offset):
                coords.add(coord)
        coords -= self.holes
        return sorted(coords)


class QuasiTritwigsElongatedHexagon2x3_1(QuasiTritwigs):

    """many solutions"""

    width = 5
    height = 6

    holes = set(((1,2,1), (1,4,1), (3,0,1), (3,2,1)))

    def coordinates(self):
        coords = set(self.coordinates_elongated_hexagon(2, 3)) - self.holes
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P13'][-1]['flips'] = None
        self.piece_data['P13'][-1]['rotations'] = (0, 1, 2)


class QuasiTritwigsElongatedHexagon2x3_2(QuasiTritwigsElongatedHexagon2x3_1):

    """many solutions"""

    holes = set(((1,3,1), (2,1,1), (2,3,1), (3,1,1)))


class QuasiTritwigsElongatedHexagon2x3_3(QuasiTritwigsElongatedHexagon2x3_1):

    """many solutions"""

    holes = set(((0,3,0), (1,2,2), (3,2,0), (3,3,2)))


class QuasiTritwigsElongatedHexagon2x3_4(QuasiTritwigsElongatedHexagon2x3_1):

    """many solutions"""

    holes = set(((1,3,0), (2,2,2), (2,2,0), (2,3,2)))


class QuasiTritwigsElongatedHexagon2x3_5(QuasiTritwigsElongatedHexagon2x3_1):

    """many solutions"""

    holes = set(((0,4,0), (2,1,2), (2,4,2), (3,1,0)))


class QuasiTritwigsElongatedHexagon2x3_6(QuasiTritwigsElongatedHexagon2x3_1):

    """many solutions"""

    holes = set(((1,2,0), (1,3,2), (2,3,0), (3,2,2)))


class QuasiTritwigsTrefoil1(QuasiTritwigs):

    """many solutions"""

    width = 8
    height = 8

    def coordinates(self):
        coords = set(
            list(self.coordinates_bordered(4, 1, offset=(0,3,0)))
            + list(self.coordinates_bordered(1, 4, offset=(3,3,0)))
            + list(self.coordinates_bordered(1, 1, offset=(4,2,0)))
            + list(self.coordinates_bordered(1, 1, offset=(5,1,0)))
            + list(self.coordinates_bordered(1, 1, offset=(6,0,0))))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P13'][-1]['flips'] = None
        self.piece_data['P13'][-1]['rotations'] = (0, 1)


class QuasiTritwigsTrefoil2(QuasiTritwigsTrefoil1):

    """many solutions"""

    width = 7
    height = 7

    def coordinates(self):
        coords = set(
            list(self.coordinates_bordered(1, 3, offset=(1,0,0)))
            + list(self.coordinates_bordered(3, 1, offset=(3,1,0)))
            + list(self.coordinates_bordered(1, 2, offset=(2,2,0)))
            + list(self.coordinates_bordered(1, 1, offset=(0,5,0)))
            + list(self.coordinates_bordered(1, 1, offset=(1,4,0))))
        return sorted(coords)


class QuasiTritwigsTrefoil3(QuasiTritwigsTrefoil1):

    """many solutions"""

    width = 6
    height = 6

    def coordinates(self):
        coords = set(
            list(self.coordinates_bordered(1, 2, offset=(0,2,0)))
            + list(self.coordinates_bordered(1, 2, offset=(2,1,0)))
            + list(self.coordinates_bordered(1, 2, offset=(3,2,0)))
            + list(self.coordinates_bordered(2, 1, offset=(3,0,0)))
            + list(self.coordinates_bordered(1, 1, offset=(1,3,0)))
            + list(self.coordinates_bordered(1, 1, offset=(2,4,0))))
        return sorted(coords)


class QuasiTritwigsTrefoil4(QuasiTritwigsTrefoil1):

    """many solutions"""

    width = 6
    height = 6

    def coordinates(self):
        coords = (
            set(list(self.coordinates_triangle(2))
                + list(self.coordinates_triangle(2, offset=(0,3,0)))
                + list(self.coordinates_triangle(2, offset=(1,1,0)))
                + list(self.coordinates_triangle(2, offset=(3,0,0))))
            - set(self.coordinates_triangle_unbordered(2, offset=(1,1,0))))
        return sorted(coords)


class QuasiTritwigsTrefoil5(QuasiTritwigsTrefoil1):

    """many solutions"""

    width = 6
    height = 6

    def coordinates(self):
        coords = (
            set(list(self.coordinates_triangle(2, offset=(0,3,0)))
                + list(self.coordinates_triangle(2, offset=(2,2,0)))
                + list(self.coordinates_triangle(2, offset=(3,0,0)))
                + list(self.coordinates_triangle(2, offset=(3,3,0))))
            - set(self.coordinates_triangle_unbordered(2, offset=(2,2,0))))
        return sorted(coords)


class QuasiTritwigsTrefoil6(QuasiTritwigsTrefoil1):

    """many solutions"""

    width = 6
    height = 6

    def coordinates(self):
        coords = set(
            list(self.coordinates_bordered(2, 1, offset=(0,3,0)))
            + list(self.coordinates_bordered(1, 1, offset=(1,4,0)))
            + list(self.coordinates_bordered(2, 1, offset=(1,1,0)))
            + list(self.coordinates_bordered(2, 1, offset=(2,2,0)))
            + list(self.coordinates_bordered(1, 1, offset=(3,0,0)))
            + list(self.coordinates_bordered(1, 1, offset=(3,3,0)))
            + list(self.coordinates_bordered(1, 1, offset=(4,1,0))))
        return sorted(coords)


class QuasiTritwigsTrefoil7(QuasiTritwigsTrefoil1):

    """many solutions"""

    width = 7
    height = 7

    def coordinates(self):
        coords = set(
            list(self.coordinates_bordered(1, 2, offset=(0,1,0)))
            + list(self.coordinates_bordered(2, 1, offset=(1,2,0)))
            + list(self.coordinates_bordered(1, 1, offset=(1,5,0)))
            + list(self.coordinates_bordered(1, 2, offset=(2,3,0)))
            + list(self.coordinates_bordered(1, 1, offset=(3,1,0)))
            + list(self.coordinates_bordered(2, 1, offset=(4,0,0))))
        return sorted(coords)


class QuasiTritwigsTrefoil8(QuasiTritwigsTrefoil1):

    """many solutions"""

    width = 7
    height = 7

    def coordinates(self):
        coords = set(
            list(self.coordinates_bordered(1, 2, offset=(0,2,0)))
            + list(self.coordinates_bordered(1, 1, offset=(1,3,0)))
            + list(self.coordinates_bordered(1, 1, offset=(2,5,0)))
            + list(self.coordinates_bordered(1, 2, offset=(3,3,0)))
            + list(self.coordinates_bordered(1, 1, offset=(3,1,0)))
            + list(self.coordinates_bordered(2, 1, offset=(4,0,0)))
            + list(self.coordinates_triangle_unbordered(2, offset=(2,2,0))))
        return sorted(coords)
