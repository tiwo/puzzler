#!/usr/bin/env python
# $Id$

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2012 by David J. Goodger
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
        coords = (
            set(self.coordinates_cuboid(self.width, self.height, self.depth))
            - set(self.coordinates_cuboid(self.width-2, self.height-2,
                                          self.depth-1, offset=(1,1,1))))
        return sorted(coords)


class Polycubes234OpenBox6x4x2(Polycubes234OpenBox4x4x3):

    """many solutions"""

    width = 6
    height = 4
    depth = 2
