#!/usr/bin/env python
# $Id$

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2012 by David J. Goodger
# License: GPL 2 (see __init__.py)

"""
Concrete heptiamonds puzzles.
"""

from puzzler.puzzles.polyiamonds import Heptiamonds
from puzzler.puzzles.polyhexes import Polyhexes
from puzzler.coordsys import (
    Triangular3DCoordSet, Triangular3D, Hexagonal2DCoordSet)


class Heptiamonds3x28(Heptiamonds):

    """ solutions"""

    height = 3
    width = 28

    duplicate_conditions = ({'rotate_180': True},)


class Heptiamonds4x21(Heptiamonds):

    """ solutions"""

    height = 4
    width = 21

    duplicate_conditions = ({'rotate_180': True},)


class Heptiamonds6x14(Heptiamonds):

    """ solutions"""

    height = 6
    width = 14

    duplicate_conditions = ({'rotate_180': True},)


class Heptiamonds7x12(Heptiamonds):

    """ solutions"""

    height = 7
    width = 12

    duplicate_conditions = ({'rotate_180': True},)


class HeptiamondsSnowflake1(Heptiamonds):

    """ solutions"""

    height = 12
    width = 12

    check_for_duplicates = False

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    total = x + y + z
                    if ( 5 < total < 18
                         and (y > 1 or x < 10 and total > 7)
                         and (x > 1 or y < 10 and total > 7)
                         and (total < 16 or x < 10 and y < 10)):
                        yield (x, y, z)

    def customize_piece_data(self):
        self.piece_data['I7'][-1]['rotations'] = None
        self.piece_data['W7'][-1]['flips'] = None


class HeptiamondsSnowflake2(Heptiamonds):

    """ solutions"""

    height = 16
    width = 16

    check_for_duplicates = False

    def coordinates(self):
        holes = set(((7,4,0),(7,4,1),(8,4,0),(8,3,1),
                     (11,3,1),(11,4,0),(11,4,1),(12,4,0),
                     (11,7,1),(12,7,0),(11,8,0),(11,8,1),
                     (7,12,0),(7,11,1),(8,11,0),(8,11,1),
                     (3,11,1),(4,11,0),(4,11,1),(4,12,0),
                     (3,8,1),(4,8,0),(4,7,1),(4,7,0),))
        coords = set()
        for y in range(4, 16):
            for x in range(4, 16):
                for z in range(self.depth):
                    coord = (x, y, z)
                    if x + y + z < 20 and not coord in holes:
                        coords.add(coord)
                        yield coord
        for y in range(12):
            for x in range(12):
                for z in range(self.depth):
                    coord = (x, y, z)
                    if ( x + y + z > 11 and not coord in holes
                         and coord not in coords):
                        coords.add(coord)
                        yield (x, y, z)

    def customize_piece_data(self):
        self.piece_data['P7'][-1]['rotations'] = None
        self.piece_data['P7'][-1]['flips'] = None


class HeptiamondsTriangle(Heptiamonds):

    """ solutions"""

    height = 13
    width = 13

    check_for_duplicates = False

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if x + y + z < 13 and (x, y, z) != (4, 4, 0):
                        yield (x, y, z)

    def customize_piece_data(self):
        self.piece_data['I7'][-1]['rotations'] = None
        self.piece_data['W7'][-1]['flips'] = None


class Heptiamonds12x13Trapezium(Heptiamonds):

    """ solutions"""

    height = 12
    width = 13

    check_for_duplicates = False

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if x + y + z < self.width:
                        yield (x, y, z)

    def customize_piece_data(self):
        self.piece_data['W7'][-1]['flips'] = None


class Heptiamonds6x17Trapezium(Heptiamonds12x13Trapezium):

    height = 6
    width = 17


class Heptiamonds4x23Trapezium(Heptiamonds12x13Trapezium):

    height = 4
    width = 23


class HeptiamondsHexagram(Heptiamonds):

    """
    many solutions

    16-unit-high hexagram with central 4-unit hexagonal hole
    """

    height = 16
    width = 16

    def coordinates(self):
        coords = set()
        for z in range(self.depth):
            for y in range(4, 16):
                for x in range(4, 16):
                    total = x + y + z
                    if total < 20 and not (5 < x < 10 and 5 < y < 10
                                           and 13 < total < 18):
                        coord = (x, y, z)
                        coords.add(coord)
                        yield coord
            for y in range(12):
                for x in range(12):
                    total = x + y + z
                    if total >= 12 and not (5 < x < 10 and 5 < y < 10
                                            and 13 < total < 18):
                        coord = (x, y, z)
                        if coord not in coords:
                            coords.add(coord)
                            yield coord

    def customize_piece_data(self):
        self.piece_data['P7'][-1]['flips'] = None
        self.piece_data['P7'][-1]['rotations'] = None


class HeptiamondsHexagram2(Heptiamonds):

    """
    16-unit-high hexagram (side length = 4) with two 4-unit-high hexagram
    holes (side length = 1) arranged horizontally, 1 unit apart.

    Many solutions.
    """

    height = 16
    width = 16

    offsets = ((4,6,0), (8,6,0))

    def coordinates(self):
        holes = set()
        for coord in self.coordinates_hexagram(1):
            for offset in self.offsets:
                holes.add(coord + offset)
        for coord in self.coordinates_hexagram(4):
            if coord not in holes:
                yield coord


class HeptiamondsHexagram3(HeptiamondsHexagram2):

    """
    16-unit-high hexagram (side length = 4) with two 4-unit-high hexagram
    holes (side length = 1) arranged horizontally, 3 units apart.

    Many solutions.
    """

    offsets = ((3,6,0), (9,6,0))


class HeptiamondsHexagram4(HeptiamondsHexagram2):

    """
    16-unit-high hexagram (side length = 4) with two 4-unit-high hexagram
    holes (side length = 1) arranged vertically, touching.

    Many solutions.
    """

    offsets = ((5,8,0), (7,4,0))


class HeptiamondsHexagon1(Heptiamonds):

    """
     solutions

    12-unit-high hexagon with central 8-unit-high hexagram hole
    """

    height = 12
    width = 12

    duplicate_conditions = ({'rotate_180': True},)

    def coordinates(self):
        hole = set()
        for y in range(4, 10):
            for x in range(4, 10):
                for z in range(self.depth):
                    if x + y + z < 14:
                        hole.add((x, y, z))
        for y in range(2, 8):
            for x in range(2, 8):
                for z in range(self.depth):
                    if x + y + z > 9:
                        hole.add((x, y, z))
        for y in range(self.height):
            for x in range(self.width):
                for z in range(self.depth):
                    total = x + y + z
                    coord = (x, y, z)
                    if 5 < total < 18 and coord not in hole:
                        yield coord

    def customize_piece_data(self):
        self.piece_data['P7'][-1]['flips'] = None


class HeptiamondsHexagon2(Heptiamonds):

    """
     solutions

    12-unit-high hexagon with two central stacked 4-unit-high hexagon holes
    """

    height = 12
    width = 12

    duplicate_conditions = ({'rotate_180': True},)

    def coordinates(self):
        hole = set()
        for y in range(2, 6):
            for x in range(5, 9):
                for z in range(self.depth):
                    if 8 < x + y + z < 13:
                        hole.add((x, y, z))
        for y in range(6, 10):
            for x in range(3, 7):
                for z in range(self.depth):
                    if 10 < x + y + z < 15:
                        hole.add((x, y, z))
        for y in range(self.height):
            for x in range(self.width):
                for z in range(self.depth):
                    coord = (x, y, z)
                    if 5 < x + y + z < 18 and coord not in hole:
                        yield coord

    def customize_piece_data(self):
        self.piece_data['P7'][-1]['flips'] = None


class HeptiamondsHexagon3(Heptiamonds):

    """
     solutions

    12-unit-high hexagon with two central adjacent 4-unit-high hexagon holes
    (horizontal)
    """

    height = 12
    width = 12

    duplicate_conditions = ({'rotate_180': True},)

    def coordinates(self):
        hole = set()
        for y in range(4, 8):
            for x in range(2, 6):
                for z in range(self.depth):
                    if 7 < x + y + z < 12:
                        hole.add((x, y, z))
            for x in range(6, 10):
                for z in range(self.depth):
                    if 11 < x + y + z < 16:
                        hole.add((x, y, z))
        for y in range(self.height):
            for x in range(self.width):
                for z in range(self.depth):
                    coord = (x, y, z)
                    if 5 < x + y + z < 18 and coord not in hole:
                        yield coord

    def customize_piece_data(self):
        self.piece_data['P7'][-1]['flips'] = None


class HeptiamondsHexagon4(Heptiamonds):

    """
     solutions

    12-unit-high hexagon with two central separated 4-unit-high hexagon holes
    (horizontal)
    """

    height = 12
    width = 12

    duplicate_conditions = ({'rotate_180': True},)

    def coordinates(self):
        hole = set()
        for y in range(4, 8):
            for x in range(1, 5):
                for z in range(self.depth):
                    if 6 < x + y + z < 11:
                        hole.add((x, y, z))
            for x in range(7, 11):
                for z in range(self.depth):
                    if 12 < x + y + z < 17:
                        hole.add((x, y, z))
        for y in range(self.height):
            for x in range(self.width):
                for z in range(self.depth):
                    coord = (x, y, z)
                    if 5 < x + y + z < 18 and coord not in hole:
                        yield coord

    def customize_piece_data(self):
        self.piece_data['P7'][-1]['flips'] = None


class HeptiamondsHexagon5(Heptiamonds):

    """
     solutions

    12-unit-high hexagon with two 4-unit-high hexagon holes in opposite
    corners (horizontal)
    """

    height = 12
    width = 12

    duplicate_conditions = ({'rotate_180': True},)

    def coordinates(self):
        hole = set()
        for y in range(4, 8):
            for x in range(4):
                for z in range(self.depth):
                    if 5 < x + y + z < 10:
                        hole.add((x, y, z))
            for x in range(8, 12):
                for z in range(self.depth):
                    if 13 < x + y + z < 18:
                        hole.add((x, y, z))
        for y in range(self.height):
            for x in range(self.width):
                for z in range(self.depth):
                    coord = (x, y, z)
                    if 5 < x + y + z < 18 and coord not in hole:
                        yield coord

    def customize_piece_data(self):
        self.piece_data['P7'][-1]['flips'] = None


class HeptiamondsHexagon6(Heptiamonds):

    """
     solutions

    12-unit-high hexagon with a central snowflake hole
    """

    height = 12
    width = 12

    duplicate_conditions = ({'rotate_180': True},)

    def coordinates(self):
        hole = set()
        for y in range(3, 9):
            for x in range(3, 9):
                for z in range(self.depth):
                    if 8 < x + y + z < 15:
                        hole.add((x, y, z))
        for coord in ((4,4,1), (7,3,0), (8,4,1), (3,7,0), (4,8,1), (7,7,0)):
            hole.remove(coord)
        for y in range(self.height):
            for x in range(self.width):
                for z in range(self.depth):
                    coord = (x, y, z)
                    if 5 < x + y + z < 18 and coord not in hole:
                        yield coord

    def customize_piece_data(self):
        self.piece_data['P7'][-1]['flips'] = None


class HeptiamondsHexagon7(Heptiamonds):

    """
     solutions

    12-unit-high hexagon with a central trefoil hole
    """

    height = 12
    width = 12

    def coordinates(self):
        hole = set()
        for y in range(3, 9):
            for x in range(3, 9):
                for z in range(self.depth):
                    if 8 < x + y + z < 15:
                        hole.add((x, y, z))
        for coord in ((5,3,1), (6,3,0), (8,5,1), (8,6,0), (3,8,0), (3,8,1)):
            hole.remove(coord)
        for y in range(self.height):
            for x in range(self.width):
                for z in range(self.depth):
                    coord = (x, y, z)
                    if 5 < x + y + z < 18 and coord not in hole:
                        yield coord

    def customize_piece_data(self):
        self.piece_data['P7'][-1]['flips'] = None


class HeptiamondsHexagon8(Heptiamonds):

    """
    many solutions.

    12-unit-high hexagon with a central hexagonal whorl hole.
    """

    height = 12
    width = 12

    def coordinates(self):
        hole = set()
        for y in range(3, 9):
            for x in range(3, 9):
                for z in range(self.depth):
                    if 8 < x + y + z < 15:
                        hole.add((x, y, z))
        for coord in ((5,3,1), (8,3,0), (8,5,1), (6,8,0), (3,6,0), (3,8,1)):
            hole.remove(coord)
        for y in range(self.height):
            for x in range(self.width):
                for z in range(self.depth):
                    coord = (x, y, z)
                    if 5 < x + y + z < 18 and coord not in hole:
                        yield coord


class HeptiamondsHexagon9(Heptiamonds):

    """
    many solutions.

    12-unit-high hexagon with a central triangular whorl hole.
    """

    height = 12
    width = 12

    def coordinates(self):
        hole = set()
        for y in range(4, 10):
            for x in range(4, 10):
                for z in range(self.depth):
                    if x + y + z < 14:
                        hole.add((x, y, z))
        for y in range(2):
            for x in range(2):
                for z in range(self.depth):
                    if x + y + z > 1:
                        for dx, dy in ((2,4), (8,2), (4,8)):
                            hole.add((x + dx, y + dy, z))
        for y in range(self.height):
            for x in range(self.width):
                for z in range(self.depth):
                    coord = (x, y, z)
                    if 5 < x + y + z < 18 and coord not in hole:
                        yield coord


class HeptiamondsHexagon10(Heptiamonds):

    """
    many solutions.

    12-unit-high hexagon with a central tri-lobed hole.
    """

    height = 12
    width = 12

    def coordinates(self):
        hole = set()
        for y in range(4, 8):
            for x in range(4, 8):
                for z in range(self.depth):
                    if 9 < x + y + z < 14:
                        hole.add((x, y, z))
        for y in range(2, 10):
            for x in range(2, 10):
                for z in range(self.depth):
                    total = x + y + z
                    if 7 < total < 16:
                        if (  ((5 <= y <= 6) and (x < 6))
                              or ((5 <= x <= 6) and (y > 6))
                              or ((11 <= total <= 12) and (x > 6))):
                            hole.add((x, y, z))
        for y in range(self.height):
            for x in range(self.width):
                for z in range(self.depth):
                    coord = (x, y, z)
                    if 5 < x + y + z < 18 and coord not in hole:
                        yield coord


class HeptiamondsHexagon11(Heptiamonds):

    """
    many solutions.

    12-unit-high hexagon with three hexagonal holes.
    """

    height = 12
    width = 12

    def coordinates(self):
        hole = set()
        for y in range(2, 10):
            for x in range(2, 10):
                for z in range(self.depth):
                    total = x + y + z
                    if (  ((y <= 4) and (3 < x < 8) and (7 < total < 11))
                          or ((y >= 7) and (x < 5) and (9 < total < 14))
                          or ((4 <= y <= 7) and (x > 6) and (12 < total < 16))):
                        hole.add((x, y, z))
        for y in range(self.height):
            for x in range(self.width):
                for z in range(self.depth):
                    coord = (x, y, z)
                    if 5 < x + y + z < 18 and coord not in hole:
                        yield coord


class HeptiamondsDiamondRing(Heptiamonds):

    """
    many solutions

    10-unit diamond with central 4-unit diamond hole
    """

    height = 10
    width = 10

    duplicate_conditions = ({'rotate_180': True},)

    svg_rotation = 30

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if x < 3 or x > 6 or y < 3 or y > 6:
                        yield (x, y, z)

    def customize_piece_data(self):
        self.piece_data['W7'][-1]['flips'] = None


class HeptiamondsDiamondWindow(Heptiamonds):

    """
    many solutions

    10-unit diamond with 4 2-unit diamond holes, like a window frame

    design by `Johannes Hindriks <http://jhhindriks.info/37/index.htm>`_
    """

    height = 10
    width = 10

    check_for_duplicates = False

    svg_rotation = 30

    def coordinates(self):
        coords = set(self.coordinates_parallelogram(10, 10))
        for x in (2, 6):
            for y in (2, 6):
                coords -= set(
                    self.coordinates_parallelogram(2, 2, offset=(x,y,0)))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P7'][-1]['flips'] = None
        self.piece_data['P7'][-1]['rotations'] = (0, 1, 2,)


class Heptiamonds4x22LongHexagon(Heptiamonds):

    """
     solutions

    Elongated hexagon (clipped parallelogram) 4 units high by 22 units wide.
    """

    height = 4
    width = 22

    duplicate_conditions = ({'rotate_180': True},)

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if (  (self.height / 2 - 1)
                          < (x + y + z)
                          < (self.width + self.height / 2) ):
                        yield (x, y, z)

    def customize_piece_data(self):
        self.piece_data['W7'][-1]['flips'] = None


class Heptiamonds10x12ShortHexagon(Heptiamonds4x22LongHexagon):

    """
     solutions

    Shortened hexagon (clipped parallelogram) 10 units wide by 12 units high.
    """

    height = 12
    width = 10


class HeptiamondsChevron(Heptiamonds):

    """
    Left-facing chevron.

    Width of solution space is (apparent width) + (height / 2).
    """

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if y >= self.height / 2:
                        if x < (self.width - self.height / 2):
                            # top half
                            yield (x, y, z)
                    elif (self.height / 2 - 1) < (x + y + z) < self.width:
                        # bottom half
                        yield (x, y, z)

    def customize_piece_data(self):
        self.piece_data['W7'][-1]['flips'] = None


class Heptiamonds4x21Chevron(HeptiamondsChevron):

    """many solutions."""

    height = 4
    width = 23


class Heptiamonds6x14Chevron(HeptiamondsChevron):

    """many solutions."""

    height = 6
    width = 17


class Heptiamonds12x7Chevron(HeptiamondsChevron):

    """many solutions."""

    height = 12
    width = 13


class Heptiamonds14x6Chevron(HeptiamondsChevron):

    """many solutions."""

    height = 14
    width = 13

    svg_rotation = 90


class Heptiamonds28x3Chevron(HeptiamondsChevron):

    """many solutions."""

    height = 28
    width = 17

    svg_rotation = 90


class HeptiamondsStack(Heptiamonds):

    """
    Stack of 2-high elongated hexagons; approximation of a rectangle.

    Width of solution space is (apparent width) + (height / 2) - 1.
    """

    duplicate_conditions = ({'rotate_180': True},)

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if (self.height - 1) <= (2 * x + y + z) < (self.width * 2):
                        yield (x, y, z)

    def customize_piece_data(self):
        self.piece_data['W7'][-1]['flips'] = None


class Heptiamonds11x8Stack(HeptiamondsStack):

    """many solutions"""

    height = 8
    width = 14


class Heptiamonds4x24Stack(HeptiamondsStack):

    """many solutions"""

    height = 24
    width = 15

    svg_rotation = 90


class HeptiamondsHexedTriangle(Heptiamonds):

    """many solutions"""

    height = 14
    width = 14

    check_for_duplicates = False

    svg_rotation = -30

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if ( (x + 2 * y + z >= 13)
                         and (y - x <= 7)
                         and (2 * x + y + z <= 27)):
                        yield (x, y, z)


class HeptiamondsHexgridElongatedHexagon9x2(Heptiamonds):

    """many solutions"""

    width = 13
    height = 13

    check_for_duplicates = False

    svg_rotation = 30

    def coordinates(self):
        hcoords = set(Polyhexes.coordinates_elongated_hexagon(9, 2))
        coords = set(self.coordinates_hexgrid(hcoords, offset=(0,-1,0)))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P7'][-1]['rotations'] = (0, 1, 2)
        self.piece_data['P7'][-1]['flips'] = None


class HeptiamondsHexgridElongatedHexagon5x3(Heptiamonds):

    """many solutions"""

    width = 12
    height = 12

    check_for_duplicates = False

    svg_rotation = 30

    def coordinates(self):
        hcoords = (
            set(Polyhexes.coordinates_elongated_hexagon(5, 3))
            - set(Polyhexes.coordinates_hexagon(1, offset=(3,2))))
        coords = set(self.coordinates_hexgrid(hcoords, offset=(0,-2,0)))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P7'][-1]['rotations'] = (0, 1, 2)
        self.piece_data['P7'][-1]['flips'] = None


class HeptiamondsHexgrid7x4(Heptiamonds):

    """many solutions"""

    width = 11
    height = 14

    check_for_duplicates = False

    svg_rotation = 30

    def coordinates(self):
        hcoords = set(Polyhexes.coordinates_parallelogram(7, 4))
        coords = self.coordinates_hexgrid(hcoords)
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P7'][-1]['rotations'] = (0, 1, 2)


class HeptiamondsHexgrid14x2(Heptiamonds):

    """many solutions"""

    width = 16
    height = 17

    check_for_duplicates = False

    svg_rotation = 30

    def coordinates(self):
        hcoords = set(Polyhexes.coordinates_parallelogram(14, 2))
        coords = self.coordinates_hexgrid(hcoords)
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P7'][-1]['rotations'] = (0, 1, 2)


class HeptiamondsHexgridHexagon1(Heptiamonds):

    """many solutions"""

    width = 14
    height = 14

    check_for_duplicates = False

    svg_rotation = -30

    def coordinates(self):
        hcoords = (
            set(Polyhexes.coordinates_hexagon(4))
            - set(Polyhexes.coordinates_parallelogram(3, 3, offset=(2,2))))
        coords = self.coordinates_hexgrid(hcoords, offset=(0,-3,0))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P7'][-1]['rotations'] = (0, 1, 2)
        self.piece_data['P7'][-1]['flips'] = None


class HeptiamondsHexgridHexagon_x1(HeptiamondsHexgridHexagon1):

    """0 solutions"""

    holes = set(((1,3), (1,5), (2,3), (3,1), (3,4), (3,5), (4,2), (5,1), (5,3)))

    def coordinates(self):
        hcoords = set(Polyhexes.coordinates_hexagon(4)) - self.holes
        coords = self.coordinates_hexgrid(hcoords, offset=(0,-3,0))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P7'][-1]['rotations'] = (0, 1)
        self.piece_data['P7'][-1]['flips'] = None


class HeptiamondsHexgridTwoDiamonds1(Heptiamonds):

    """many solutions"""

    width = 14
    height = 14

    holes = set(((0,4), (0,5), (1,4), (3,2), (3,3), (3,4), (5,2), (6,1), (6,2)))

    check_for_duplicates = False

    def coordinates(self):
        hcoords = set(Polyhexes.coordinates_hexagon(4)) - self.holes
        coords = self.coordinates_hexgrid(hcoords, offset=(0,-3,0))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P7'][-1]['rotations'] = (0, 1, 2)
        self.piece_data['P7'][-1]['flips'] = None


class HeptiamondsHexgridTwoDiamonds2(HeptiamondsHexgridTwoDiamonds1):

    """many solutions"""

    holes = set(((0,4), (0,5), (1,4), (3,1), (3,3), (3,5), (5,2), (6,1), (6,2)))


class HeptiamondsHexgridTwoDiamonds3(Heptiamonds):

    """many solutions"""

    width = 17
    height = 8

    check_for_duplicates = False

    def coordinates(self):
        d = Hexagonal2DCoordSet(Polyhexes.coordinates_parallelogram(4, 4))
        d = d.rotate(5, (3,0))
        hcoords = set(list(d.translate((0, 2))) + list(d.translate((4, 0))))
        coords = self.coordinates_hexgrid(hcoords, offset=(0,-7,0))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P7'][-1]['flips'] = None
        self.piece_data['P7'][-1]['rotations'] = (0, 1, 2)


class HeptiamondsHexgridTwoDiamonds4(Heptiamonds):

    """many solutions"""

    width = 13
    height = 12

    check_for_duplicates = False

    def coordinates(self):
        d = Hexagonal2DCoordSet(Polyhexes.coordinates_parallelogram(4, 4))
        d = d.rotate(5, (3,0))
        hcoords = set(list(d) + list(d.translate((0, 2))))
        coords = self.coordinates_hexgrid(hcoords, offset=(0,-3,0))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P7'][-1]['flips'] = None
        self.piece_data['P7'][-1]['rotations'] = (0, 1, 2)


class HeptiamondsHexgridTrefoil1(Heptiamonds):

    """many solutions"""

    width = 15
    height = 15

    check_for_duplicates = False

    def coordinates(self):
        hcoords = set(
            list(Polyhexes.coordinates_hexagon(2, offset=(0,5)))
            + list(Polyhexes.coordinates_hexagon(2, offset=(3,3)))
            + list(Polyhexes.coordinates_hexagon(2, offset=(4,0)))
            + list(Polyhexes.coordinates_hexagon(2, offset=(5,4))))
        coords = self.coordinates_hexgrid(hcoords, offset=(0,-5,0))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P7'][-1]['rotations'] = (0, 1)


class HeptiamondsHexgridTrefoil2(Heptiamonds):

    """many solutions"""

    width = 14
    height = 14

    check_for_duplicates = False

    svg_rotation = 30

    def coordinates(self):
        t = Hexagonal2DCoordSet(Polyhexes.coordinates_triangle(2))
        hcoords = (
            set(Polyhexes.coordinates_hexagon(4))
            - set(t.translate((0,4)))
            - set(t.translate((4,0)))
            - set(t.translate((4,4))))
        coords = self.coordinates_hexgrid(hcoords, offset=(0,-3,0))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P7'][-1]['flips'] = None
        self.piece_data['P7'][-1]['rotations'] = (0, 1)


class HeptiamondsHexgridTrefoil3(Heptiamonds):

    """many solutions"""

    width = 13
    height = 13

    check_for_duplicates = False

    def coordinates(self):
        t = Hexagonal2DCoordSet(Polyhexes.coordinates_parallelogram(3, 1))
        hcoords = (
            set(Polyhexes.coordinates_hexagon(4))
            - set(t.translate((4,3)))
            - set(t.rotate0(1).translate((3,0)))
            - set(t.rotate0(2).translate((2,4))))
        coords = self.coordinates_hexgrid(hcoords, offset=(-1,-4,0))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P7'][-1]['flips'] = None
        self.piece_data['P7'][-1]['rotations'] = (0, 1)


class HeptiamondsHexgridTrefoil4(Heptiamonds):

    """many solutions"""

    width = 13
    height = 13

    check_for_duplicates = False

    def coordinates(self):
        t = Hexagonal2DCoordSet(Polyhexes.coordinates_triangle(2))
        hcoords = (
            set(Polyhexes.coordinates_hexagon(4))
            - set(t.translate((0,3)))
            - set(t.translate((5,0)))
            - set(t.translate((3,5))))
        coords = self.coordinates_hexgrid(hcoords, offset=(0,-3,0))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P7'][-1]['rotations'] = (0, 1)


class HeptiamondsHexgridTrefoil_x1(Heptiamonds):

    """0 solutions"""

    width = 15
    height = 15

    check_for_duplicates = False

    def coordinates(self):
        hcoords = set(
            list(Polyhexes.coordinates_hexagon(2, offset=(0,3)))
            + list(Polyhexes.coordinates_hexagon(2, offset=(3,3)))
            + list(Polyhexes.coordinates_hexagon(2, offset=(3,6)))
            + list(Polyhexes.coordinates_hexagon(2, offset=(6,0))))
        coords = self.coordinates_hexgrid(hcoords, offset=(-3,-7,0))
        return sorted(coords)


class HeptiamondsHexgridBumpyTriangle(Heptiamonds):

    """many solutions"""

    width = 12
    height = 12

    check_for_duplicates = False

    def coordinates(self):
        hcoords = set(
            list(Polyhexes.coordinates_hexagon(3, offset=(1,1)))
            + list(Polyhexes.coordinates_hexagon(2, offset=(0,4)))
            + list(Polyhexes.coordinates_hexagon(2, offset=(2,0)))
            + list(Polyhexes.coordinates_hexagon(2, offset=(4,2))))
        coords = self.coordinates_hexgrid(hcoords, offset=(0,-3,0))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P7'][-1]['flips'] = None
        self.piece_data['P7'][-1]['rotations'] = (0, 1)


class HeptiamondsHexgridStaggeredRectangle7x4(Heptiamonds):

    """many solutions"""

    width = 14
    height = 9

    check_for_duplicates = False

    def coordinates(self):
        hcoords = list(Polyhexes.coordinates_staggered_rectangle(7, 4))
        coords = self.coordinates_hexgrid(hcoords, offset=(0,-5,0))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P7'][-1]['flips'] = None


class HeptiamondsHexgridRosettes1(Heptiamonds):

    """many solutions"""

    width = 12
    height = 12

    check_for_duplicates = False

    svg_rotation = 30

    def coordinates(self):
        hcoords = set(
            list(Polyhexes.coordinates_hexagon(2, offset=(0,2)))
            + list(Polyhexes.coordinates_hexagon(2, offset=(1,4)))
            + list(Polyhexes.coordinates_hexagon(2, offset=(3,0)))
            + list(Polyhexes.coordinates_hexagon(2, offset=(4,2))))
        coords = self.coordinates_hexgrid(hcoords, offset=(-1,-4,0))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P7'][-1]['flips'] = None
        self.piece_data['P7'][-1]['rotations'] = (0, 1, 2)


class HeptiamondsHexgridRosettes2(Heptiamonds):

    """many solutions"""

    width = 12
    height = 15

    check_for_duplicates = False

    svg_rotation = 60

    def coordinates(self):
        hcoords = set(
            list(Polyhexes.coordinates_hexagon(2))
            + list(Polyhexes.coordinates_hexagon(2, offset=(3,0)))
            + list(Polyhexes.coordinates_hexagon(2, offset=(0,3)))
            + list(Polyhexes.coordinates_hexagon(2, offset=(3,3))))
        coords = self.coordinates_hexgrid(hcoords, offset=(0,-1,0))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P7'][-1]['flips'] = None
        self.piece_data['P7'][-1]['rotations'] = (0, 1, 2)


class HeptiamondsHexgridRosettes_x1(Heptiamonds):

    """0 solutions"""

    width = 15
    height = 15

    check_for_duplicates = False

    svg_rotation = 30

    def coordinates(self):
        hcoords = set(
            list(Polyhexes.coordinates_hexagon(2))
            + list(Polyhexes.coordinates_hexagon(2, offset=(3,0)))
            + list(Polyhexes.coordinates_hexagon(2, offset=(6,0)))
            + list(Polyhexes.coordinates_hexagon(2, offset=(9,0))))
        coords = self.coordinates_hexgrid(hcoords, offset=(0,-1,0))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P7'][-1]['flips'] = None
        self.piece_data['P7'][-1]['rotations'] = (0, 1, 2)


class HeptiamondsHexgridFlower1(Heptiamonds):

    """many solutions"""

    width = 12
    height = 12

    check_for_duplicates = False

    svg_rotation = 30

    holes = set(((0,3), (0,6), (3,0), (3,6), (6,0), (6,3), (2,2), (2,5), (5,2)))

    def coordinates(self):
        hcoords = set(Polyhexes.coordinates_hexagon(4)) - self.holes
        coords = self.coordinates_hexgrid(hcoords, offset=(-1,-4,0))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P7'][-1]['flips'] = None
        self.piece_data['P7'][-1]['rotations'] = (0, 1)


class HeptiamondsHexgridFlower2(HeptiamondsHexgridFlower1):

    """many solutions"""

    holes = set(((0,3), (0,6), (3,0), (3,6), (6,0), (6,3), (3,2), (2,4), (4,3)))

    svg_rotation = 0


class HeptiamondsShortHexRing(Heptiamonds):

    """
    many solutions.

    2x8 short hexagon with central 2-unit hexagon hole.
    """

    height = 10
    width = 10

    duplicate_conditions = ({'rotate_180': True},)

    svg_rotation = 30

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    total = x + y + z
                    if (  (1 < total < 18)
                          and (total < 8 or total > 11
                               or x < 3 or x > 6 or y < 3 or y > 6)):
                        yield (x, y, z)


class HeptiamondsTriangleRing(Heptiamonds):

    """many solutions"""

    height = 13
    width = 13

    check_for_duplicates = False

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    total = x + y + z
                    if 0 < total < 14 and (x < 3 or y < 3 or total > 10):
                        yield (x, y, z)


class HeptiamondsSemiregularHexagon8x3(Heptiamonds):

    """many solutions"""

    height = 11
    width = 11

    check_for_duplicates = False

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    total = x + y + z
                    if 2 < total < 14 and ((x, y, z) != (4,4,1)):
                        yield (x, y, z)


class HeptiamondsHexagons2x3_1(Heptiamonds):

    """
    Four 2x3 hexagons stacked vertically (I4 tetrahex).

    Many solutions.
    """

    height = 24
    width = 14

    offsets = [(0,18,0), (3,12,0), (6,6,0), (9,0,0)]

    def coordinates(self):
        for coord in self.coordinates_hex():
            for offset in self.offsets:
                yield coord + offset

    def coordinates_hex(self):
        for z in range(self.depth):
            for y in range(6):
                for x in range(5):
                    total = x + y + z
                    if 2 < total < 8:
                        yield Triangular3D((x, y, z))


class HeptiamondsHexagons2x3_2(HeptiamondsHexagons2x3_1):

    """
    Two horizontally adjacent groups of two 2x3 vertically stacked hexagons.

    Many solutions.
    """

    height = 12
    width = 13

    offsets = [(0,6,0), (3,0,0), (5,6,0), (8,0,0)]


class HeptiamondsHexagons2x3_3(HeptiamondsHexagons2x3_1):

    """
    Four 2x3 hexagons in a honeycomb grid (one nestled on each side of central
    stack of two; O4 tetrahex).

    Many solutions.
    """

    height = 12
    width = 12

    offsets = [(0,3,0), (5,0,0), (2,6,0), (7,3,0)]


class HeptiamondsHexagons2x3_4(HeptiamondsHexagons2x3_1):

    """
    As in #3, but the two central hexagons are now two vertical units apart.

    Many solutions.
    """

    height = 14
    width = 11

    offsets = [(0,4,0), (5,0,0), (1,8,0), (6,4,0)]


class HeptiamondsHexagons2x3_5(HeptiamondsHexagons2x3_1):

    """
    As in #3, but the two central hexagons are now four vertical units apart.

    Many solutions.
    """

    height = 16
    width = 10

    offsets = [(0,5,0), (5,0,0), (0,10,0), (5,5,0)]


class HeptiamondsHexagons2x3_6(HeptiamondsHexagons2x3_1):

    """
    Four 2x3 hexagons arranged as a trefoil (Y4 tetrahex): three hexagons
    attached to one central hexagon.

    Many solutions.
    """

    height = 15
    width = 13

    offsets = [(0,9,0), (5,6,0), (7,9,0), (8,0,0)]


class HeptiamondsHexagons2x3_7(HeptiamondsHexagons2x3_1):

    """
    Four 2x3 hexagons adjacent horizontally, with corners touching.

    many solutions.
    """

    height = 6
    width = 20

    offsets = [(0,0,0), (5,0,0), (10,0,0), (15,0,0)]

    I7_offsets = [(4, (0,0,0)), (5, (1,0,0)), (4, (1,1,0)), (3, (1,2,0))]

    def build_matrix(self):
        """
        There are only 4 possible positions for the I7 piece.

        After that, duplication prevention gets hard (if it's even necessary).
        """
        keys = sorted(self.pieces.keys())
        for aspect_index, coords in self.I7_offsets:
            i_coords, i_aspect = self.pieces['I7'][aspect_index]
            translated = i_aspect.translate(coords)
            self.build_matrix_row('I7', translated)
        keys.remove('I7')
        self.build_regular_matrix(keys)


class HeptiamondsSemiregularHexagons6x2(Heptiamonds):

    """
    Two identical semi-regular hexagons with triangular holes (second rotated
    to save space).

    Many solutions.
    """

    height = 8
    width = 13

    def coordinates(self):
        holes = set([(2,3,1), (3,2,1), (3,3,0), (3,3,1),
                     (9,4,0), (9,4,1), (9,5,0), (10,4,0)])
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if (x,y,z) in holes:
                        continue
                    total = x + y + z
                    if total < 10:
                        if total < 2 or x > 7:
                            continue
                    elif total > 10:
                        if x < 5 or total > 18:
                            continue
                    else:
                        continue
                    yield (x, y, z)


class HeptiamondsTrefoil1(Heptiamonds):

    """
    many solutions

    design from Kadon's Iamond Ring booklet
    """

    height = 16
    width = 16

    svg_rotation = 30

    def coordinates(self):
        h = Triangular3DCoordSet(self.coordinates_elongated_hexagon(6, 2))
        coords = set(
            list(h.translate((8,6,0)))
            + list(h.rotate0(1).translate((10,-2,0)))
            + list(h.rotate0(2).translate((10,8,0))))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P7'][-1]['rotations'] = (0, 1)
        self.piece_data['P7'][-1]['flips'] = None


class HeptiamondsTrefoil2(Heptiamonds):

    """many solutions"""

    height = 12
    width = 12

    svg_rotation = 30

    def coordinates(self):
        h = Triangular3DCoordSet(self.coordinates_hexagon(3))
        coords = set(
            list(self.coordinates_hexagon(4, offset=(2,2,0)))
            + list(h.translate((0,6,0)))
            + list(h.translate((3,0,0)))
            + list(h.translate((6,3,0))))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P7'][-1]['rotations'] = (0, 1)
        self.piece_data['P7'][-1]['flips'] = None


class HeptiamondsTrefoil3(Heptiamonds):

    """many solutions"""

    height = 14
    width = 14

    svg_rotation = 30

    def coordinates(self):
        h = Triangular3DCoordSet(self.coordinates_elongated_hexagon(3, 2))
        coords = set(
            list(self.coordinates_hexagon(4, offset=(3,3,0)))
            + list(h.translate((9,5,0)))
            + list(h.rotate0(1).translate((9,-2,0)))
            + list(h.rotate0(2).translate((7,9,0))))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P7'][-1]['rotations'] = (0, 1)
        self.piece_data['P7'][-1]['flips'] = None


class HeptiamondsTrefoil3(Heptiamonds):

    """many solutions"""

    height = 14
    width = 14

    svg_rotation = 30

    def coordinates(self):
        h = Triangular3DCoordSet(self.coordinates_elongated_hexagon(3, 2))
        coords = set(
            list(self.coordinates_hexagon(4, offset=(3,3,0)))
            + list(h.translate((9,5,0)))
            + list(h.rotate0(1).translate((9,-2,0)))
            + list(h.rotate0(2).translate((7,9,0))))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P7'][-1]['rotations'] = (0, 1)
        self.piece_data['P7'][-1]['flips'] = None
