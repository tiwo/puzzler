#!/usr/bin/env python
# -*- coding: utf-8 -*-
# $Id$

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2012 by David J. Goodger
# License: GPL 2 (see __init__.py)

"""
Concrete polytwig (orders 4 & 5) puzzles.
"""

from puzzler.puzzles import polytwigs
from puzzler.puzzles.polytwigs import Polytwigs45, OneSidedPolytwigs45
from puzzler.coordsys import HexagonalGrid3DCoordSet, HexagonalGrid3D


class Polytwigs45Triangle1(Polytwigs45):

    """many solutions"""

    width = 7
    height = 7

    holes = set(((1,3,0), (2,2,0), (2,2,1), (2,2,2), (2,3,2)))

    def coordinates(self):
        coords = set(self.coordinates_triangle(6)) - self.holes
        return sorted(coords)
            
    def customize_piece_data(self):
        self.piece_data['R5'][-1]['rotations'] = (0, 1, 2)
        self.piece_data['R5'][-1]['flips'] = None


class Polytwigs45DiamondRing(Polytwigs45):

    """many solutions"""

    width = 6
    height = 6

    holes = set(((1,1,2), (4,4,2)))

    svg_rotation = 60

    def coordinates(self):
        coords = (
            set(self.coordinates_bordered(5, 5))
            - set(self.coordinates_unbordered(3, 3, offset=(1,1,0)))
            - self.holes)
        return sorted(coords)
            
    def customize_piece_data(self):
        self.piece_data['R5'][-1]['rotations'] = (0, 1, 2)
        self.piece_data['R5'][-1]['flips'] = None


class Polytwigs45ElongatedHexagon4x3Ring(Polytwigs45):

    """many solutions"""

    width = 7
    height = 6

    def coordinates(self):
        coords = (
            set(self.coordinates_elongated_hexagon(4, 3))
            - set(self.coordinates_butterfly_unbordered(3, 2, offset=(1,1,0))))
        return sorted(coords)
            
    def customize_piece_data(self):
        self.piece_data['R5'][-1]['rotations'] = (0, 1, 2)
        self.piece_data['R5'][-1]['flips'] = None


class Polytwigs45Butterfly5x3Ring(Polytwigs45):

    """many solutions"""

    width = 8
    height = 6

    def coordinates(self):
        coords = (
            set(self.coordinates_butterfly(5, 3))
            - set(self.coordinates_butterfly_unbordered(2, 2, offset=(2,1,0))))
        return sorted(coords)
            
    def customize_piece_data(self):
        self.piece_data['R5'][-1]['rotations'] = (0, 1, 2)
        self.piece_data['R5'][-1]['flips'] = None


class Polytwigs45InsetRectangle5x5Ring(Polytwigs45):

    """many solutions"""

    width = 6
    height = 8

    svg_rotation = 0

    def coordinates(self):
        coords = (
            set(self.coordinates_inset_rectangle(5, 5))
            - set(self.coordinates_hexagon_unbordered(2, offset=(1,2,0))))
        return sorted(coords)
            
    def customize_piece_data(self):
        self.piece_data['R5'][-1]['rotations'] = (0, 1, 2)
        self.piece_data['R5'][-1]['flips'] = None


class Polytwigs45FourCongruent1(Polytwigs45):

    """19 solutions (but no overall symmetrical shape)"""

    width = 16
    height = 11

    extras = ((0,4,0), (2,1,0), (3,0,1))

    svg_rotation = 0

    def coordinates(self):
        s = HexagonalGrid3DCoordSet(
            list(self.coordinates_bordered(1, 3, offset=(1,1,0)))
            + [self.coordinate_offset(x, y, z, None)
               for (x, y, z) in self.extras])
        coords = set()
        self.shapes = []
        for i in range(4):
            t = s.translate((i * 4, (3 - i) * 2, 0))
            coords.update(t)
            self.shapes.append(t)
        return sorted(coords)

    def build_matrix(self):
        tetratwigs = sorted(polytwigs.TetratwigsData.piece_data.keys())
        for i in range(4):
            self.build_regular_matrix([tetratwigs[i]], self.shapes[i])
        self.build_regular_matrix(
            sorted(polytwigs.PentatwigsData.piece_data.keys()))


class Polytwigs45FourCongruent2(Polytwigs45FourCongruent1):

    """38 solutions"""

    width = 15
    height = 11

    extras = ((1,1,0), (1,4,2), (2,0,1))

    def coordinates(self):
        s = HexagonalGrid3DCoordSet(
            list(self.coordinates_bordered(1, 3, offset=(0,1,0)))
            + [self.coordinate_offset(x, y, z, None)
               for (x, y, z) in self.extras])
        coords = set()
        self.shapes = []
        for i in range(4):
            t = s.translate((i * 4, (3 - i) * 2, 0))
            coords.update(t)
            self.shapes.append(t)
        return sorted(coords)


class Polytwigs45FourCongruent3(Polytwigs45FourCongruent1):

    """2 solutions"""

    width = 15
    height = 10

    extras = ((0,2,1), (0,3,2), (2,1,0), (2,1,2))

    def coordinates(self):
        s = HexagonalGrid3DCoordSet(
            list(self.coordinates_triangle(2))
            + [self.coordinate_offset(x, y, z, None)
               for (x, y, z) in self.extras])
        coords = set()
        self.shapes = []
        for i in range(4):
            t = s.translate((i * 4, (3 - i) * 2, 0))
            coords.update(t)
            self.shapes.append(t)
        return sorted(coords)


class Polytwigs45FourCongruent3Combined(Polytwigs45):

    """
    24 solutions when restricted to the unit shapes;
    many solutions if unrestricted
    """

    width = 6
    height = 6

    extras = ((0,2,1), (0,3,2), (2,1,0), (2,1,2))

    offsets = ((0,0,0), (4,0,0), None, (4,4,0), (0,4,0))

    svg_rotation = 60

    def coordinates(self):
        s = HexagonalGrid3DCoordSet(
            list(self.coordinates_triangle(2))
            + [self.coordinate_offset(x, y, z, None)
               for (x, y, z) in self.extras])
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
        self.piece_data['R5'][-1]['rotations'] = (0, 1, 2)

    def build_matrix(self):
        pieces = sorted(
            polytwigs.TetratwigsData.piece_data.keys()
            + polytwigs.PentatwigsData.piece_data.keys())
        for i in range(4):
            self.build_regular_matrix(pieces, self.shapes[i])


class Polytwigs45FourCongruent4(Polytwigs45FourCongruent3):

    """ solutions"""

    width = 15
    height = 10

    extras = ((0,2,1), (0,3,2), (1,2,2), (2,1,2))


class Polytwigs45FourCongruent_x1(Polytwigs45FourCongruent1):

    """0 solutions"""

    width = 12
    height = 8

    extras = ((1,0,0), (2,0,2), (1,2,0))

    def coordinates(self):
        s = HexagonalGrid3DCoordSet(
            list(self.coordinates_bordered(1, 3))
            + [self.coordinate_offset(x, y, z, None)
               for (x, y, z) in self.extras])
        coords = set()
        self.shapes = []
        for i in range(4):
            t = s.translate((i * 3, (3 - i) + (i <= 1), 0))
            coords.update(t)
            self.shapes.append(t)
        return sorted(coords)


class Polytwigs45FourCongruent_x2(Polytwigs45FourCongruent1):

    """0 solutions"""

    width = 8
    height = 8

    extras = ((0,3,1), (0,4,0), (0,4,2))

    def coordinates(self):
        s = HexagonalGrid3DCoordSet(
            list(self.coordinates_bordered(1, 3))
            + [self.coordinate_offset(x, y, z, None)
               for (x, y, z) in self.extras])
        coords = set()
        self.shapes = []
        for i in range(4):
            t = s.translate((i * 2, (3 - i), 0))
            coords.update(t)
            self.shapes.append(t)
        return sorted(coords)


class Polytwigs45FourCongruent_x3(Polytwigs45FourCongruent1):

    """0 solutions"""

    width = 15
    height = 9

    extras = ((0,1,1), (1,2,1), (2,2,2))

    def coordinates(self):
        s = HexagonalGrid3DCoordSet(
            list(self.coordinates_bordered(2, 1))
            + list(self.coordinates_bordered(1, 1, offset=(1,1,0)))
            + [self.coordinate_offset(x, y, z, None)
               for (x, y, z) in self.extras])
        coords = set()
        self.shapes = []
        for i in range(4):
            t = s.translate((i * 4, (3 - i) * 2, 0))
            coords.update(t)
            self.shapes.append(t)
        return sorted(coords)


class Polytwigs45FourCongruent_x4(Polytwigs45FourCongruent1):

    """0 solutions"""

    width = 15
    height = 9

    extras = ((0,0,2), (0,2,1), (1,2,2), (2,0,0))

    def coordinates(self):
        s = HexagonalGrid3DCoordSet(
            list(self.coordinates_triangle(2))
            + [self.coordinate_offset(x, y, z, None)
               for (x, y, z) in self.extras])
        coords = set()
        self.shapes = []
        for i in range(4):
            t = s.translate((i * 4, (3 - i) * 2, 0))
            coords.update(t)
            self.shapes.append(t)
        return sorted(coords)


class Polytwigs45FourCongruent_x5(Polytwigs45FourCongruent_x4):

    """0 solutions"""

    width = 15
    height = 10

    extras = ((0,0,2), (0,2,1), (0,3,2), (2,0,0))
