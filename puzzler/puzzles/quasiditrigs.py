#!/usr/bin/env python
# -*- coding: utf-8 -*-
# $Id$

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2012 by David J. Goodger
# License: GPL 2 (see __init__.py)

"""
Concrete quasi-ditrig puzzles.
"""

from puzzler.puzzles.polytrigs import QuasiDitrigs, OneSidedQuasiDitrigs


class QuasiDitrigsTriangle(QuasiDitrigs):

    """
    266 solutions

    Discovered by Colin F. Brown
    """

    height = 3
    width = 4

    def coordinates(self):
        return self.coordinates_triangle(3)

    def customize_piece_data(self):
        self.piece_data['P12'][-1]['flips'] = None
        self.piece_data['P12'][-1]['rotations'] = (0, 1)


class QuasiDitrigsTriangleStack(QuasiDitrigs):

    """63 solutions"""

    height = 4
    width = 4

    def coordinates(self):
        return self.coordinates_triangle_unbordered(4)

    def customize_piece_data(self):
        self.piece_data['P12'][-1]['flips'] = None
        self.piece_data['P12'][-1]['rotations'] = (0, 1)


class QuasiDitrigsTwoTriangles1(QuasiDitrigs):

    """
    8 solutions

    Discovered by Colin F. Brown (as "diabolo")
    """

    height = 5
    width = 5

    svg_rotation = 90

    def coordinates(self):
        return self.coordinates_butterfly(2, 2)

    def customize_piece_data(self):
        self.piece_data['P12'][-1]['flips'] = None
        self.piece_data['P12'][-1]['rotations'] = (0, 1, 2)


class QuasiDitrigsTwoTriangles2(QuasiDitrigs):

    """48 solutions"""

    width = 5
    height = 2

    def coordinates(self):
        coords = set(
            list(self.coordinates_triangle(2))
            + list(self.coordinates_triangle(2, offset=(2,0,0))))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P12'][-1]['flips'] = None


class QuasiDitrigsTwoTriangles3(QuasiDitrigs):

    """7 solutions"""

    width = 4
    height = 3

    def coordinates(self):
        coords = set(
            list(self.coordinates_triangle(2))
            + list(self.coordinates_inverted_triangle(2, offset=(1,0,0))))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P12'][-1]['rotations'] = (0, 1, 2)


class QuasiDitrigsHexagram(QuasiDitrigs):

    """0 solutions"""

    width = 5
    height = 4

    def coordinates(self):
        coords = (
            set(self.coordinates_hexagram(1))
            - set(self.coordinates_hexagon_unbordered(1, offset=(1,1,0))))
        return sorted(coords)

    """
    Also 0 solutions:
    
        coords = (
            set(self.coordinates_hexagram(1))
            - (set(self.coordinates_hexagon(1, offset=(1,1,0)))
               - set(self.coordinates_hexagon_unbordered(1, offset=(1,1,0)))))
    """


class QuasiDitrigsStarburst(QuasiDitrigs):

    """
    298 solutions

    Discovered by Colin F. Brown
    """

    width = 5
    height = 4

    hex_offset = (1,1,0)
    extras = ((0,2,0), (1,3,2), (2,0,1), (2,3,1), (3,2,0), (4,0,2))

    def coordinates(self):
        coords = set(self.coordinates_hexagon(1, offset = self.hex_offset))
        for (x, y, z) in self.extras:
            coords.add(self.coordinate_offset(x, y, z, None))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P12'][-1]['flips'] = None
        self.piece_data['P12'][-1]['rotations'] = None


class QuasiDitrigsSatellite(QuasiDitrigsStarburst):

    """
    24 solutions

    Discovered by Colin F. Brown
    """

    width = 7
    height = 6

    hex_offset = (2,2,0)
    extras = ((0,3,0), (1,3,0), (5,1,2), (6,0,2), (3,4,1), (3,5,1), )

    def customize_piece_data(self):
        self.piece_data['P12'][-1]['flips'] = None
        self.piece_data['P12'][-1]['rotations'] = (0, 1)
