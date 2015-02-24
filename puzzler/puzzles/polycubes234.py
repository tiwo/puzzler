#!/usr/bin/env python
# $Id$

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2015 by David J. Goodger
# License: GPL 2 (see __init__.py)

"""
Concrete polycube (order 2 through 4) puzzles.
"""

from puzzler.puzzles import Puzzle3D, Puzzle2D
from puzzler.puzzles.polycubes import Polycubes234


class Polycubes234Solid(Polycubes234):

    """abstract base class: provide dimensions and `holes`."""

    def coordinates(self):
        coords = (
            set(self.coordinates_cuboid(self.width, self.height, self.depth))
            - self.holes)
        return sorted(coords)


class Polycubes234_5x4x2(Polycubes234Solid):

    """many solutions"""

    width = 5
    height = 4
    depth = 2

    transform_solution_matrix = Puzzle3D.swap_yz_transform

    holes = set()


class Polycubes234_10x2x2(Polycubes234Solid):

    """many solutions"""

    width = 10
    height = 2
    depth = 2

    transform_solution_matrix = Puzzle3D.swap_yz_transform

    holes = set()


class Polycubes234_2x5x2x2(Polycubes234):

    """many solutions"""

    width = 5
    height = 5
    depth = 2

    transform_solution_matrix = Puzzle3D.swap_yz_transform

    def coordinates(self):
        coords = set(
            list(self.coordinates_cuboid(5, 2, 2))
            + list(self.coordinates_cuboid(5, 2, 2, offset=(0,3,0))))
        return sorted(coords)


class Polycubes234AztecPyramid(Polycubes234):

    """many solutions"""

    width = 8
    height = 8
    depth = 3

    transform_solution_matrix = Puzzle3D.swap_yz_transform

    def coordinates(self):
        return self.coordinates_aztec_pyramid(3)


class Polycubes234OpenBox4x4x3(Polycubes234):

    """many solutions"""

    width = 4
    height = 4
    depth = 3

    transform_solution_matrix = Puzzle3D.swap_yz_transform

    def coordinates(self):
        return self.coordinates_open_box(self.width, self.height, self.depth)


class Polycubes234OpenBox6x4x2(Polycubes234OpenBox4x4x3):

    """many solutions"""

    width = 6
    height = 4
    depth = 2


class Polycubes234Steps4x4x4(Polycubes234):

    """many solutions"""

    width = 4
    height = 4
    depth = 4

    def coordinates(self):
        coords = set(
            self.coordinate_offset(x, y, z, None)
            for y, z in Puzzle2D.coordinates_triangle(4) for x in range(4))
        return sorted(coords)


class Polycubes234Steps10x3x2_x(Polycubes234):

    """0 solutions"""

    width = 10
    height = 3
    depth = 2

    transform_solution_matrix = Puzzle3D.swap_yz_transform

    def coordinates(self):
        coords = set(
            list(self.coordinates_cuboid(10, 3, 1))
            + list(self.coordinates_cuboid(10, 1, 1, offset=(0,1,1))))
        return sorted(coords)


class Polycubes234Steps6x5x2(Polycubes234):

    """many solutions"""

    width = 6
    height = 5
    depth = 2

    def coordinates(self):
        coords = set(
            self.coordinate_offset(x, y, z, None)
            for x, y in Puzzle2D.coordinates_triangle(6)
            for z in range(2)
            if y < 5)
        return sorted(coords)


class Polycubes234CrossTower1(Polycubes234):

    """
    many solutions

    Design by Kaito Goodger.
    """

    width = 4
    height = 4
    depth = 3

    transform_solution_matrix = Puzzle3D.swap_yz_transform

    def coordinates(self):
        coords = set(
            list(self.coordinates_cuboid(4, 2, 3, offset=(0,1,0)))
            + list(self.coordinates_cuboid(2, 4, 3, offset=(1,0,0)))
            + list(self.coordinates_cuboid(4, 4, 1)))
        return sorted(coords)


class Polycubes234CrossTower2(Polycubes234):

    """many solutions"""

    width = 4
    height = 4
    depth = 4

    transform_solution_matrix = Puzzle3D.swap_yz_transform

    def coordinates(self):
        coords = set(
            list(self.coordinates_cuboid(4, 2, 3, offset=(0,1,0)))
            + list(self.coordinates_cuboid(2, 4, 3, offset=(1,0,0)))
            + list(self.coordinates_cuboid(2, 2, 1, offset=(1,1,3))))
        return sorted(coords)


class Polycubes234CrossTower_x(Polycubes234):

    """0 solutions"""

    width = 3
    height = 3
    depth = 8

    def coordinates(self):
        coords = set(
            list(self.coordinates_cuboid(3, 1, 8, offset=(0,1,0)))
            + list(self.coordinates_cuboid(1, 3, 8, offset=(1,0,0))))
        return sorted(coords)


class Polycubes234RingWall6x6x2(Polycubes234):

    """many solutions"""

    width = 6
    height = 6
    depth = 2

    transform_solution_matrix = Puzzle3D.swap_yz_transform

    def coordinates(self):
        return self.coordinates_ring_wall(self.width, self.height, self.depth)


class Polycubes234RingWall7x5x2(Polycubes234RingWall6x6x2):

    """many solutions"""

    width = 7
    height = 5
    depth = 2


class Polycubes234RingWall8x4x2(Polycubes234RingWall6x6x2):

    """many solutions"""

    width = 8
    height = 4
    depth = 2


class Polycubes234RingWall9x3x2(Polycubes234RingWall6x6x2):

    """many solutions"""

    width = 9
    height = 3
    depth = 2


class Polycubes234RingWall4x3x4(Polycubes234RingWall6x6x2):

    """many solutions"""

    width = 4
    height = 3
    depth = 4


class Polycubes234RingWall3x3x5(Polycubes234RingWall6x6x2):

    """many solutions"""

    width = 3
    height = 3
    depth = 5


class Polycubes234Cross1(Polycubes234):

    """many solutions"""

    width = 6
    height = 6
    depth = 2

    transform_solution_matrix = Puzzle3D.swap_yz_transform

    def coordinates(self):
        coords = set(
            list(self.coordinates_cuboid(6, 2, 2, offset=(0,2,0)))
            + list(self.coordinates_cuboid(2, 6, 2, offset=(2,0,0))))
        return sorted(coords)


class Polycubes234StackedSquares1(Polycubes234):

    """many solutions"""

    width = 4
    height = 4
    depth = 4

    transform_solution_matrix = Puzzle3D.swap_yz_transform

    def coordinates(self):
        coords = set(
            list(self.coordinates_cuboid(4, 4, 2))
            + list(self.coordinates_cuboid(2, 2, 2, offset=(1,1,2))))
        return sorted(coords)


class Polycubes234Tower1(Polycubes234):

    """
    many solutions

    Design by Kaito Goodger.
    """

    width = 5
    height = 5
    depth = 4

    transform_solution_matrix = Puzzle3D.swap_yz_transform

    def coordinates(self):
        coords = set(
            list(self.coordinates_cuboid(3, 3, 4, offset=(1,1,0)))
            + list(self.coordinates_cuboid(1, 5, 1, offset=(2,0,0)))
            + list(self.coordinates_cuboid(5, 1, 1, offset=(0,2,0))))
        return sorted(coords)


class Polycubes234Tower2(Polycubes234Solid):

    """many solutions"""

    width = 3
    height = 3
    depth = 5

    holes = set(((0,0,4), (0,2,4), (1,1,4), (2,0,4), (2,2,4)))

    transform_solution_matrix = Puzzle3D.swap_yz_transform


class Polycubes234Tower3(Polycubes234Tower2):

    """many solutions"""

    holes = set(((0,1,4), (1,0,4), (1,1,4), (1,2,4), (2,1,4)))
