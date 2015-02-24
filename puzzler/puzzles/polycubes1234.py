#!/usr/bin/env python
# $Id$

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2015 by David J. Goodger
# License: GPL 2 (see __init__.py)

"""
Concrete polycube (order 1 through 4) puzzles.
"""

from puzzler.puzzles import Puzzle3D, Puzzle2D
from puzzler.puzzles.polycubes import Polycubes1234


class Polycubes1234StackedSquares1(Polycubes1234):

    """many solutions"""

    width = 5
    height = 5
    depth = 2

    transform_solution_matrix = Puzzle3D.cycle_xyz_transform

    def coordinates(self):
        coords = set(
            list(self.coordinates_cuboid(5, 5, 1))
            + list(self.coordinates_cuboid(4, 4, 1, offset=(0,0,1))))
        return sorted(coords)


class Polycubes1234StackedSquares2(Polycubes1234):

    """many solutions"""

    width = 4
    height = 4
    depth = 3

    transform_solution_matrix = Puzzle3D.cycle_xyz_transform

    def coordinates(self):
        coords = set(
            list(self.coordinates_cuboid(4, 4, 2))
            + list(self.coordinates_cuboid(3, 3, 1, offset=(0,0,2))))
        return sorted(coords)


class Polycubes1234Solid(Polycubes1234):

    """abstract base class: provide dimensions and `holes`."""

    def coordinates(self):
        coords = (
            set(self.coordinates_cuboid(self.width, self.height, self.depth))
            - self.holes)
        return sorted(coords)


class Polycubes1234_7x3x2_1(Polycubes1234Solid):

    """many solutions"""

    width = 7
    height = 3
    depth = 2

    holes = set(((3,1,1),))

    transform_solution_matrix = Puzzle3D.swap_yz_transform


class Polycubes1234_3x3x5_1(Polycubes1234Solid):

    """many solutions"""

    width = 3
    height = 3
    depth = 5

    holes = set(((0,0,4), (0,2,4), (2,0,4), (2,2,4)))

    transform_solution_matrix = Puzzle3D.swap_yz_transform


class Polycubes1234_3x3x5_2(Polycubes1234_3x3x5_1):

    """many solutions"""

    holes = set(((0,1,4), (1,0,4), (1,2,4), (2,1,4)))


class Polycubes1234OpenBox3x3x5(Polycubes1234):

    """many solutions"""

    width = 3
    height = 3
    depth = 5

    transform_solution_matrix = Puzzle3D.swap_yz_transform

    def coordinates(self):
        return self.coordinates_open_box(self.width, self.height, self.depth)


class Polycubes1234OpenBox5x5x2(Polycubes1234OpenBox3x3x5):

    """many solutions"""

    width = 5
    height = 5
    depth = 2


class Polycubes1234DiamondMound_x(Polycubes1234Solid):

    """0 solutions: excessive parity imbalance"""

    width = 7
    height = 7
    depth = 3

    transform_solution_matrix = Puzzle3D.swap_yz_transform

    def coordinates(self):
        coords = set(self.coordinates_cuboid(3, 1, 1, offset=(2,3,2)))
        for z in range(2):
            coords.update(
                set((self.coordinate_offset(x, y, z, None)
                     for (x, y) in
                     Puzzle2D.coordinates_diamond(4 - z, offset=(z,z)))))
        return sorted(coords)


class Polycubes1234DiamondCheckerboard_x(Polycubes1234Solid):

    """0 solutions: excessive parity imbalance"""

    width = 7
    height = 7
    depth = 2

    transform_solution_matrix = Puzzle3D.swap_yz_transform

    def coordinates(self):
        diamond = list(Puzzle2D.coordinates_diamond(4))
        coords = set(
            self.coordinate_offset(x, y, 0, None) for (x, y) in diamond)
        coords.update(
            set(self.coordinate_offset(x, y, 1, None) for (x, y) in diamond
                if ((x + y) % 2)))
        return sorted(coords)


class Polycubes1234CrossTower1(Polycubes1234):

    """0 solutions"""

    width = 5
    height = 5
    depth = 5

    transform_solution_matrix = Puzzle3D.swap_yz_transform

    def coordinates(self):
        coords = set(
            list(self.coordinates_cuboid(3, 5, 1, offset=(1,0,0)))
            + list(self.coordinates_cuboid(5, 3, 1, offset=(0,1,0)))
            + list(self.coordinates_cuboid(3, 1, 4, offset=(1,2,1)))
            + list(self.coordinates_cuboid(1, 3, 4, offset=(2,1,1))))
        return sorted(coords)
