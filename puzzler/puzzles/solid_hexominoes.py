#!/usr/bin/env python
# $Id$

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2015 by David J. Goodger
# License: GPL 2 (see __init__.py)

"""
Concrete solid hexomino puzzles.

Care must be taken to avoid parity imbalances.
"""

from puzzler.puzzles import Puzzle3D, Puzzle2D
from puzzler.puzzles.polycubes import SolidHexominoes, SolidHexominoesPlus


class SolidHexominoesSteppedBlock13x5x4(SolidHexominoes):

    """
    many solutions

    Design from `Andrew Clarke's Poly Pages
    <http://www.recmath.com/PolyPages/PolyPages/Polycubes.html>`_
    """

    width = 5
    height = 13
    depth = 4

    transform_solution_matrix = Puzzle3D.cycle_xyz_transform

    def coordinates(self):
        coords = set(
            list(self.coordinates_cuboid(5, 13, 1))
            + list(self.coordinates_cuboid(5, 11, 1, offset=(0,1,1)))
            + list(self.coordinates_cuboid(5, 9, 2, offset=(0,2,2))))
        return sorted(coords)


class SolidHexominoesSteppedBlock9x5x8(SolidHexominoes):

    """many solutions"""

    width = 5
    height = 9
    depth = 8

    transform_solution_matrix = Puzzle3D.cycle_xyz_transform

    def coordinates(self):
        coords = set(
            list(self.coordinates_cuboid(5, 9, 1))
            + list(self.coordinates_cuboid(5, 7, 1, offset=(0,1,1)))
            + list(self.coordinates_cuboid(5, 5, 5, offset=(0,2,2)))
            + list(self.coordinates_cuboid(3, 1, 1, offset=(1,4,7)))
            + list(self.coordinates_cuboid(1, 3, 1, offset=(2,3,7))))
        return sorted(coords)


class SolidHexominoes9x9x3_1(SolidHexominoes):

    """
    many solutions

    The central cube in the middle layer is empty.

    Design from `Andrew Clarke's Poly Pages`_
    """

    width = 9
    height = 9
    depth = 3

    holes = ((4,4,1),)

    transform_solution_matrix = Puzzle3D.cycle_xyz_transform

    def coordinates(self):
        coords = set(
            list(self.coordinates_cuboid(9, 9, 2))
            + list(self.coordinates_cuboid(7, 7, 1, offset=(1,1,2))))
        for coord in self.holes:
            coords.remove(coord)
        return sorted(coords)


class SolidHexominoes9x9x3_2(SolidHexominoes):

    """
    many solutions

    Design from `Andrew Clarke's Poly Pages`_
    """

    width = 9
    height = 9
    depth = 3

    holes = ((4,4,0), (4,4,1), (4,4,2), (3,4,2), (5,4,2),
             (4,2,2), (4,3,2), (4,5,2), (4,6,2),)

    transform_solution_matrix = Puzzle3D.cycle_xyz_transform

    def coordinates(self):
        coords = set(self.coordinates_cuboid(9, 9, 2))
        layer = set(Puzzle2D.coordinates_rectangle(9, 9)).intersection(
            set(Puzzle2D.coordinates_diamond(6, offset=(-1,-1))))
        for (x,y) in layer:
            coords.add(self.coordinate_offset(x, y, 2, None))
        for coord in self.holes:
            coords.remove(coord)
        return sorted(coords)


class SolidHexominoesPlus6x6x6(SolidHexominoesPlus):

    """many solutions"""

    width = 6
    height = 6
    depth = 6


class SolidHexominoesPlusSteps11x6x6(SolidHexominoesPlus):

    """many solutions"""

    width = 6
    height = 11
    depth = 6

    transform_solution_matrix = Puzzle3D.cycle_xyz_transform

    def coordinates(self):
        coords = set()
        for i in range(self.depth):
            coords.update(set(self.coordinates_cuboid(
                self.width, self.height - 2 * i, 1, offset=(0,i,i))))
        return sorted(coords)
