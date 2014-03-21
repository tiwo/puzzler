#!/usr/bin/env python
# $Id$

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2012 by David J. Goodger
# License: GPL 2 (see __init__.py)

"""
Concrete hexiamonds puzzles.
"""

from puzzler.puzzles.polyiamonds import Hexiamonds, OneSidedHexiamonds
from puzzler.puzzles.polyhexes import Polyhexes
from puzzler.coordsys import Triangular3DCoordSet


class Hexiamonds3x12(Hexiamonds):

    """0 solutions"""

    height = 3
    width = 12

    check_for_duplicates = True
    duplicate_conditions = ({'rotate_180': True},)


class Hexiamonds4x9(Hexiamonds):

    """74 solutions"""

    height = 4
    width = 9

    check_for_duplicates = True
    duplicate_conditions = ({'rotate_180': True},)


class Hexiamonds6x6(Hexiamonds):

    """156 solutions"""

    height = 6
    width = 6

    check_for_duplicates = True
    duplicate_conditions = ({'rotate_180': True},
                            {'xy_swapped': True},
                            {'rotate_180': True, 'xy_swapped': True},)


class Hexiamonds4x11Trapezium(Hexiamonds):

    """76 solutions"""

    height = 4
    width = 11

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if x + y + z < self.width:
                        yield (x, y, z)

    def customize_piece_data(self):
        self.piece_data['I6'][-1]['flips'] = None


class Hexiamonds6x9Trapezium(Hexiamonds4x11Trapezium):

    """0 solutions (impossible due to parity)"""

    height = 6
    width = 9


class Hexiamonds4x10LongHexagon(Hexiamonds):

    """856 solutions"""

    height = 4
    width = 10

    check_for_duplicates = True
    duplicate_conditions = ({'rotate_180': True},)

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if 1 < x + y + z <= self.width + 1:
                        yield (x, y, z)

    def customize_piece_data(self):
        self.piece_data['I6'][-1]['flips'] = None


class Hexiamonds5x8StackedLongHexagons(Hexiamonds):

    """378 solutions"""

    height = 8
    width = 8

    check_for_duplicates = True
    duplicate_conditions = ({'rotate_180': True},)

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if 7 <= (2 * x + y + z) <= 15:
                        yield (x, y, z)

    def customize_piece_data(self):
        self.piece_data['I6'][-1]['flips'] = None


class Hexiamonds4x12StackedHexagons(Hexiamonds):

    """51 solutions"""

    height = 12
    width = 8

    check_for_duplicates = True
    duplicate_conditions = ({'rotate_180': True},)

    svg_rotation = 90

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    total = x + y + z
                    if (  (y < 4 and 4 <= x < 8 and 6 <= total < 10)
                          or (4 <= y < 8 and 2 <= x < 6 and 8 <= total < 12)
                          or (8 <= y and x < 4 and 10 <= total < 14)):
                        yield (x, y, z)

    def customize_piece_data(self):
        self.piece_data['I6'][-1]['flips'] = None


class Hexiamonds4x10LongButterfly(Hexiamonds):

    """0 solutions"""

    height = 4
    width = 12

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    total = x + y + z
                    if (  (total > 3 or x > 1)
                          and (total < self.width or x < 10)):
                        yield (x, y, z)


class Hexiamonds5x8StackedLongButterflies(Hexiamonds):

    """290 solutions"""

    height = 8
    width = 9

    check_for_duplicates = True
    duplicate_conditions = ({'rotate_180': True},)

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if 8 <= (2 * x + y + z) <= 16:
                        yield (x, y, z)

    def customize_piece_data(self):
        self.piece_data['I6'][-1]['flips'] = None


class Hexiamonds4x12StackedButterflies(Hexiamonds):

    """26 solutions"""

    height = 12
    width = 10

    check_for_duplicates = True
    duplicate_conditions = ({'rotate_180': True},)

    svg_rotation = 90

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    total = x + y + z
                    if (  (y < 2 and 6 <= x and total < 10)
                          or (2 <= y < 6 and 4 <= x < 8 and 8 <= total < 12)
                          or (6 <= y < 10 and 2 <= x < 6 and 10 <= total < 14)
                          or (10 <= y and x < 4 and 12 <= total)):
                        yield (x, y, z)

    def customize_piece_data(self):
        self.piece_data['I6'][-1]['flips'] = None


class HexiamondsSnowflake(Hexiamonds):

    """
    55 solutions

    Same as `Kadon's Iamond Hex <http://gamepuzzles.com/esspoly.htm#IH>`__.
    """

    height = 8
    width = 8

    def coordinates(self):
        exceptions = ((0,3,1), (0,4,0), (0,4,1), (0,5,0), (0,7,0), (0,7,1),
                      (1,7,0), (1,7,1), (2,1,1), (3,0,1), (3,1,0), (3,7,1),
                      (4,0,0), (4,6,1), (4,7,0), (5,6,0), (6,0,0), (6,0,1),
                      (7,0,0), (7,0,1), (7,2,1), (7,3,0), (7,3,1), (7,4,0))
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if ( 3 < x + y + z < self.width + self.height - 4
                         and (x, y, z) not in exceptions):
                        yield (x, y, z)

    def customize_piece_data(self):
        self.piece_data['J6'][-1]['rotations'] = None


class HexiamondsIamondHexSeparatedColors(HexiamondsSnowflake):

    """
    Solves the separated colors challenge of
    `Kadon's Iamond Hex <http://gamepuzzles.com/esspoly.htm#IH>`__.

    I bought one at G4G10 in March 2012.  The pieces come in three different
    colors.  An added challenge is to find solutions where no two pieces of
    the same color make contact along their edges.
    """

    piece_colors = {
        'H6': 'darkorange',
        'I6': 'darkorange',
        'S6': 'darkorange',
        'X6': 'darkorange',
        'C6': 'rgb(230,0,0)', # red
        'F6': 'rgb(230,0,0)',
        'G6': 'rgb(230,0,0)',
        'V6': 'rgb(230,0,0)',
        'E6': 'rgb(255,220,0)', # yellow
        'J6': 'rgb(255,220,0)',
        'O6': 'rgb(255,220,0)',
        'P6': 'rgb(255,220,0)',
        '0': 'gray',
        '1': 'black'}

    def record_solution(self, solution, *args, **kwargs):
        shapes = {}
        coordmap = {}
        for row in solution:
            name = row[-1]
            coords = Triangular3DCoordSet(tuple(
                int(c) for c in coordstr.split(',')) for coordstr in row[:-1])
            shapes[name] = coords
            for coord in coords:
                coordmap[coord] = name
        for name, coords in shapes.items():
            color = self.piece_colors[name]
            # find the neighbors of all coordinates in the shape:
            neighbors = set()
            for coord in coords:
                neighbors.update(coord.neighbors())
            # exclude the shape itself:
            neighbors.difference_update(coords)
            # restrict neighbors to coordinates inside the solution (tray):
            neighbors.intersection_update(self.solution_coords)
            for coord in neighbors:
                if self.piece_colors[coordmap[coord]] == color:
                    return False
        return HexiamondsSnowflake.record_solution(
            self, solution, *args, **kwargs)


class HexiamondsIamondHexJoinedColors(HexiamondsIamondHexSeparatedColors):

    """
    Solves the joined colors challenge of
    `Kadon's Iamond Hex <http://gamepuzzles.com/esspoly.htm#IH>`__.

    I bought one at G4G10 in March 2012.  The pieces come in three different
    colors.  An added challenge is to find solutions where all four pieces of
    each color make contact along their edges.
    """

    def record_solution(self, solution, *args, **kwargs):
        shapes = {}
        coordmap = {}
        for row in solution:
            name = row[-1]
            coords = Triangular3DCoordSet(tuple(
                int(c) for c in coordstr.split(',')) for coordstr in row[:-1])
            shapes[name] = coords
            for coord in coords:
                coordmap[coord] = name
        for name, coords in shapes.items():
            color = self.piece_colors[name]
            # find the neighbors of all coordinates in the shape:
            neighbors = set()
            for coord in coords:
                neighbors.update(coord.neighbors())
            # exclude the shape itself:
            neighbors.difference_update(coords)
            # restrict neighbors to coordinates inside the solution (tray):
            neighbors.intersection_update(self.solution_coords)
            for coord in neighbors:
                if self.piece_colors[coordmap[coord]] == color:
                    break
            else:
                return False
        # doesn't guarantee that *all 4* pieces are joined (could be two
        # joined pairs), but good enough
        return HexiamondsSnowflake.record_solution(
            self, solution, *args, **kwargs)


class HexiamondsRing(Hexiamonds):

    """
    0 solutions

    8-unit high hexagon with a central 4-unit hexagonal hole.
    """

    height = 8
    width = 8

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if ( 3 < x + y + z < 12
                         and not (1 < x < 6 and 1 < y < 6
                                  and 5 < x + y + z < 10)):
                        yield (x, y, z)


class HexiamondsRing2(Hexiamonds):

    """
    11 solutions

    8-unit high hexagon with a 4-unit hexagonal hole offset one unit from the
    center.
    """

    height = 8
    width = 8

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if ( 3 < x + y + z < 12
                         and not (2 < x < 7 and 1 < y < 6
                                  and 6 < x + y + z < 11)):
                        yield (x, y, z)

    def customize_piece_data(self):
        self.piece_data['I6'][-1]['flips'] = None


class HexiamondsHexagon3(Hexiamonds):

    """0 solutions"""

    height = 8
    width = 8

    def coordinates(self):
        hole = set()
        for z in range(self.depth):
            for y in range(2, 6):
                for x in range(2, 6):
                    if 5 < x + y + z < 10:
                        hole.add((x,y,z))
        for coord in ((1,5,1), (2,3,0), (4,1,1), (6,2,0), (5,4,1), (3,6,0)):
            hole.add(coord)
        for coord in ((2,4,0), (3,2,1), (5,2,0), (5,3,1), (4,5,0), (2,5,1)):
            hole.remove(coord)
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if 3 < x + y + z < 12 and (x,y,z) not in hole:
                        yield (x, y, z)


class HexiamondsHexagon4(Hexiamonds):

    """0 solutions"""

    height = 8
    width = 8

    def coordinates(self):
        hole = set()
        for z in range(self.depth):
            for y in range(2):
                for x in range(2):
                    for bx,by in ((1,4), (3,3), (4,1), (4,4)):
                        if 0 < x + y + z < 3:
                            hole.add((x + bx, y + by, z))
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if 3 < x + y + z < 12 and (x,y,z) not in hole:
                        yield (x, y, z)


class HexiamondsHexagon5(Hexiamonds):

    """0 solutions"""

    height = 8
    width = 8

    def coordinates(self):
        hole = set()
        for z in range(self.depth):
            for y in range(2, 6):
                for x in range(2, 6):
                    if 5 < x + y + z < 10:
                        hole.add((x,y,z))
        for coord in ((1,4,1), (1,5,0), (4,5,1), (5,5,0), (5,1,0), (5,1,1)):
            hole.add(coord)
        for coord in ((2,5,0), (2,5,1), (5,3,1), (5,4,0), (3,2,1), (4,2,0)):
            hole.remove(coord)
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if 3 < x + y + z < 12 and (x,y,z) not in hole:
                        yield (x, y, z)


class HexiamondsHexagon6(Hexiamonds):

    """0 solutions"""

    height = 8
    width = 8

    def coordinates(self):
        hole = set()
        for z in range(self.depth):
            for y in range(2, 6):
                for x in range(2, 6):
                    if 5 < x + y + z < 10:
                        hole.add((x,y,z))
        for coord in ((1,4,1), (2,3,0), (4,5,1), (3,6,0), (5,1,1), (6,2,0)):
            hole.add(coord)
        for coord in ((2,5,0), (2,5,1), (5,3,1), (5,4,0), (3,2,1), (4,2,0)):
            hole.remove(coord)
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if 3 < x + y + z < 12 and (x,y,z) not in hole:
                        yield (x, y, z)


class HexiamondsCrescent(Hexiamonds):

    """
    87 solutions

    8-unit high hexagon with a 4-unit hexagonal bite removed from one corner.
    """

    height = 8
    width = 8

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if ( 3 < x + y + z < 12
                         and not (x > 3 and 1 < y < 6 and 7 < x + y + z)):
                        yield (x, y, z)

    def customize_piece_data(self):
        self.piece_data['I6'][-1]['flips'] = None


class HexiamondsCrescent2(Hexiamonds):

    """
    2 solutions

    8-unit high hexagon with a 4-unit hexagonal bite removed from one side.
    """

    height = 8
    width = 8

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if ( 3 < x + y + z < 12
                         and not (2 < x < 7 and 2 < y < 7 and 7 < x + y + z)):
                        yield (x, y, z)

    def customize_piece_data(self):
        self.piece_data['I6'][-1]['flips'] = None


class HexiamondsTrefoil(Hexiamonds):

    """640 solutions"""

    height = 8
    width = 8

    def coordinates(self):
        for z in range(self.depth):
            for y in range(2, 6):
                for x in range(4):
                    if 3 < x + y + z <= 7:
                        yield (x, y, z)
            for y in range(4):
                for x in range(4, 8):
                    if 5 < x + y + z <= 9:
                        yield (x, y, z)
            for y in range(4, 8):
                for x in range(2, 6):
                    if 7 < x + y + z <= 11:
                        yield (x, y, z)

    def customize_piece_data(self):
        self.piece_data['I6'][-1]['rotations'] = None
        self.piece_data['I6'][-1]['flips'] = None


class Hexiamonds3Hexagons(Hexiamonds):

    """0 solutions"""

    height = 4
    width = 12

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(4):
                    if 1 < x + y + z <= 5:
                        yield (x, y, z)
                for x in range(4, 8):
                    if 5 < x + y + z <= 9:
                        yield (x, y, z)
                for x in range(8, 12):
                    if 9 < x + y + z <= 13:
                        yield (x, y, z)


class HexiamondsCoin(Hexiamonds):

    """304 solutions"""

    height = 6
    width = 8

    check_for_duplicates = True
    duplicate_conditions = ({'rotate_180': True},)

    def coordinates(self):
        hole = set(((3,2,1), (3,3,0), (3,3,1), (4,2,0), (4,2,1), (4,3,0)))
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if ( 2 < x + y + z <= 10
                         and not (x, y, z) in hole):
                        yield (x, y, z)

    def customize_piece_data(self):
        self.piece_data['I6'][-1]['flips'] = None


class HexiamondsIrregularHexagon7x8(Hexiamonds):

    """
    5885 solutions.

    Suggested by Dan Klarskov, under the name 'hexui'.
    """

    height = 8
    width = 7

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if 1 < x + y + z < 9:
                        yield (x, y, z)

    def customize_piece_data(self):
        self.piece_data['I6'][-1]['flips'] = None


class HexiamondsStackedChevrons_6x6(Hexiamonds):

    """
    933 solutions.

    Suggested by Dan Klarskov, under the name 'polyam2'.
    """

    height = 6
    width = 9

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if self.height <= (2 * x + y + z) < (self.width * 2):
                        yield (x, y, z)

    def customize_piece_data(self):
        self.piece_data['I6'][-1]['flips'] = None


class HexiamondsStackedChevrons_12x3_1(Hexiamonds):

    """269 solutions."""

    height = 12
    width = 9

    svg_rotation = 90

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if 11 <= (2 * x + y + z) < 17:
                        yield (x, y, z)

    def customize_piece_data(self):
        self.piece_data['I6'][-1]['flips'] = None


class HexiamondsStackedChevrons_12x3_2(Hexiamonds):

    """114 solutions."""

    height = 12
    width = 9

    svg_rotation = 90

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    total = x + y + z
                    if (  (y < 2 and 6 <= total < 9)
                          or (2 <= y < 4 and 4 <= x < 7)
                          or (4 <= y < 6 and 8 <= total < 11)
                          or (6 <= y < 8 and 2 <= x < 5)
                          or (8 <= y < 10 and 10 <= total < 13)
                          or (y >= 10 and x < 3)):
                        yield (x, y, z)

    def customize_piece_data(self):
        self.piece_data['I6'][-1]['flips'] = None


class HexiamondsStackedChevrons_12x3_3(Hexiamonds):

    """46 solutions."""

    height = 12
    width = 9

    svg_rotation = 90

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    total = x + y + z
                    if (  (y < 3 and 6 <= total < 9)
                          or (3 <= y < 6 and 3 <= x < 6)
                          or (6 <= y < 9 and 9 <= total < 12)
                          or (y >= 9 and x < 3)):
                        yield (x, y, z)

    def customize_piece_data(self):
        self.piece_data['I6'][-1]['flips'] = None


class HexiamondsChevron(Hexiamonds):

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
        self.piece_data['I6'][-1]['flips'] = None


class HexiamondsChevron_4x9(HexiamondsChevron):

    """142 solutions."""

    height = 4
    width = 11


class HexiamondsChevron_6x6(HexiamondsChevron):

    """1004 solutions."""

    height = 6
    width = 9


class HexiamondsChevron_12x3(HexiamondsChevron):

    """29 solutions."""

    height = 12
    width = 9

    svg_rotation = 90


class HexiamondsV_9x9(Hexiamonds):

    """0 solutions"""

    height = 9
    width = 9

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    total = x + y + z
                    if (  self.width <= total
                          and not (y > 5 and x < 6 and total > 11)):
                        yield (x, y, z)


class HexiamondsTriangleRing_x(Hexiamonds):

    """0 solutions"""

    height = 9
    width = 9

    def coordinates(self):
        return sorted(
            set(self.coordinates_triangle(9))
            - set(self.coordinates_triangle(3, offset=(2,2,0))))


class HexiamondsTenyo(Hexiamonds):

    """
    4968 solutions.

    This is the puzzle that is sold by Tenyo Inc., Japan, in their `"PlaPuzzle"
    line`__ (`details`__).

    __ http://www.tenyo.co.jp/pp/
    __ http://www.tenyo.co.jp/pp/pz04/index.html
    """

    height = 8
    width = 7

    svg_rotation = 90

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    xyz = x + y + z
                    if (  ((xyz > 4) or (x > 0 and xyz > 3))
                          and ((xyz < 9) or (x < 6 and xyz < 10)
                               or (x < 5 and xyz < 11))):
                        yield (x, y, z)

    def customize_piece_data(self):
        self.piece_data['I6'][-1]['flips'] = None


class HexiamondsTwoTriangles(Hexiamonds):

    """0 solutions"""

    height = 6
    width = 7

    def coordinates(self):
        for coord in self.coordinates_parallelogram(7, 6):
            x, y, z = coord
            total = x + y + z
            if total <= 5 or total >= 7:
                yield coord


class HexiamondsX1(Hexiamonds):

    """11 solutions"""

    height = 8
    width = 11

    holes = set((
        (3,7,1), (5,4,0), (5,3,1), (7,0,0),
        (0,7,1), (6,7,1), (4,0,0), (10,0,0)))

    def coordinates(self):
        for coord in self.coordinates_butterfly(7, 4):
            if coord not in self.holes:
                yield coord

    def customize_piece_data(self):
        self.piece_data['P6'][-1]['rotations'] = (0, 1, 2)
        self.piece_data['P6'][-1]['flips'] = None


class HexiamondsX_x1(HexiamondsX1):

    """
    0 solutions:

    holes = set(
        tuple(Hexiamonds.coordinates_butterfly(2, 1, offset=(4,3,0)))
        + ((3,7,1), (7,0,0)))

    holes = set((
        (3,7,1), (4,6,0), (4,5,1), (5,4,0), (5,3,1), (6,2,0), (6,1,1), (7,0,0)))

    holes = set((
        (3,7,1), (5,4,0), (5,3,1), (7,0,0), (2,6,1), (5,6,1), (5,1,0), (8,1,0)))
    """


class HexiamondsX_x2(Hexiamonds):

    """0 solutions"""

    height = 10
    width = 15

    holes = set((
        (2,9,1), (3,8,1), (3,9,0), (3,9,1), (4,7,1), (4,8,0),
        (4,8,1), (4,9,0), (4,9,1), (7,0,0), (7,0,1), (7,1,0),
        (7,1,1), (7,2,0), (8,0,0), (8,0,1), (8,1,0), (9,0,0)))

    def coordinates(self):
        for coord in self.coordinates_butterfly(7, 5):
            if coord not in self.holes:
                yield coord


class HexiamondsSpikedHexagon1(Hexiamonds):

    """
    4 solutions

    Design from Andrew Clarke's Poly Pages:
    http://recmath.org/PolyPages/PolyPages/index.htm?Polyiamonds.htm
    """

    width = 10
    height = 10

    def coordinates(self):
        x = Triangular3DCoordSet(self.coordinates_butterfly(2, 1))
        coords = set(
            list(self.coordinates_hexagon(3, offset=(2,2,0)))
            + list(x.translate((0,4,0)))
            + list(x.rotate0(1).translate((6,6,0)))
            + list(x.rotate0(2).translate((11,0,0))))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P6'][-1]['rotations'] = (0, 1)
        self.piece_data['P6'][-1]['flips'] = None


class HexiamondsSpikedHexagon2(Hexiamonds):

    """3 solutions"""

    width = 8
    height = 8

    svg_rotation = -30

    def coordinates(self):
        x = Triangular3DCoordSet(self.coordinates_parallelogram(2, 2))
        coords = set(
            list(self.coordinates_hexagon(3, offset=(1,1,0)))
            + list(x.translate((6,0,0)))
            + list(x.rotate0(1).translate((2,2,0)))
            + list(x.rotate0(2).translate((6,6,0))))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P6'][-1]['rotations'] = (0, 1)
        self.piece_data['P6'][-1]['flips'] = None


class HexiamondsSpikedHexagon_x1(Hexiamonds):

    """0 solutions"""

    width = 8
    height = 8

    offsets = ((3,7,0), (1,6,0), (2,3,0), (5,1,0), (7,2,0), (6,5,0),)

    offsets = ((5,0,0), (8,1,0), (7,5,0), (3,8,0), (0,7,0), (1,3,0))

    def coordinates(self):
        spike = Triangular3DCoordSet(self.coordinates_trapezoid(2, 1))
        coords = set(self.coordinates_hexagon(3, offset=(1,1,0)))
        for steps, offset in enumerate(self.offsets):
            coords.update(spike.rotate0(steps).translate(offset))
        return sorted(coords)


class HexiamondsSpikedHexagon_x2(Hexiamonds):

    """0 solutions"""

    width = 8
    height = 8

    offsets = ((1,7,0), (1,4,0), (4,1,0), (7,1,0), (7,4,0), (4,7,0),)

    def coordinates(self):
        spike = Triangular3DCoordSet(
            self.coordinate_offset(x, 0, 0, None) for x in range(3))
        coords = set(self.coordinates_hexagon(3, offset=(1,1,0)))
        for steps, offset in enumerate(self.offsets):
            coords.update(spike.rotate0(steps).translate(offset))
        return sorted(coords)


class Hexiamonds4x3SemiregularHexagon(Hexiamonds):

    """
    710 solutions

    Design from `Wolfram Mathworld
    <http://mathworld.wolfram.com/HexiamondTiling.html>`__.
    """

    width = 7
    height = 7

    holes = set(((3,3,0),))

    def coordinates(self):
        coords = set(self.coordinates_semiregular_hexagon(4, 3)) - self.holes
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P6'][-1]['rotations'] = (0, 1)
        self.piece_data['P6'][-1]['flips'] = None


class HexiamondsHeart(Hexiamonds):

    """
    4,154 solutions

    Design by Dan Klarskov
    """

    width = 7
    height = 8

    svg_rotation = -90

    def coordinates(self):
        coords = (
            set(self.coordinates_elongated_hexagon(3, 4))
            - set(self.coordinates_hexagon(2, offset=(5,2,0))))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['I6'][-1]['flips'] = None


class HexiamondsSpinner1(Hexiamonds):

    """751 solutions"""

    width = 8
    height = 8

    def coordinates(self):
        x = Triangular3DCoordSet(self.coordinates_parallelogram(3, 1))
        coords = set(
            list(self.coordinates_hexagon(3, offset=(1,1,0)))
            + list(x.translate((4,0,0)))
            + list(x.rotate0(2).translate((8,4,0)))
            + list(x.rotate0(4).translate((0,8,0))))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P6'][-1]['rotations'] = (0, 1)


class HexiamondsSpinner_x1(Hexiamonds):

    """0 solutions"""

    width = 12
    height = 12

    def coordinates(self):
        x = Triangular3DCoordSet(self.coordinates_parallelogram(4, 2))
        coords = set(
            list(self.coordinates_hexagon(2, offset=(4,4,0)))
            + list(x.translate((8,4,0)))
            + list(x.rotate0(2).translate((6,8,0)))
            + list(x.rotate0(4).translate((4,6,0))))
        return sorted(coords)


class HexiamondsSpinner_x2(Hexiamonds):

    """0 solutions"""

    width = 8
    height = 8

    def coordinates(self):
        x = Triangular3DCoordSet(self.coordinates_parallelogram(2, 2))
        coords = set(
            list(self.coordinates_hexagon(2, offset=(2,2,0)))
            + list(x.translate((6,2,0)))
            + list(x.rotate0(1).translate((6,4,0)))
            + list(x.rotate0(2).translate((4,6,0)))
            + list(x.rotate0(3).translate((2,6,0)))
            + list(x.rotate0(4).translate((2,4,0)))
            + list(x.rotate0(5).translate((4,2,0))))
        return sorted(coords)


class HexiamondsSpinner_x3(Hexiamonds):

    """0 solutions"""

    width = 10
    height = 10

    def coordinates(self):
        x = Triangular3DCoordSet(self.coordinates_parallelogram(3, 2))
        coords = set(
            list(self.coordinates_triangle(6, offset=(2,2,0)))
            + list(x.translate((2,0,0)))
            + list(x.rotate0(2).translate((10,2,0)))
            + list(x.rotate0(4).translate((0,10,0))))
        return sorted(coords)


class HexiamondsHexgrid4x3(Hexiamonds):

    """142 solutions"""

    width = 7
    height = 9

    svg_rotation = 30

    def coordinates(self):
        hcoords = set(Polyhexes.coordinates_parallelogram(4, 3))
        coords = self.coordinates_hexgrid(hcoords)
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P6'][-1]['rotations'] = (0, 1, 2)


class HexiamondsHexgridTrapezoid5x3(Hexiamonds):

    """144 solutions"""

    width = 8
    height = 8

    svg_rotation = 30

    def coordinates(self):
        hcoords = set(Polyhexes.coordinates_trapezoid(5, 3))
        coords = self.coordinates_hexgrid(hcoords)
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P6'][-1]['flips'] = None


class HexiamondsHexgridSemiregularHexagon3x2(Hexiamonds):

    """103 solutions"""

    width = 8
    height = 8

    svg_rotation = 30

    def coordinates(self):
        hcoords = set(Polyhexes.coordinates_semiregular_hexagon(3, 2))
        coords = self.coordinates_hexgrid(hcoords, offset=(0,-1,0))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P6'][-1]['flips'] = None
        self.piece_data['P6'][-1]['rotations'] = (0, 1)


class HexiamondsHexgrid6x2_x(Hexiamonds):

    """0 solutions"""

    width = 8
    height = 9

    def coordinates(self):
        hcoords = set(Polyhexes.coordinates_parallelogram(6, 2))
        coords = self.coordinates_hexgrid(hcoords)
        return sorted(coords)


class HexiamondsHexgridHexagonRing_x(Hexiamonds):

    """0 solutions"""

    width = 10
    height = 10

    def coordinates(self):
        hcoords = (
            set(Polyhexes.coordinates_hexagon(3, offset=(0,-1)))
            - set(Polyhexes.coordinates_hexagon(2, offset=(1,0))))
        coords = self.coordinates_hexgrid(hcoords)
        return sorted(coords)


class HexiamondsHexgridHexagramRing_x(Hexiamonds):

    """0 solutions"""

    width = 8
    height = 8

    def coordinates(self):
        hcoords = (
            set(Polyhexes.coordinates_hexagram(2, offset=(-1,-1)))
            - set(Polyhexes.coordinates_hexagon(1, offset=(1,1))))
        coords = self.coordinates_hexgrid(hcoords)
        return sorted(coords)


class HexiamondsHexgridTriangleRing_x1(Hexiamonds):

    """0 solutions"""

    width = 10
    height = 10

    def coordinates(self):
        hcoords = (
            set(Polyhexes.coordinates_triangle(5))
            - set(Polyhexes.coordinates_triangle(2, offset=(1,1))))
        coords = self.coordinates_hexgrid(hcoords)
        return sorted(coords)


class HexiamondsHexgridTriangleRing_x2(Hexiamonds):

    """0 solutions"""

    width = 10
    height = 10

    def coordinates(self):
        hcoords = set(Polyhexes.coordinates_triangle(5))
        hex = Triangular3DCoordSet(self.coordinates_hexagon(1))
        coords = (
            set(self.coordinates_hexgrid(hcoords))
            - hex.translate((3,4,0))
            - hex.translate((4,5,0))
            - hex.translate((5,3,0)))
        return sorted(coords)


class HexiamondsChoose9Hexagon(Hexiamonds):

    """
    Abstract base class for puzzles that use 9 of the 12 hexiamonds to form an
    regular hexagon of side length 3.

    Naively, there are (12 choose 9) = 220 different sets of 9 hexiamonds.
    However, to form a regular hexagon, an equal number of 'up' and 'down'
    triangles are necessary. The F6 & P6 hexiamonds are unbalanced (two 'up'
    triangles and four 'down', or vice-versa), while all other hexiamonds are
    balanced (three of each). So puzzles must either include or exclude both
    F6 & P6.

    Therefore there are actually (10 choose 3) + (10 choose 1) = 120 + 10 =
    130 possible hexiamond subsets for these puzzles.
    """

    # list the pieces to omit:
    omit = ()

    # one piece must be fixed, to prevent duplicates:
    fixed = 'P6'

    width = 6
    height = 6

    def coordinates(self):
        return self.coordinates_hexagon(3)

    def customize_piece_data(self):
        self.piece_data[self.fixed][-1]['flips'] = (1,) # per the original
        self.piece_data[self.fixed][-1]['rotations'] = None
        for name in self.omit:
            del self.piece_data[name]


class HexiamondsHexicator(HexiamondsChoose9Hexagon):

    """
    1 solution

    Col. George Sicherman's 'Hexicator' puzzle
    (http://userpages.monmouth.com/~colonel/hexicator/hexicator.html),
    consisting of 9 hexiamonds to be formed into a regular hexagon (side
    length 3).  The club/crook (J6), pistol/signpost (H6), and shoe/hook (G6)
    pieces are omitted from the puzzle.
    """

    omit = ['J6', 'H6', 'G6']


class HexiamondsChoose9Hexagon2(HexiamondsChoose9Hexagon):

    """
    9 solutions

    The pieces omitted from this puzzle are the three hexiamonds that cannot
    be formed with two triamonds: E6/crown, H6/pistol/signpost, and
    V6/lobster.

    Suggested by Michael Spencer on 2013-11-24:

        My local cafe has a wooden hexiamond puzzle that I thought might
        interest you. It is very similar to one puzzle you mention
        (http://userpages.monmouth.com/~colonel/hexicator/hexicator.html) but
        instead of omitting the G, H and J pieces it omits E, H and V (in
        other words, precisely those pieces that cannot be formed from two
        triamonds). I am now very curious to know how many solutions this
        version has!
    """

    omit = ['E6', 'H6', 'V6']


class HexiamondsChoose9Hexagon3(HexiamondsChoose9Hexagon):

    """
    15 solutions

    The pieces omitted from this puzzle are the three hexiamonds that cannot
    be formed with three diamonds: F6/yacht, P6/sphinx, and X6/butterfly.
    """

    omit = ['F6', 'P6', 'X6']

    fixed = 'J6'


class OneSidedHexiamondsOBeirnesHexagon(OneSidedHexiamonds):

    """
    124,519 solutions, agrees with Knuth.

    Split into 7 sub-puzzles by the distance of the small-hexagon piece (O6)
    from the center of the puzzle.

    O'Beirne's Hexagon consists of 19 small 6-triangle hexagons, arranged in a
    hexagon like a honeycomb (12 small hexagons around 6 around 1); equivalent
    to Polyhexes.coordinates_hexagon(3).
    """

    height = 10
    width = 10

    check_for_duplicates = True
    duplicate_conditions = ({'standardize': 'P6'},
                            {'standardize': 'p6'},)

    @classmethod
    def components(cls):
        return (OneSidedHexiamondsOBeirnesHexagon_A,
                OneSidedHexiamondsOBeirnesHexagon_B,
                OneSidedHexiamondsOBeirnesHexagon_C,
                OneSidedHexiamondsOBeirnesHexagon_D,
                OneSidedHexiamondsOBeirnesHexagon_E,
                OneSidedHexiamondsOBeirnesHexagon_F,
                OneSidedHexiamondsOBeirnesHexagon_G,)

    def coordinates(self):
        bumps = set((
            (0,6,1), (0,7,0), (0,7,1), (9,2,0), (9,2,1), (9,3,0),
            (6,0,1), (7,0,0), (7,0,1), (2,9,0), (2,9,1), (3,9,0),
            (2,3,0), (2,2,1), (3,2,0), (6,7,1), (7,7,0), (7,6,1)))
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if (  (5 < (x + y + z) < 14) and (0 < x < 9) and (0 < y < 9)
                          or (x,y,z) in bumps):
                        yield (x, y, z)

    def build_matrix(self):
        """"""
        keys = sorted(self.pieces.keys())
        o_coords, o_aspect = self.pieces['O6'][0]
        for coords in self.O6_offsets:
            translated = o_aspect.translate(coords)
            self.build_matrix_row('O6', translated)
        keys.remove('O6')
        self.build_regular_matrix(keys)


class OneSidedHexiamondsOBeirnesHexagon_A(OneSidedHexiamondsOBeirnesHexagon):

    """1914 solutions."""

    O6_offsets = ((4,4,0),)

    def customize_piece_data(self):
        OneSidedHexiamondsOBeirnesHexagon.customize_piece_data(self)
        # one sphinx pointing up, to eliminate duplicates & reduce searches:
        self.piece_data['P6'][-1]['rotations'] = None


class OneSidedHexiamondsOBeirnesHexagon_B(OneSidedHexiamondsOBeirnesHexagon):

    """5727 solutions."""

    O6_offsets = ((5,4,0),)


class OneSidedHexiamondsOBeirnesHexagon_C(OneSidedHexiamondsOBeirnesHexagon):

    """11447 solutions."""

    O6_offsets = ((3,6,0),)


class OneSidedHexiamondsOBeirnesHexagon_D(OneSidedHexiamondsOBeirnesHexagon):

    """7549 solutions."""

    O6_offsets = ((6,4,0),)


class OneSidedHexiamondsOBeirnesHexagon_E(OneSidedHexiamondsOBeirnesHexagon):

    """6675 solutions."""

    O6_offsets = ((3,7,0),)


class OneSidedHexiamondsOBeirnesHexagon_F(OneSidedHexiamondsOBeirnesHexagon):

    """15717 solutions."""

    O6_offsets = ((7,4,0),)


class OneSidedHexiamondsOBeirnesHexagon_G(OneSidedHexiamondsOBeirnesHexagon):

    """75490 solutions."""

    O6_offsets = ((2,8,0),)


class OneSidedHexiamonds_TestHexagon(OneSidedHexiamonds):

    """Used to test the 'standardize' duplicate condition."""

    height = 6
    width = 6

    _test_pieces = set(['I6', 'P6', 'J6', 'V6', 'C6', 'O6'])

    symmetric_pieces = 'V6 C6 O6'.split()
    """Pieces with reflexive symmetry, identical to their mirror images."""

    asymmetric_pieces = 'I6 P6 J6'.split()
    """Pieces without reflexive symmetry, different from their mirror images."""

    check_for_duplicates = True

    duplicate_conditions = ({'standardize': 'P6'},
                            {'standardize': 'p6'})

    @classmethod
    def components(cls):
        return (OneSidedHexiamonds_TestHexagon_A,
                OneSidedHexiamonds_TestHexagon_B)

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if 3 <= (x + y + z) < 9:
                        yield (x, y, z)

    def build_matrix(self):
        """"""
        keys = sorted(self.pieces.keys())
        o_coords, o_aspect = self.pieces['O6'][0]
        for coords in self.O6_offsets:
            translated = o_aspect.translate(coords)
            self.build_matrix_row('O6', translated)
        keys.remove('O6')
        self.build_regular_matrix(keys)

    def customize_piece_data(self):
        for key in self.piece_data.keys():
            if key not in self._test_pieces:
                del self.piece_data[key]
        OneSidedHexiamonds.customize_piece_data(self)


class OneSidedHexiamonds_TestHexagon_A(OneSidedHexiamonds_TestHexagon):

    O6_offsets = ((1,4,0), (2,4,0), (2,3,0),)


class OneSidedHexiamonds_TestHexagon_B(OneSidedHexiamonds_TestHexagon):

    O6_offsets = ((2,2,0),)

    def customize_piece_data(self):
        OneSidedHexiamonds_TestHexagon.customize_piece_data(self)
        # one sphinx pointing up, to eliminate duplicates & reduce searches:
        self.piece_data['P6'][-1]['rotations'] = None
#         ## doesn't work (omits valid solutions):
#         #self.piece_data['C6'][-1]['rotations'] = (0,2,4)


class OneSidedHexiamondsLongHexagon8x3(OneSidedHexiamonds):

    """Many solutions."""

    height = 6
    width = 11

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if 2 < x + y + z <= 13:
                        yield (x, y, z)


class OneSidedHexiamondsButterfly11x3(OneSidedHexiamonds):

    """Many solutions."""

    height = 6
    width = 14

    def coordinates(self):
        return self.coordinates_butterfly(11, 3)


class OneSidedHexiamonds19x3(OneSidedHexiamonds):

    """0 solutions."""

    height = 3
    width = 19


class OneSidedHexiamondsHexgridElongatedHexagon6x2(OneSidedHexiamonds):

    """many solutions"""

    width = 10
    height = 11

    svg_rotation = 30

    def coordinates(self):
        hcoords = set(Polyhexes.coordinates_elongated_hexagon(6, 2))
        coords = set(self.coordinates_hexgrid(hcoords, offset=(0,-1,0)))
        return sorted(coords)


class OneSidedHexiamondsHexgridTrapezoid10x2(OneSidedHexiamonds):

    """many solutions"""

    width = 12
    height = 12

    svg_rotation = 30

    def coordinates(self):
        hcoords = set(Polyhexes.coordinates_trapezoid(10, 2))
        coords = set(self.coordinates_hexgrid(hcoords))
        return sorted(coords)


class OneSidedHexiamondsHexgridButterfly4x4(OneSidedHexiamonds):

    """many solutions"""

    width = 14
    height = 8

    def coordinates(self):
        hcoords = set(Polyhexes.coordinates_butterfly(4, 4))
        coords = set(self.coordinates_hexgrid(hcoords, offset=(0,-6,0)))
        return sorted(coords)


class OneSidedHexiamondsHexgridTriangle1(OneSidedHexiamonds):

    """many solutions"""

    width = 12
    height = 12

    svg_rotation = 30

    def coordinates(self):
        hcoords = set(
            list(Polyhexes.coordinates_trapezoid(6, 4))
            + [Polyhexes.coordinate_offset(0, 5, None)])
        coords = self.coordinates_hexgrid(hcoords)
        return sorted(coords)


class OneSidedHexiamondsHexgridTwoTriangles(OneSidedHexiamonds):

    """many solutions"""

    width = 20
    height = 12

    svg_rotation = 30

    def coordinates(self):
        hcoords = set(
            list(Polyhexes.coordinates_triangle(4))
            + list(Polyhexes.coordinates_triangle(4, offset=(3,0))))
        coords = self.coordinates_hexgrid(hcoords)#, offset=(0,-1,0))
        return sorted(coords)


class OneSidedHexiamondsTriangle12_x1(OneSidedHexiamonds):

    """0 solutions"""

    height = 12
    width = 12

    def coordinates(self):
        coords = set(self.coordinates_triangle(12))
        for offset in ((1,1,0), (1,2,0), (2,1,0)):
            coords -= set(self.coordinates_inverted_triangle(4, offset=offset))
        return sorted(coords)


class OneSidedHexiamondsTriangle12_x2(OneSidedHexiamonds):

    """0 solutions"""

    height = 12
    width = 12

    def coordinates(self):
        coords = set(self.coordinates_triangle(12))
        for offset in ((2,3,0), (3,2,0), (3,3,0)):
            coords -= set(self.coordinates_triangle(4, offset=offset))
        return sorted(coords)


class OneSidedHexiamondsTriangle12_x3(OneSidedHexiamonds):

    """0 solutions"""

    height = 12
    width = 12

    def coordinates(self):
        coords = set(self.coordinates_triangle(12))
        coords -= set(self.coordinates_triangle(6, offset=(2,2,0)))
        coords.update(set(self.coordinates_hexagon(1, offset=(3,3,0))))
        return sorted(coords)


class OneSidedHexiamondsTriangle12_x4(OneSidedHexiamonds):

    """0 solutions"""

    height = 12
    width = 12

    def coordinates(self):
        coords = set(self.coordinates_triangle(12))
        coords -= set(self.coordinates_inverted_triangle(6))
        coords.update(set(self.coordinates_hexagon(1, offset=(3,3,0))))
        return sorted(coords)


class OneSidedHexiamondsTriangle_x1(OneSidedHexiamonds):

    """0 solutions"""

    height = 11
    width = 11

    holes = set(((2,2,0), (2,6,0), (6,2,0)))
    holes = set(((1,4,1), (4,1,1), (4,4,1)))
    holes = set(((2,4,0), (4,2,0), (4,4,0)))
    holes = set(((2,2,1), (2,5,1), (5,2,1)))
    holes = set(((2,4,1), (3,2,1), (4,3,1)))

    def coordinates(self):
        coords = (
            set(self.coordinates_triangle(11))
            - set(self.coordinates_triangle(2, offset=(3,3,0))))
        coords -= self.holes
        return sorted(coords)


class OneSidedHexiamondsTriangleRing1(OneSidedHexiamonds):

    """0 solutions"""

    height = 10
    width = 10

    def coordinates(self):
        coords = set(self.coordinates_semiregular_hexagon(9, 1))
        coords -= set(self.coordinates_triangle(2, offset=(3,3,0)))
        return sorted(coords)


class OneSidedHexiamondsCompoundTriangle_x1(OneSidedHexiamonds):

    """0 solutions"""

    height = 10
    width = 10

    def coordinates(self):
        coords = set()
        for offset in ((0,1,0), (1,0,0), (1,1,0)):
            coords.update(set(self.coordinates_triangle(9, offset=offset)))
        coords -= set(((3,3,1),))
        return sorted(coords)


class OneSidedHexiamondsTrefoil1(OneSidedHexiamonds):

    """many solutions"""

    height = 11
    width = 11

    def coordinates(self):
        coords = set(self.coordinates_semiregular_hexagon(
            1, 4, offset=(1,1,0)))
        part = Triangular3DCoordSet(self.coordinates_elongated_hexagon(1, 3))
        for i, offset in enumerate(((0,5,0), (11,-3,0), (7,0,0))):
            coords.update(part.rotate0(i).translate(offset))
        return sorted(coords)


class OneSidedHexiamondsTrefoil2(OneSidedHexiamonds):

    """0 solutions"""

    height = 10
    width = 10

    svg_rotation = 30

    def coordinates(self):
        coords = set(self.coordinates_hexagon(3, offset=(2,2,0)))
        for offset in ((0,6,0), (3,0,0), (6,3,0)):
            coords.update(set(self.coordinates_hexagon(2, offset=offset)))
        for offset in ((1,4,0), (4,7,0), (7,1,0)):
            coords.update(set(self.coordinates_hexagon(1, offset=offset)))
        return sorted(coords)


class OneSidedHexiamondsTrefoil3(OneSidedHexiamonds):

    """many solutions"""

    height = 10
    width = 10

    svg_rotation = 30

    def coordinates(self):
        coords = set()
        part = Triangular3DCoordSet(
            list(self.coordinates_hexagon(2, offset=(0,1,0)))
            + list(self.coordinates_elongated_hexagon(1, 3, offset=(1,0,0))))
        for i, offset in enumerate(((5,2,0), None, (8,5,0), None, (2,8,0))):
            if not offset:
                continue
            coords.update(part.rotate0(i).translate(offset))
        return sorted(coords)


class OneSidedHexiamondsTrefoil4(OneSidedHexiamonds):

    """many solutions"""

    height = 12
    width = 12

    holes = set(((5,1,1), (5,2,0)))

    svg_rotation = 30

    def coordinates(self):
        coords = set()
        part = (
            Triangular3DCoordSet(self.coordinates_elongated_hexagon(4, 2))
            - self.holes)
        for i, offset in enumerate(((6,4,0), None, (8,6,0), None, (4,8,0))):
            if not offset:
                continue
            coords.update(part.rotate0(i).translate(offset))
        return sorted(coords)


class OneSidedHexiamondsTrefoil5(OneSidedHexiamondsTrefoil4):

    """many solutions"""

    holes = set(((4,3,0), (5,0,1)))


class OneSidedHexiamondsTrefoil6(OneSidedHexiamondsTrefoil4):

    """many solutions"""

    holes = set(((3,3,1), (5,0,0)))


class OneSidedHexiamondsTrefoil7(OneSidedHexiamondsTrefoil4):

    """many solutions"""

    holes = set(((2,3,1), (4,0,0)))


class OneSidedHexiamondsTrefoil8(OneSidedHexiamondsTrefoil4):

    """many solutions"""

    holes = set(((1,3,1), (3,0,0)))


class OneSidedHexiamondsTrefoil9(OneSidedHexiamondsTrefoil4):

    """many solutions"""

    holes = set(((0,3,1), (2,0,0)))


class OneSidedHexiamondsTrefoil10(OneSidedHexiamondsTrefoil4):

    """many solutions"""

    holes = set(((0,2,1), (1,1,0)))


class OneSidedHexiamondsTrefoil11(OneSidedHexiamondsTrefoil4):

    """many solutions"""

    holes = set(((0,2,0), (0,1,1)))


class OneSidedHexiamondsTrefoil_x1(OneSidedHexiamonds):

    """0 solutions"""

    height = 9
    width = 9

    def coordinates(self):
        coords = set()
        for offset in ((0,2,0), (2,0,0), (2,2,0)):
            coords.update(set(self.coordinates_semiregular_hexagon(
                6, 1, offset=offset)))
        return sorted(coords)


class OneSidedHexiamondsTrefoil_x2(OneSidedHexiamonds):

    """0 solutions"""

    height = 12
    width = 12

    def coordinates(self):
        coords = set(self.coordinates_inverted_triangle(3, offset=(4,4,0)))
        for offset in ((0,0,0), (0,6,0), (6,0,0)):
            coords.update(set(self.coordinates_inverted_triangle(
                6, offset=offset)))
        return sorted(coords)


class OneSidedHexiamondsTrefoil_x3(OneSidedHexiamonds):

    """0 solutions"""

    height = 11
    width = 11

    def coordinates(self):
        coords = set(self.coordinates_hexagon(2, offset=(3,3,0)))
        for offset in ((0,0,0), (0,6,0), (6,0,0)):
            coords.update(set(self.coordinates_semiregular_hexagon(
                1, 4, offset=offset)))
        return sorted(coords)


class OneSidedHexiamondsTrefoil_x4(OneSidedHexiamonds):

    """0 solutions"""

    height = 11
    width = 11

    def coordinates(self):
        coords = set(self.coordinates_inverted_triangle(6))
        part = Triangular3DCoordSet(
            list(self.coordinates_parallelogram(3, 3, offset=(0,1,0)))
            + list(self.coordinates_parallelogram(3, 3, offset=(1,0,0))))
        for i, offset in enumerate(((0,0,0), (4,4,0), (12,0,0))):
            coords.update(part.rotate0(i).translate(offset))
        return sorted(coords)


class OneSidedHexiamondsTrefoil_x5(OneSidedHexiamonds):

    """0 solutions"""

    height = 12
    width = 12

    def coordinates(self):
        coords = set(self.coordinates_inverted_triangle(6))
        part = Triangular3DCoordSet(self.coordinates_parallelogram(4, 4))
        for i, offset in enumerate(((0,0,0), (4,4,0), (12,0,0))):
            coords.update(part.rotate0(i).translate(offset))
        coords -= set(self.coordinates_hexagon(1, offset=(3,3,0)))
        return sorted(coords)


class OneSidedHexiamondsTrefoil_x6(OneSidedHexiamonds):

    """0 solutions"""

    height = 12
    width = 12

    def coordinates(self):
        coords = set(self.coordinates_hexagon(2, offset=(4,4,0)))
        for offset in ((0,6,0), (6,0,0), (6,6,0)):
            coords.update(set(self.coordinates_triangle(6, offset=offset)))
        coords -= set(self.coordinates_hexagon(1, offset=(5,5,0)))
        return sorted(coords)


class OneSidedHexiamondsTrefoil_x7(OneSidedHexiamondsTrefoil4):

    """0 solutions"""

    holes = set(((0,3,0), (1,0,1)))


class OneSidedHexiamondsBumpyTriangle(OneSidedHexiamonds):

    """many solutions"""

    height = 10
    width = 10

    svg_rotation = 30

    def coordinates(self):
        coords = set()
        for offset in ((0,6,0), (3,0,0), (6,3,0)):
            coords.update(set(self.coordinates_hexagon(2, offset=offset)))
        for offset in ((1,3,0), (2,1,0), (3,2,0)):
            coords.update(set(self.coordinates_hexagon(3, offset=offset)))
        return sorted(coords)


class OneSidedHexiamondsTabbedHexagon(OneSidedHexiamonds):

    """many solutions"""

    height = 10
    width = 10

    offsets = ((0,7,0), (1,3,0), (3,8,0), (5,0,0), (7,5,0), (8,1,0))

    def coordinates(self):
        coords = set(self.coordinates_hexagon(4, offset=(1,1,0)))
        for offset in self.offsets:
            coords.update(set(self.coordinates_hexagon(1, offset=offset)))
        return sorted(coords)


class OneSidedHexiamondsNotchedHexagonRing(OneSidedHexiamonds):

    """many solutions"""

    height = 10
    width = 10

    def coordinates(self):
        coords = set(
            list(self.coordinates_semiregular_hexagon(6, 3, offset=(1,1,0)))
            + list(self.coordinates_semiregular_hexagon(3, 6)))
        coords -= set(self.coordinates_hexagon(2, offset=(3,3,0)))
        return sorted(coords)


class OneSidedHexiamondsKnobbedHexagon1(OneSidedHexiamonds):

    """many solutions"""

    height = 10
    width = 10

    holes = set(OneSidedHexiamonds.coordinates_hexagon(1, offset=(4,4,0)))

    def coordinates(self):
        coords = set(self.coordinates_hexagon(4, offset=(1,1,0)))
        for offset in ((0,4,0), (0,8,0), (4,0,0), (4,8,0), (8,0,0), (8,4,0)):
            coords.update(set(self.coordinates_hexagon(1, offset=offset)))
        coords -= self.holes
        return sorted(coords)


class OneSidedHexiamondsKnobbedHexagon_x1(OneSidedHexiamondsKnobbedHexagon1):

    """0 solutions"""

    holes = set(((3,5,1), (4,4,0), (4,6,0), (5,3,1), (5,5,1), (6,4,0)))
    holes = set(((2,6,0), (3,3,1), (3,7,1), (6,2,0), (6,6,0), (7,3,1)))
    holes = set(((1,6,1), (3,3,0), (3,8,0), (6,1,1), (6,6,1), (8,3,0)))
