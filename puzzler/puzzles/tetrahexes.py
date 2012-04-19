#!/usr/bin/env python
# $Id$

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2012 by David J. Goodger
# License: GPL 2 (see __init__.py)

"""
Concrete tetrahex puzzles.
"""

from puzzler.puzzles.polyhexes import Tetrahexes
from puzzler.coordsys import Hexagonal2DCoordSet


class Tetrahexes4x7(Tetrahexes):

    """9 solutions"""

    height = 4
    width = 7

    def customize_piece_data(self):
        self.piece_data['P4'][-1]['rotations'] = (0, 1, 2)
        

class Tetrahexes7x7Triangle(Tetrahexes):

    """0 solutions"""

    height = 7
    width = 7

    def coordinates(self):
        for y in range(self.height):
            for x in range(self.width):
                if x + y < self.height:
                    yield (x, y)


class TetrahexesElongatedHexagon9x2(Tetrahexes):

    """
    2 solutions

    = 3x10 parallelogram with clipped corners (the old name)
    """

    width = 10
    height = 3

    def coordinates(self):
        return self.coordinates_elongated_hexagon(9, 2)

    def customize_piece_data(self):
        self.piece_data['P4'][-1]['flips'] = None
        self.piece_data['P4'][-1]['rotations'] = (0, 1, 2)


class TetrahexesCoin(Tetrahexes):

    """4 solutions"""

    height = 5
    width = 7

    def coordinates(self):
        max = self.width + self.height - 3
        for y in range(self.height):
            for x in range(self.width):
                if (x + y > 1) and (x + y < max) and not (x == 3 and y == 2):
                    yield (x, y)

    def customize_piece_data(self):
        self.piece_data['P4'][-1]['flips'] = None
        self.piece_data['P4'][-1]['rotations'] = (0, 1, 2)


class TetrahexesHexagon_x1(Tetrahexes):

    """0 solutions"""

    width = 7
    height = 7

    def coordinates(self):
        coords = (
            set(self.coordinates_hexagon(4))
            - set(self.coordinates_parallelogram(3, 3, offset=(2,2))))
        return sorted(coords)


class TetrahexesTwoDiamonds1(Tetrahexes):

    """2 solutions"""

    width = 11
    height = 6

    svg_rotation = -30

    def coordinates(self):
        d = Hexagonal2DCoordSet(self.coordinates_parallelogram(4, 4))
        d = d.rotate(5, (3,0))
        coords = set(list(d.translate((0, 2))) + list(d.translate((4, 0))))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P4'][-1]['flips'] = None
        self.piece_data['P4'][-1]['rotations'] = (0, 1, 2)


class TetrahexesTwoDiamonds2(Tetrahexes):

    """11 solutions"""

    width = 7
    height = 6

    svg_rotation = -30

    def coordinates(self):
        d = Hexagonal2DCoordSet(self.coordinates_parallelogram(4, 4))
        d = d.rotate(5, (3,0))
        coords = set(list(d) + list(d.translate((0, 2))))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P4'][-1]['flips'] = None
        self.piece_data['P4'][-1]['rotations'] = (0, 1, 2)


class TetrahexesTwoDiamonds_x1(Tetrahexes):

    """0 solutions"""

    width = 7
    height = 7

    holes = set(((0,4), (0,5), (1,4), (3,2), (3,3), (3,4), (5,2), (6,1), (6,2)))

    holes = set(((0,4), (0,5), (1,4), (3,1), (3,3), (3,5), (5,2), (6,1), (6,2)))

    def coordinates(self):
        coords = set(self.coordinates_hexagon(4)) - self.holes
        return sorted(coords)


class TetrahexesRosettes_x1(Tetrahexes):

    """0 solutions"""

    width = 7
    height = 7

    def coordinates(self):
        coords = set(
            list(self.coordinates_hexagon(2, offset=(0,2)))
            + list(self.coordinates_hexagon(2, offset=(1,4)))
            + list(self.coordinates_hexagon(2, offset=(3,0)))
            + list(self.coordinates_hexagon(2, offset=(4,2))))
        return sorted(coords)


class TetrahexesTrefoil_x1(Tetrahexes):

    """0 solutions"""

    width = 7
    height = 7

    def coordinates(self):
        t = Hexagonal2DCoordSet(self.coordinates_triangle(2))
        coords = (
            set(self.coordinates_hexagon(4))
            - set(t.translate((0,4)))
            - set(t.translate((4,0)))
            - set(t.translate((4,4))))
        return sorted(coords)


class TetrahexesTrefoil_x2(Tetrahexes):

    """0 solutions"""

    width = 8
    height = 8

    def coordinates(self):
        coords = set(
            list(self.coordinates_hexagon(2, offset=(0,5)))
            + list(self.coordinates_hexagon(2, offset=(3,3)))
            + list(self.coordinates_hexagon(2, offset=(4,0)))
            + list(self.coordinates_hexagon(2, offset=(5,4))))
        return sorted(coords)


class TetrahexesTrefoil_x3(Tetrahexes):

    """0 solutions"""

    width = 7
    height = 7

    def coordinates(self):
        t = Hexagonal2DCoordSet(self.coordinates_triangle(2))
        coords = (
            set(self.coordinates_hexagon(4))
            - set(t.translate((0,3)))
            - set(t.translate((5,0)))
            - set(t.translate((3,5))))
        return sorted(coords)


class TetrahexesTrefoil_x4(Tetrahexes):

    """0 solutions"""

    width = 7
    height = 7

    def coordinates(self):
        t = Hexagonal2DCoordSet(self.coordinates_triangle(2))
        coords = (
            set(self.coordinates_hexagon(4))
            - set(t.translate((1,5)))
            - set(t.translate((2,1)))
            - set(t.translate((5,2))))
        return sorted(coords)


class TetrahexesFlower1(Tetrahexes):

    """4 solutions"""

    width = 7
    height = 7

    holes = set(((0,3), (0,6), (3,0), (3,6), (6,0), (6,3), (2,2), (2,5), (5,2)))

    def coordinates(self):
        coords = set(self.coordinates_hexagon(4)) - self.holes
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P4'][-1]['rotations'] = (0, 1)


class TetrahexesBumpyTriangle(Tetrahexes):

    """1 solution"""

    height = 7
    width = 7

    svg_rotation = 30

    def coordinates(self):
        coords = set(
            list(self.coordinates_hexagon(3, offset=(1,1)))
            + list(self.coordinates_hexagon(2, offset=(0,4)))
            + list(self.coordinates_hexagon(2, offset=(2,0)))
            + list(self.coordinates_hexagon(2, offset=(4,2))))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P4'][-1]['flips'] = None
        self.piece_data['P4'][-1]['rotations'] = (0, 1)


class TetrahexesStaggeredRectangle7x4(Tetrahexes):

    """23 solutions"""

    height = 7
    width = 7

    svg_rotation = -30

    def coordinates(self):
        return self.coordinates_staggered_rectangle(7, 4)

    def customize_piece_data(self):
        self.piece_data['P4'][-1]['flips'] = None
