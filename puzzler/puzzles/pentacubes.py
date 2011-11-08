#!/usr/bin/env python
# $Id$

"""
Concrete pentacube puzzles.
"""

from puzzler.puzzles import Puzzle3D
from puzzler.puzzles.polycubes import (
     SolidPentominoes, Pentacubes, PentacubesPlus, NonConvexPentacubes)


class Pentacubes5x7x7OpenBox(Pentacubes):

    """ solutions"""

    width = 7
    height = 7
    depth = 5

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if ( z == 0 or x == 0 or x == self.width - 1
                         or y == 0 or y == self.height - 1):
                        yield (x, y, z)

    transform_solution_matrix = Puzzle3D.swap_yz_transform


class Pentacubes3x9x9OpenBox(Pentacubes):

    """ solutions"""

    width = 9
    height = 9
    depth = 3

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if ( z == 0 or x == 0 or x == self.width - 1
                         or y == 0 or y == self.height - 1):
                        yield (x, y, z)

    transform_solution_matrix = Puzzle3D.swap_yz_transform


class Pentacubes2x11x11Frame(Pentacubes):

    """ solutions"""

    width = 11
    height = 11
    depth = 2

    def coordinates(self):
        for y in range(self.height):
            for x in range(self.width):
                yield (x, y, 0)
        for y in range(2, self.height - 2):
            for x in range(2, self.width - 2):
                if ( x == 2 or x == self.width - 3
                     or y == 2 or y == self.height - 3):
                    yield (x, y, 1)

    transform_solution_matrix = Puzzle3D.swap_yz_transform


class Pentacubes5x5x6Tower1(Pentacubes):

    """ solutions"""

    width = 5
    height = 6
    depth = 5

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if y == 5 and x == 2:
                        continue
                    yield (x, y, z)


class Pentacubes5x5x6Tower2(Pentacubes):

    """ solutions"""

    width = 5
    height = 6
    depth = 5

    def coordinates(self):
        hole = set(((2,5,2), (2,5,1), (1,5,2), (3,5,2), (2,5,3)))
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if (x,y,z) not in hole:
                        yield (x, y, z)


class Pentacubes5x5x6Tower3(Pentacubes):

    """ solutions"""

    width = 5
    height = 6
    depth = 5

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if y > 0 and z == 2 == x:
                        continue
                    yield (x, y, z)


class PentacubesCornerCrystal(Pentacubes):

    """ solutions"""

    width = 10
    height = 10
    depth = 10

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    total = x + y + z
                    if ( total < 6
                         or total < 10 and (x == 0 or y == 0 or z == 0)):
                        yield (x, y, z)

    def customize_piece_data(self):
        """
        Add a monocube to fill in the extra space, and restrict the X piece to
        one orientation to account for symmetry.
        """
        Pentacubes.customize_piece_data(self)
        self.piece_data['o'] = ((), {})
        self.piece_data['X'][-1]['axes'] = None
        self.piece_colors['o'] = 'white'

    def build_matrix(self):
        """Restrict the monocube to the 4 interior, hidden spaces."""
        keys = sorted(self.pieces.keys())
        o_coords, o_aspect = self.pieces['o'][0]
        for coords in ((1,1,1), (2,1,1), (1,2,1), (1,1,2)):
            translated = o_aspect.translate(coords)
            self.build_matrix_row('o', translated)
        keys.remove('o')
        self.build_regular_matrix(keys)


class PentacubesNineSlices(Pentacubes):

    """ solutions"""

    width = 9
    height = 9
    depth = 5

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if ( 3 < x + y < 13 and -5 < y - x < 5
                         and (z + abs(x - 4)) < 5):
                        yield (x, y, z)

    transform_solution_matrix = Puzzle3D.swap_yz_transform


class PentacubesGreatWall(Pentacubes):

    """ solutions"""

    width = 15
    height = 15
    depth = 5

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if x % 2:
                        if x + y == 13:
                            yield (x, y, z)
                    elif 11 < x + y < 15:
                        yield (x, y, z)

    transform_solution_matrix = Puzzle3D.cycle_xyz_transform


class Pentacubes3x3x20Tower1(Pentacubes):

    """ solutions"""

    width = 3
    height = 20
    depth = 3

    def coordinates(self):
        holes = set()
        for y in range(1, 19, 2):
            for z in range(3):
                holes.add((1,y,z))
        for z in range(self.depth):
            for y in range(self.height - 1):
                for x in range(self.width):
                    if (x,y,z) not in holes:
                        yield (x, y, z)
        yield (1, 19, 1)


class Pentacubes3x3x20Tower2(Pentacubes):

    """ solutions"""

    width = 3
    height = 20
    depth = 3

    def coordinates(self):
        holes = set()
        for y in range(1, 19, 2):
            for i in range(3):
                if (y // 2) % 2:
                    holes.add((i,y,1))
                else:
                    holes.add((1,y,i))
        for z in range(self.depth):
            for y in range(self.height - 1):
                for x in range(self.width):
                    if (x,y,z) not in holes:
                        yield (x, y, z)
        yield (1, 19, 1)


class Pentacubes3x3x17Tower(Pentacubes):

    """ solutions"""

    width = 3
    height = 17
    depth = 3

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height - 1):
                for x in range(self.width):
                    yield (x, y, z)
        yield (1, 16, 1)


class Pentacubes3x3x19CrystalTower(Pentacubes):

    """ solutions"""

    width = 3
    height = 19
    depth = 3

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height - 1):
                for x in range(self.width):
                    if x + y + z < 18:
                        yield (x, y, z)
        yield (0, 18, 0)


class Pentacubes5x9x9Fortress(Pentacubes):

    """ solutions"""

    width = 9
    height = 9
    depth = 5

    def coordinates(self):
        for y in range(self.height):
            for x in range(self.width):
                yield (x, y, 0)
        for z in range(1, self.depth):
            for i in range(self.height):
                if z <= abs(i - 4):
                    yield (0, i, z)
                    yield (8, i, z)
                    if 0 < i < self.width - 1:
                        yield (i, 0, z)
                        yield (i, 8, z)

    transform_solution_matrix = Puzzle3D.swap_yz_transform


class Pentacubes3x9x9Mound(Pentacubes):

    """ solutions"""

    width = 9
    height = 9
    depth = 3

    def coordinates(self):
        coords = set()
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if (  z <= x < (self.width - z)
                          and z <= y < (self.height - z)
                          and not (4 - z < x < 4 + z and 4 - z < y < 4 + z)):
                        yield (x, y, z)


class Pentacubes11x11x6Pyramid(Pentacubes):

    """
    One empty cube in the center of the bottom layer.

    0 solutions

    Proof of impossibility: Color the cubes of the 29 pentacubes with a 3-D
    black & white checkerboard pattern, such that no like-colored faces touch.
    Each pentacube piece has an imbalance of one, except for X and T1, which
    both have imbalances of 3.  Therefore the maximum possible imbalance of
    any puzzle is 33.  Now color the 11x11x6 pyramid with the same
    checkerboard pattern.  The imbalance is 37 (91 cubes of one color vs. 54
    of the other), more than the maximum possible imbalance.  Even if the
    empty cube is moved, the imbalance could only be reduced to 35, which is
    still too large.  No solution is possible.

    Instead of black & white, the coordinate total (X + Y + Z) of each cube
    could be used, divided into even & odd totals.
    """

    width = 11
    height = 11
    depth = 6

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if (x,y,z) == (5,5,0):
                        continue
                    elif z + abs(x - 5) + abs(y - 5) < self.depth:
                        yield (x, y, z)

    transform_solution_matrix = Puzzle3D.swap_yz_transform


class Pentacubes11x11x5Pyramid(Pentacubes):

    """ solutions"""

    width = 11
    height = 11
    depth = 5

    def coordinates(self):
        corners = set(((0,2),(0,1),(0,0),(1,0),(2,0),
                       (8,0),(9,0),(10,0),(10,1),(10,2),
                       (10,8),(10,9),(10,10),(9,10),(8,10),
                       (2,10),(1,10),(0,10),(0,9),(0,8)))
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if ( z == 0 and (x,y) not in corners
                         or z + abs(x - 5) + abs(y - 5) < self.depth):
                        yield (x, y, z)


class Pentacubes9x9x9OctahedralPlanes(Pentacubes):

    """
     solutions

    Even/odd imbalance: 23.
    """

    width = 9
    height = 9
    depth = 9

    def coordinates(self):
        coords = set()
        for i in range(self.depth):
            for j in range(self.height):
                if abs(i - 4) + abs(j - 4) < 6:
                    coords.add((i, j, 4))
                    coords.add((i, 4, j))
                    coords.add((4, i, j))
        return sorted(coords)


class Pentacubes2x13x13DiamondFrame(Pentacubes):

    """ solutions"""

    width = 13
    height = 13
    depth = 2

    def customize_piece_data(self):
        Pentacubes.customize_piece_data(self)
        self.piece_data['F'][-1]['rotations'] = None

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if z * 4 <= abs(x - 6) + abs(y - 6) < 7:
                        yield (x, y, z)


class Pentacubes2x3x2Chair(Pentacubes):

    """
    A structure made of only two pieces.

    17 solutions
    """

    width = 2
    height = 3
    depth = 2

    check_for_duplicates = True

    duplicate_conditions = ({'x_reversed': True},)

    custom_class_name = 'Pentacubes2x3x2Chair_%(p1)s_%(p2)s'
    custom_class_template = """\
class %s(Pentacubes2x3x2Chair):
    custom_pieces = [%%(p1)r, %%(p2)r]
""" % custom_class_name

    @classmethod
    def components(cls):
        """
        Generate subpuzzle classes dynamically.
        One class for each pair of pieces.
        """
        piece_names = sorted(SolidPentominoes.piece_data.keys()
                             + cls.non_planar_piece_data.keys())
        classes = []
        for i, p1 in enumerate(piece_names):
            for p2 in piece_names[i+1:]: # avoid duplicate combinations
                exec cls.custom_class_template % locals()
                classes.append(locals()[cls.custom_class_name % locals()])
        return classes

    def coordinates(self):
        for coord in ((0,0,0), (1,0,0), (0,1,0), (1,1,0), (0,2,0), (1,2,0),
                      (0,0,1), (1,0,1), (0,1,1), (1,1,1)):
            yield coord

    def customize_piece_data(self):
        """Restrict pieces to those listed in `self.custom_pieces`."""
        Pentacubes.customize_piece_data(self)
        for name in self.piece_data.keys():
            if name not in self.custom_pieces:
                del self.piece_data[name]


class Pentacubes5x7x5Cubbyholes(Pentacubes):

    """ solutions"""

    width = 5
    height = 7
    depth = 5

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if not (x % 2 and y % 2):
                        yield (x, y, z)


class Pentacubes9x9x5Cubbyholes(Pentacubes):

    """ solutions"""

    width = 9
    height = 9
    depth = 5

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if 5 < (x + y) < 11 and not (x % 2 and y % 2):
                        yield (x, y, z)


class Pentacubes7x7x5Block(Pentacubes):

    """ solutions"""

    width = 7
    height = 7
    depth = 5

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if 1 <= x <= 5 and 1 <= y <= 5 or x == 3 or y == 3:
                        yield (x, y, z)

    transform_solution_matrix = Puzzle3D.swap_yz_transform


class PentacubesPlus2x5x15(PentacubesPlus):

    """ solutions"""

    width = 15
    height = 5
    depth = 2

    transform_solution_matrix = Puzzle3D.swap_yz_transform


class PentacubesPlus2x3x25(PentacubesPlus):

    """ solutions"""

    width = 25
    height = 3
    depth = 2

    transform_solution_matrix = Puzzle3D.swap_yz_transform


class PentacubesPlus3x5x10(PentacubesPlus):

    """ solutions"""

    width = 10
    height = 5
    depth = 3

    transform_solution_matrix = Puzzle3D.swap_yz_transform


class PentacubesPlus5x5x6(PentacubesPlus):

    """ solutions"""

    width = 5
    height = 6
    depth = 5


class PentacubesPlus11x11x11OctahedralPlanes(PentacubesPlus):

    """
     solutions

    Even/odd imbalance: 30.
    """

    width = 11
    height = 11
    depth = 11

    def coordinates(self):
        coords = set()
        for i in range(self.depth):
            for j in range(self.height):
                if i == j == 5:
                    continue
                if abs(i - 5) + abs(j - 5) < 6:
                    coords.add((i, j, 5))
                    coords.add((i, 5, j))
                    coords.add((5, i, j))
        return sorted(coords)


class NonConvexPentacubes2x5x14(NonConvexPentacubes):

    """ solutions"""

    width = 14
    height = 5
    depth = 2

    transform_solution_matrix = Puzzle3D.swap_yz_transform


class NonConvexPentacubes2x7x10(NonConvexPentacubes):

    """ solutions"""

    width = 10
    height = 7
    depth = 2

    transform_solution_matrix = Puzzle3D.swap_yz_transform


class NonConvexPentacubes4x5x7(NonConvexPentacubes):

    """ solutions"""

    width = 7
    height = 5
    depth = 4

    transform_solution_matrix = Puzzle3D.swap_yz_transform


class PentacubesZigZag1(NonConvexPentacubes):

    """ solutions"""

    width = 18
    height = 19
    depth = 2

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if 8 <= (int(x/2) + int(y/2)) <= 9:
                        yield (x, y, z)

    transform_solution_matrix = Puzzle3D.cycle_xyz_transform


class PentacubesZigZag2(NonConvexPentacubes):

    """ solutions"""

    width = 20
    height = 18
    depth = 2

    check_for_duplicates = True

    duplicate_conditions = ({'x_reversed': True, 'y_reversed': True},)

    def coordinates(self):
        ends = set([(0,16), (19,1)])
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if (x,y) in ends:
                        continue
                    if 8 <= (int(x/2) + int(y/2)) <= 9:
                        yield (x, y, z)

    transform_solution_matrix = Puzzle3D.cycle_xyz_transform


class PentacubesDiagonalWall(NonConvexPentacubes):

    """0? solutions"""

    width = 19
    height = 19
    depth = 2

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if 18 <= (x + y) <= 21:
                        yield (x, y, z)

    transform_solution_matrix = Puzzle3D.cycle_xyz_transform
