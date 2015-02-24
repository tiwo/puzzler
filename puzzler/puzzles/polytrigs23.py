#!/usr/bin/env python
# -*- coding: utf-8 -*-
# $Id$

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2015 by David J. Goodger
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


class Polytrigs23ThreeCongruent1(Polytrigs23ThreeCongruent):

    """
    4 solutions::

           ______
          /\    /\
         /  \  /  \
        /____\/____\______
        \    /\    /
         \  /  \  /
          \/____\/_____
    """

    width = 12
    height = 3

    extras = set(((2,0,0), (2,1,0)))

    shape_pitch = 4

    def coordinates_shape(self):
        s = TriangularGrid3DCoordSet(
            list(self.coordinates_hexagon(1))
            + [self.coordinate_offset(x, y, z, None)
               for x, y, z in self.extras])
        return s


class Polytrigs23ThreeCongruent1Combined1(Polytrigs23ThreeCongruent1):

    """8 solutions"""

    width = 6
    height = 6

    offsets = ((0,3,0), None, (5,0,0), None, (3,5,0))

    def coordinates(self):
        s = self.coordinates_shape()
        coords = set()
        self.shapes = []
        for i, offset in enumerate(self.offsets):
            if not offset:
                continue
            shape = s.rotate0(i).translate(offset)
            coords.update(shape)
            self.shapes.append(shape)
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P3'][-1]['rotations'] = (0, 1)

    def build_matrix(self):
        pieces = sorted(
            polytrigs.DitrigsData.piece_data.keys()
            + polytrigs.TritrigsData.piece_data.keys())
        for shape in self.shapes:
            self.build_regular_matrix(pieces, shape)


class Polytrigs23ThreeCongruent1Combined2(Polytrigs23ThreeCongruent1Combined1):

    """8 solutions"""

    offsets = ((0,3,0), None, (6,0,0), None, (3,6,0))


class Polytrigs23ThreeCongruent1Combined3(Polytrigs23ThreeCongruent1Combined1):

    """8 solutions"""

    width = 7
    height = 7

    offsets = ((0,3,0), None, (7,0,0), None, (3,7,0))


class Polytrigs23ThreeCongruent1Combined4(Polytrigs23ThreeCongruent1Combined3):

    """8 solutions"""

    offsets = ((0,2,0), None, (6,0,0), None, (2,6,0))


class Polytrigs23ThreeCongruent_x1(Polytrigs23ThreeCongruent):

    """
    0 solutions (impossible: I3)::

             /\
            /  \
           /____\
          /\    /\
         /  \  /  \
        /____\/____\
        \    /\
         \  /  \
          \/____\
           \
            \
             \
    """

    width = 9
    height = 4

    holes = set(((2,0,1), (2,1,1)))

    def coordinates_shape(self):
        s = TriangularGrid3DCoordSet(
            list(self.coordinates_triangle(2, offset=(0,2,0)))
            + list(self.coordinates_inverted_triangle(2)))
        s -= self.holes
        return s


class Polytrigs23ThreeCongruent_x2(Polytrigs23ThreeCongruent):

    """
    0 solutions::

              ______
             /\    /
            /  \  /
           /____\/_____
          /\    /\
         /  \  /  \
        /____\/____\
        \    /
         \  /
          \/
    """

    width = 9
    height = 4

    holes = set(((0,0,0), (0,0,1), (2,1,1)))

    def coordinates_shape(self):
        s = TriangularGrid3DCoordSet(
            list(self.coordinates_bordered(1, 3))
            + list(self.coordinates_bordered(1, 1, offset=(1,1,0))))
        s -= self.holes
        return s


class Polytrigs23ThreeCongruent_x3(Polytrigs23ThreeCongruent):

    """
    0 solutions (impossible: I3)::

              ______
             /\
            /  \
           /____\
          /\    /\
         /  \  /  \
        /____\/____\
        \    /\
         \  /  \
          \/____\
    """

    width = 9
    height = 4

    holes = set(((1,2,1), (2,0,1)))

    def coordinates_shape(self):
        s = TriangularGrid3DCoordSet(
            list(self.coordinates_hexagon(1))
            + list(self.coordinates_bordered(1, 1, offset=(0,2,0))))
        s -= self.holes
        return s


class Polytrigs23ThreeCongruent_x4(Polytrigs23ThreeCongruent):

    """
    0 solutions (impossible: I3)::

              ______
             /\    /\
            /  \  /  \
           /____\/____\
          /\    /\
         /  \  /  \
        /____\/____\
        \
         \
          \
    """

    width = 9
    height = 4

    def coordinates_shape(self):
        s = TriangularGrid3DCoordSet(
            list(self.coordinates_triangle(2, offset=(0,1,0)))
            + list(self.coordinates_trapezoid(2, 1, offset=(0,2,0)))
            + [self.coordinate_offset(1, 0, 2, None)])
        return s


class Polytrigs23ThreeCongruent_x5(Polytrigs23ThreeCongruent):

    """
    0 solutions::

                /\
               /  \
              /____\
             /\    /
            /  \  /
           /____\/_____
          /\    /\
         /  \  /  \
        /____\/____\
    """

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

    """
    0 solutions::

                /\    /
               /  \  /
              /____\/
             /\    /
            /  \  /
           /____\/
          /\    /\
         /  \  /  \
        /____\/____\
    """

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

    """
    0 solutions::

                /
               /
              /_____
             /\    /
            /  \  /
           /____\/_____
          /\    /\    /
         /  \  /  \  /
        /____\/____\/
    """

    width = 9
    height = 3

    def coordinates_shape(self):
        s = TriangularGrid3DCoordSet(
            list(self.coordinates_bordered(2, 1))
            + list(self.coordinates_bordered(1, 2))
            + [self.coordinate_offset(0, 2, 1, None)])
        return s


class Polytrigs23ThreeCongruent_x8(Polytrigs23ThreeCongruent):

    """
    0 solutions::

              \    /
               \  /
           _____\/_____
           \    /\    /
            \  /  \  /
        _____\/____\/_____
             /\    /
            /  \  /
           /    \/
    """

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

    """
    0 solutions::

              \    /
               \  /
           _____\/_____
           \    /\    /
            \  /  \  /
        _____\/____\/
        \    /\    /
         \  /  \  /
          \/    \/
    """

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


class Polytrigs23ThreeCongruent_x10(Polytrigs23ThreeCongruent1):

    """
    0 solutions::

           ______
          /\    /\
         /  \  /  \
        /____\/____\______
        \    /\    /\
         \  /  \  /  \
          \/____\/    \
    """

    extras = set(((3,0,2), (2,1,0)))


class Polytrigs23ThreeCongruent_x11(Polytrigs23ThreeCongruent1):

    """
    0 solutions (impossible: I3)::

           ______
          /\    /\
         /  \  /  \
        /____\/____\
        \    /\    /\
         \  /  \  /  \
          \/____\/____\
    """

    extras = set(((2,0,0), (3,0,2)))


class Polytrigs23ThreeCongruent_x12(Polytrigs23ThreeCongruent):

    """
    0 solutions::

                 ______
                /\    /\
               /  \  /  \
        ______/____\/____\______
              \    /\    /
               \  /  \  /
                \/____\/
    """

    width = 15
    height = 3

    shape_pitch = 5

    def coordinates_shape(self):
        s = TriangularGrid3DCoordSet(
            list(self.coordinates_hexagon(1, offset=(1,0,0)))
            + list(self.coordinates_bordered(4, 0, offset=(0,1,0))))
        return s


class Polytrigs23ThreeCongruent_x13(Polytrigs23ThreeCongruent1):

    """
    0 solutions::

         \
          \
           \______
           /\    /\
          /  \  /  \
         /____\/____\______
         \    /\    /
          \  /  \  /
           \/____\/
    """

    extras = set(((0,2,2), (2,1,0)))


class Polytrigs23ThreeCongruent_x14(Polytrigs23ThreeCongruent1):

    """
    0 solutions::

                    /
                   /
            ______/
           /\    /\
          /  \  /  \
         /____\/____\______
         \    /\    /
          \  /  \  /
           \/____\/
    """

    extras = set(((1,2,1), (2,1,0)))


class Polytrigs23ThreeCongruent_x15(Polytrigs23ThreeCongruent1):

    """
    0 solutions::

           ______
          /\    /\
         /  \  /  \
        /____\/____\____________
        \    /\    /
         \  /  \  /
          \/____\/
    """

    width = 14
    height = 3

    shape_pitch = 5

    extras = set(((2,1,0), (3,1,0)))


class Polytrigs23Trefoil1(Polytrigs23ThreeCongruent1Combined1):

    """4,548 solutions"""

    build_matrix = Polytrigs23.build_matrix


class Polytrigs23Trefoil2(Polytrigs23ThreeCongruent1Combined2):

    """70 solutions"""

    build_matrix = Polytrigs23.build_matrix


class Polytrigs23Trefoil3(Polytrigs23ThreeCongruent1Combined4):

    """28 solutions"""

    build_matrix = Polytrigs23.build_matrix


class Polytrigs23Trefoil_x1(Polytrigs23ThreeCongruent1Combined1):

    """0 solutions"""

    extras = set(((2,0,0), (3,0,2)))

    offsets = ((0,1,0), None, (6,0,0), None, (1,6,0))


class Polytrigs23TriangleStack_x(Polytrigs23):

    """0 solutions"""

    width = 6
    height = 5

    def coordinates(self):
        coords = (
            set(self.coordinates_triangle_unbordered(6))
            - set(self.coordinates_inverted_triangle(1, offset=(0,4,0))))
        return sorted(coords)
