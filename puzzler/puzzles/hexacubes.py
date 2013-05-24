#!/usr/bin/env python
# $Id$

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2012 by David J. Goodger
# License: GPL 2 (see __init__.py)

"""
Concrete hexacube puzzles.

WARNING: Running these puzzles uses a LOT of RAM (more than I have!).
"""

from puzzler.puzzles import Puzzle3D, Puzzle2D
from puzzler.puzzles.polycubes import Hexacubes


class Hexacubes10x10x10_1(Hexacubes):

    """many solutions"""

    width = 10
    height = 10
    depth = 10

    def coordinates(self):
        coords = set(
            self.coordinates_cuboid(self.width, self.height, self.depth))
        for x in (0, 9):
            for y in (0, 9):
                coords.remove((x, y, 9))
        return sorted(coords)


class Hexacubes83x4x3(Hexacubes):

    """many solutions"""

    width = 4
    height = 83
    depth = 3

    transform_solution_matrix = Puzzle3D.cycle_xyz_transform


class HexacubesSteppedPyramid(Hexacubes):

    """
    many solutions

    Design from `Andrew Clarke's Poly Pages
    <http://www.recmath.com/PolyPages/PolyPages/index.htm?Polycubes.html#hexacubes>`_
    """

    width = 18
    height = 18
    depth = 9

    transform_solution_matrix = Puzzle3D.swap_yz_transform

    def coordinates(self):
        coords = set()
        for i in range(self.depth):
            margin = 2 * ((i + 1) / 2)
            coords.update(set(self.coordinates_cuboid(
                self.width - 2 * margin, self.height - 2 * margin, 1,
                offset=(margin, margin, i))))
        return sorted(coords)


class HexacubesHouse(Hexacubes):

    """
    many solutions

    Design by `Peter F. Esser <http://polyforms.eu/100plus/hexacubes.html>`_
    """

    width = 6
    height = 13
    depth = 16

    transform_solution_matrix = Puzzle3D.cycle_xyz_transform

    def coordinates(self):
        coords = set(self.coordinates_cuboid(self.width, self.height, 10))
        for i in range(1, 7):
            coords.update(set(self.coordinates_cuboid(
                self.width, self.height - 2 * i, 1,
                offset=(0, i, 9 + i))))
        return sorted(coords)
