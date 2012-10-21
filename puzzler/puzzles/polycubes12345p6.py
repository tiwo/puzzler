#!/usr/bin/env python
# $Id$

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2012 by David J. Goodger
# License: GPL 2 (see __init__.py)

"""
Concrete polycube (order 1 through 5, partial order 6) puzzles.
"""

from puzzler.puzzles import Puzzle3D, Puzzle2D
from puzzler.puzzles.polycubes import Polycubes12345p6


class Polycubes12345p6_6x6x6(Polycubes12345p6):

    """many solutions"""

    width = 6
    height = 6
    depth = 6


class Polycubes12345p6Cubes345(Polycubes12345p6):

    """
    many solutions

      The only three consecutive integers whose cubes sum to a cube
      are given by the Diophantine equation

          3³ + 4³ + 5³ = 6³

      -- http://mathworld.wolfram.com/CubicNumber.html

    This is also the first solution to the Diophantine 3.1.3 equation.

    This puzzle illustrates the left hand side of this equation, while
    `Polycubes12345p6_6x6x6` illustrates the right-hand side.
    """

    width = 5
    height = 14
    depth = 5

    def coordinates(self):
        # Ordering the cubes this way results in quick solutions, but
        # requires a custom transform_solution_matrix.
        coords = set(
            list(self.coordinates_cuboid(5, 5, 5, offset=(0,9,0)))
            + list(self.coordinates_cuboid(4, 4, 4, offset=(0,4,0)))
            + list(self.coordinates_cuboid(3, 3, 3)))
        return sorted(coords, reverse=True)

    def transform_solution_matrix(self, s_matrix):
        """Rearrange solution matrix for better rendering."""
        y_range = range(self.height)
        y_range = y_range[9:] + y_range[3:9] + y_range[:3]
        return [[[s_matrix[z][y][x] for y in y_range]
                 for z in range(self.depth)]
                for x in range(self.width)]
