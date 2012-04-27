#!/usr/bin/env python
# -*- coding: utf-8 -*-
# $Id$

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2012 by David J. Goodger
# License: GPL 2 (see __init__.py)

"""
Concrete polytrig (orders 2 & 3) puzzles.
"""

from puzzler.puzzles import polytrigs
from puzzler.puzzles.polytrigs import Polytrigs23, OneSidedPolytrigs23
from puzzler.coordsys import TriangularGrid3DCoordSet


class Polytrigs23Hexagon(Polytrigs23):

    """1,118 solutions"""

    width = 5
    height = 5

    def coordinates(self):
        return self.coordinates_hexagon(2)

    def customize_piece_data(self):
        self.piece_data['P3'][-1]['flips'] = None
        self.piece_data['P3'][-1]['rotations'] = None


class Polytrigs23TriangleRing(Polytrigs23):

    """821 solutions"""

    width = 6
    height = 5

    def coordinates(self):
        coords = (
            set(self.coordinates_triangle(5))
            - set(self.coordinates_triangle_unbordered(2, offset=(1,1,0))))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P3'][-1]['flips'] = None
        self.piece_data['P3'][-1]['rotations'] = (0, 1)


class Polytrigs23ThreeCongruent(Polytrigs23):

    """abstract base class"""

    shape_pitch = 3

    def coordinates_shape(self):
        """Return a TriangularGrid3DCoordSet object; implement in subclasses."""
        raise NotImplementedError

    def coordinates(self):
        s = self.coordinates_shape()
        coords = set()
        self.shapes = []
        for i in range(3):
            t = s.translate((i * self.shape_pitch, 0, 0))
            coords.update(t)
            self.shapes.append(t)
        return sorted(coords)

    def build_matrix(self):
        ditrigs = sorted(polytrigs.DitrigsData.piece_data.keys())
        for i, ditrig in enumerate(ditrigs):
            self.build_regular_matrix([ditrig], self.shapes[i])
        self.build_regular_matrix(
            sorted(polytrigs.TritrigsData.piece_data.keys()))


class Polytrigs23ThreeCongruent_x1(Polytrigs23ThreeCongruent):

    """0 solutions"""

    width = 9
    height = 4

    holes = set(((2,0,1), (2,1,1)))

    shape_pitch = 3

    def coordinates_shape(self):
        s = TriangularGrid3DCoordSet(
            list(self.coordinates_triangle(2, offset=(0,2,0)))
            + list(self.coordinates_inverted_triangle(2)))
        s -= self.holes
        return s


class Polytrigs23ThreeCongruent_x2(Polytrigs23ThreeCongruent):

    """0 solutions"""

    width = 9
    height = 4

    holes = set(((0,0,0), (0,0,1), (2,1,1)))

    shape_pitch = 3

    def coordinates_shape(self):
        s = TriangularGrid3DCoordSet(
            list(self.coordinates_bordered(1, 3))
            + list(self.coordinates_bordered(1, 1, offset=(1,1,0))))
        s -= self.holes
        return s


class Polytrigs23ThreeCongruent_x3(Polytrigs23ThreeCongruent):

    """0 solutions"""

    width = 9
    height = 4

    holes = set(((1,2,1), (2,0,1)))

    shape_pitch = 3

    def coordinates_shape(self):
        s = TriangularGrid3DCoordSet(
            list(self.coordinates_hexagon(1))
            + list(self.coordinates_bordered(1, 1, offset=(0,2,0))))
        s -= self.holes
        return s


class Polytrigs23ThreeCongruent_x4(Polytrigs23ThreeCongruent):

    """0 solutions"""

    width = 9
    height = 4

    def coordinates_shape(self):
        s = TriangularGrid3DCoordSet(
            list(self.coordinates_triangle(2, offset=(0,1,0)))
            + list(self.coordinates_trapezoid(2, 1, offset=(0,2,0)))
            + [self.coordinate_offset(1, 0, 2, None)])
        return s


class Polytrigs23ThreeCongruent_x5(Polytrigs23ThreeCongruent):

    """0 solutions"""

    width = 9
    height = 3

    holes = set(((2,1,2),))

    def coordinates_shape(self):
        s = TriangularGrid3DCoordSet(
            list(self.coordinates_triangle(2))
            + list(self.coordinates_triangle(2, offset=(0,1,0))))
        s -= self.holes
        return s


class Polytrigs23ThreeCongruent_x6(Polytrigs23ThreeCongruent):

    """0 solutions"""

    width = 9
    height = 3

    holes = set(((0,3,0),))

    def coordinates_shape(self):
        s = TriangularGrid3DCoordSet(
            list(self.coordinates_triangle(2))
            + list(self.coordinates_bordered(1, 3)))
        s -= self.holes
        return s


class Polytrigs23ThreeCongruent_x7(Polytrigs23ThreeCongruent):

    """0 solutions"""

    width = 9
    height = 3

    def coordinates_shape(self):
        s = TriangularGrid3DCoordSet(
            list(self.coordinates_bordered(2, 1))
            + list(self.coordinates_bordered(1, 2))
            + [self.coordinate_offset(0, 2, 1, None)])
        return s


class Polytrigs23ThreeCongruent_x8(Polytrigs23ThreeCongruent):

    """0 solutions"""

    width = 11
    height = 3

    extras = ((0,1,0), (1,0,1), (1,2,1), (1,2,2), (2,1,0))

    shape_pitch = 4

    def coordinates_shape(self):
        s = TriangularGrid3DCoordSet(
            list(self.coordinates_inverted_triangle(2))
            + [self.coordinate_offset(x, y, z, None)
               for x, y, z in self.extras])
        return s


class Polytrigs23ThreeCongruent_x9(Polytrigs23ThreeCongruent):

    """0 solutions"""

    width = 9
    height = 3

    extras = ((1,2,1), (1,2,2))

    def coordinates_shape(self):
        s = TriangularGrid3DCoordSet(
            list(self.coordinates_inverted_triangle(2))
            + list(self.coordinates_inverted_triangle(1))
            + [self.coordinate_offset(x, y, z, None)
               for x, y, z in self.extras])
        return s
