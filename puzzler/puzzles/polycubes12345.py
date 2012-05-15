#!/usr/bin/env python
# $Id$

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2012 by David J. Goodger
# License: GPL 2 (see __init__.py)

"""
Concrete polycube (order 1 through 5) puzzles.
"""

from puzzler.puzzles import Puzzle3D
from puzzler.puzzles.polycubes import Polycubes12345


class Polycubes12345_2x3x31(Polycubes12345):

    """many solutions"""

    width = 31
    height = 3
    depth = 2

    transform_solution_matrix = Puzzle3D.swap_yz_transform

    def customize_piece_data(self):
        self.piece_data['P4'][-1]['rotations'] = None
        self.piece_data['P4'][-1]['flips'] = None
        self.piece_data['P4'][-1]['axes'] = None


class Polycubes12345_11x3x6_1(Polycubes12345):

    """many solutions"""

    width = 3
    height = 11
    depth = 6

    holes = ((1,3), (1,7))

    transform_solution_matrix = Puzzle3D.cycle_xyz_transform

    def coordinates(self):
        coords = set(self.coordinates_cuboid(
            self.width, self.height, self.depth))
        for x, y in self.holes:
            coords -= set(
                self.coordinates_cuboid(1, 1, self.depth, offset=(x,y,0)))
        return sorted(coords)


class Polycubes12345_11x3x6_2(Polycubes12345_11x3x6_1):

    """many solutions"""

    holes = ((0,0), (2,10))


class Polycubes12345X1(Polycubes12345):

    """many solutions"""

    width = 9
    height = 9
    depth = 6

    svg_rotation = 41.5

    def coordinates(self):
        coords = set(self.coordinates_cuboid(9, 3, 4, offset=(0,3,0)))
        coords.update(self.coordinates_cuboid(3, 9, 4, offset=(3,0,0)))
        coords.update(self.coordinates_cuboid(3, 1, 1, offset=(3,4,4)))
        coords.update(self.coordinates_cuboid(1, 3, 1, offset=(4,3,4)))
        coords.add(self.coordinate_offset(4, 4, 5, None))
        return sorted(coords)


class Polycubes12345X2(Polycubes12345):

    """many solutions"""

    width = 11
    height = 11
    depth = 6

    svg_rotation = 41.5

    def coordinates(self):
        coords = set(self.coordinates_cuboid(11, 3, 3, offset=(0,4,0)))
        coords.update(self.coordinates_cuboid(3, 11, 3, offset=(4,0,0)))
        coords.update(self.coordinates_cuboid(3, 3, 1, offset=(4,4,3)))
        coords.update(self.coordinates_cuboid(3, 1, 1, offset=(4,5,4)))
        coords.update(self.coordinates_cuboid(1, 3, 1, offset=(5,4,4)))
        coords.add(self.coordinate_offset(5, 5, 5, None))
        return sorted(coords)


class Polycubes12345X3(Polycubes12345):

    """many solutions"""

    width = 11
    height = 11
    depth = 4

    svg_rotation = 41.5

    def coordinates(self):
        coords = set(self.coordinates_cuboid(11, 3, 3, offset=(0,4,0)))
        coords.update(self.coordinates_cuboid(3, 11, 3, offset=(4,0,0)))
        coords.update(self.coordinates_cuboid(7, 1, 1, offset=(2,5,3)))
        coords.update(self.coordinates_cuboid(1, 7, 1, offset=(5,2,3)))
        coords.add(self.coordinate_offset(6, 4, 3, None))
        coords.add(self.coordinate_offset(4, 6, 3, None))
        return sorted(coords)


class Polycubes12345X4(Polycubes12345):

    """many solutions"""

    width = 11
    height = 11
    depth = 4

    svg_rotation = 41.5

    def coordinates(self):
        coords = set(self.coordinates_cuboid(11, 3, 3, offset=(0,4,0)))
        coords.update(self.coordinates_cuboid(3, 11, 3, offset=(4,0,0)))
        coords.update(self.coordinates_cuboid(4, 1, 1, offset=(6,4,3)))
        coords.update(self.coordinates_cuboid(1, 4, 1, offset=(6,1,3)))
        coords.update(self.coordinates_cuboid(4, 1, 1, offset=(1,6,3)))
        coords.update(self.coordinates_cuboid(1, 4, 1, offset=(4,6,3)))
        coords.add(self.coordinate_offset(5, 5, 3, None))
        return sorted(coords)


class Polycubes12345X5(Polycubes12345):

    """many solutions"""

    width = 11
    height = 11
    depth = 4

    svg_rotation = 41.5

    def coordinates(self):
        coords = set(self.coordinates_cuboid(11, 3, 3, offset=(0,4,0)))
        coords.update(self.coordinates_cuboid(3, 11, 3, offset=(4,0,0)))
        coords.update(self.coordinates_cuboid(7, 1, 1, offset=(2,5,3)))
        coords.update(self.coordinates_cuboid(1, 7, 1, offset=(5,2,3)))
        coords.add(self.coordinate_offset(1, 4, 3, None))
        coords.add(self.coordinate_offset(9, 6, 3, None))
        return sorted(coords)


class Polycubes12345CubeCluster(Polycubes12345):

    """many solutions"""

    width = 9
    height = 9
    depth = 9

    def coordinates(self):
        coords = set(
            list(self.coordinates_cuboid(3, 3, 9, offset=(3,3,0)))
            + list(self.coordinates_cuboid(3, 9, 3, offset=(3,0,3)))
            + list(self.coordinates_cuboid(9, 3, 3, offset=(0,3,3))))
        coords -= set(self.coordinates_cuboid(1, 3, 1, offset=(4,3,4)))
        return sorted(coords)


class Polycubes12345CubeCluster2(Polycubes12345):

    """many solutions"""

    width = 9
    height = 9
    depth = 6

    transform_solution_matrix = Puzzle3D.swap_yz_transform

    def coordinates(self):
        coords = set(
            list(self.coordinates_cuboid(9, 3, 3, offset=(0,3,0)))
            + list(self.coordinates_cuboid(3, 9, 3, offset=(3,0,0)))
            + list(self.coordinates_cuboid(3, 3, 3, offset=(3,3,3)))
            + list(self.coordinates_cuboid(5, 3, 1, offset=(2,3,3)))
            + list(self.coordinates_cuboid(3, 5, 1, offset=(3,2,3)))
            + list(self.coordinates_cuboid(5, 5, 3, offset=(2,2,0))))
        return sorted(coords)


class Polycubes12345CubeCluster3(Polycubes12345):

    """many solutions"""

    width = 9
    height = 9
    depth = 3

    transform_solution_matrix = Puzzle3D.swap_yz_transform

    def coordinates(self):
        coords = set(
            list(self.coordinates_cuboid(6, 6, 3))
            + list(self.coordinates_cuboid(6, 6, 3, offset=(3,3,0))))
        coords -= set(self.coordinates_cuboid(1, 1, 3, offset=(4,4,0)))
        return sorted(coords)


class Polycubes12345OverlappingBlocks1(Polycubes12345):

    """many solutions"""

    width = 7
    height = 7
    depth = 6

    transform_solution_matrix = Puzzle3D.swap_yz_transform

    def coordinates(self):
        coords = set(
            list(self.coordinates_cuboid(4, 4, 6))
            + list(self.coordinates_cuboid(4, 4, 6, offset=(3,3,0))))
        return sorted(coords)


class Polycubes12345OverlappingBlocks2(Polycubes12345):

    """many solutions"""

    width = 9
    height = 9
    depth = 6

    transform_solution_matrix = Puzzle3D.swap_yz_transform

    def coordinates(self):
        coords = set(
            list(self.coordinates_cuboid(3, 3, 6))
            + list(self.coordinates_cuboid(3, 3, 6, offset=(3,3,0))) 
            + list(self.coordinates_cuboid(3, 3, 6, offset=(6,6,0)))
            + list(self.coordinates_cuboid(2, 2, 6, offset=(2,2,0)))
            + list(self.coordinates_cuboid(2, 2, 6, offset=(5,5,0))))
        return sorted(coords)


class Polycubes12345OverlappingBlocks3(Polycubes12345):

    """many solutions"""

    width = 9
    height = 9
    depth = 4

    transform_solution_matrix = Puzzle3D.swap_yz_transform

    def coordinates(self):
        coords = set(
            list(self.coordinates_cuboid(6, 6, 1))
            + list(self.coordinates_cuboid(6, 6, 1, offset=(3,3,0)))
            + list(self.coordinates_cuboid(5, 5, 4, offset=(2,2,0))))
        for x in (1, 5):
            for y in (1, 5):
                coords.update(
                    set(self.coordinates_cuboid(3, 3, 3, offset=(x,y,0))))
        return sorted(coords)


class Polycubes12345OverlappingBlocks4(Polycubes12345):

    """many solutions"""

    width = 7
    height = 7
    depth = 6

    transform_solution_matrix = Puzzle3D.swap_yz_transform

    def coordinates(self):
        coords = set(
            list(self.coordinates_cuboid(5, 5, 5, offset=(1,1,0)))
            + [self.coordinate_offset(3, 3, 5, None)])
        for x in (0, 4):
            for y in (0, 4):
                coords.update(
                    set(self.coordinates_cuboid(3, 3, 3, offset=(x,y,0))))
        return sorted(coords)


class Polycubes12345Pyramid1(Polycubes12345):

    """many solutions"""

    width = 11
    height = 11
    depth = 6

    transform_solution_matrix = Puzzle3D.swap_yz_transform

    def coordinates(self):
        coords = set()
        for i in range(6):
            coords.update(set(self.coordinates_cuboid(
                11 - 2 * i, 11 - 2 * i, 1, offset=(i, i, i))))
        for x in (0, 7):
            for y in (0, 7):
                coords.difference_update(set(self.coordinates_cuboid(
                    4, 4, 6, offset=(x,y,0))))
        for i in range(2):
            coords.update(set(self.coordinates_cuboid(
                7 - 2 * i, 7 - 2 * i, 1, offset=(2 + i, 2 + i, i))))
        return sorted(coords)


class Polycubes12345CrossBlock1(Polycubes12345):

    """many solutions"""

    width = 7
    height = 5
    depth = 6

    transform_solution_matrix = Puzzle3D.swap_yz_transform

    def coordinates(self):
        coords = set(
            list(self.coordinates_cuboid(7, 3, 6, offset=(0,1,0)))
            + list(self.coordinates_cuboid(5, 5, 6, offset=(1,0,0))))
        return sorted(coords)


class Polycubes12345CrossBlock2(Polycubes12345):

    """many solutions"""

    width = 7
    height = 7
    depth = 6

    transform_solution_matrix = Puzzle3D.swap_yz_transform

    def coordinates(self):
        coords = set(
            list(self.coordinates_cuboid(7, 3, 6, offset=(0,2,0)))
            + list(self.coordinates_cuboid(3, 7, 6, offset=(2,0,0))))
        coords -= set(self.coordinates_cuboid(1, 1, 6, offset=(2,2,0)))
        coords -= set(self.coordinates_cuboid(1, 1, 6, offset=(4,4,0)))
        return sorted(coords)
