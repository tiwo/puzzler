#!/usr/bin/env python
# $Id$

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2014 by David J. Goodger
# License: GPL 2 (see __init__.py)

"""
Concrete pentacube puzzles.
"""

from puzzler.puzzles import Puzzle3D, Puzzle2D
from puzzler.puzzles.polycubes import (
     SolidPentominoes, Pentacubes, PentacubesPlus, NonConvexPentacubes,
     Pentacubes3x3x3)
from puzzler.coordsys import Cartesian3DCoordSet


class Pentacubes5x7x7OpenBox(Pentacubes):

    """many solutions"""

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

    """many solutions"""

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


class Pentacubes18x3x3OpenBox(Pentacubes):

    """
    many solutions

    design from Kadon's Super Quintillions booklet
    """

    width = 3
    height = 18
    depth = 3

    def coordinates(self):
        coords = (
            set(self.coordinates_cuboid(3, 18, 3))
            - set(self.coordinates_cuboid(1, 17, 1, offset=(1,1,1))))
        return sorted(coords)


class Pentacubes2x7x15OpenBox(Pentacubes):

    """many solutions"""

    width = 7
    height = 15
    depth = 2

    transform_solution_matrix = Puzzle3D.cycle_xyz_transform

    def coordinates(self):
        return self.coordinates_open_box(self.width, self.height, self.depth)


class Pentacubes2x11x11Frame(Pentacubes):

    """many solutions"""

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

    """many solutions"""

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

    """many solutions"""

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

    """many solutions"""

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

    """many solutions"""

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
        self.piece_data['X5'][-1]['axes'] = None
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

    """many solutions"""

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

    """many solutions"""

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

    """many solutions"""

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

    """many solutions"""

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

    """many solutions"""

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

    """many solutions"""

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

    """many solutions"""

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

    """many solutions"""

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

    """many solutions"""

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


class PentacubesPyramidSpire(Pentacubes):

    """
    many solutions

    design from `Torsten Sillke's pages [1992]`_
    """

    width = 9
    height = 9
    depth = 9

    transform_solution_matrix = Puzzle3D.cycle_xyz_transform

    def coordinates(self):
        coords = set()
        for i in range(5):
            layer = Puzzle2D.coordinates_diamond(6 - i, offset=(i-1,i-1))
            for (x,y) in layer:
                coords.add(self.coordinate_offset(x, y, i, None))
        coords.update(set(self.coordinates_cuboid(1, 1, 9, offset=(4,4,0))))
        coords.intersection_update(set(self.coordinates_cuboid(9, 9, 9)))
        return sorted(coords)


class Pentacubes9x9x9OctahedralPlanes(Pentacubes):

    """
    0 solutions?

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

    """many solutions"""

    width = 13
    height = 13
    depth = 2

    def customize_piece_data(self):
        Pentacubes.customize_piece_data(self)
        self.piece_data['F5'][-1]['rotations'] = None

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if z * 4 <= abs(x - 6) + abs(y - 6) < 7:
                        yield (x, y, z)


class PentacubesDiamondPanel(Pentacubes):

    """many solutions"""

    width = 13
    height = 13
    depth = 2

    def coordinates(self):
        coords = set()
        for i in range(2):
            layer = Puzzle2D.coordinates_diamond(7 - i, offset=(i,i))
            for (x,y) in layer:
                coords.add(self.coordinate_offset(x, y, i, None))
        coords.remove((6,6,1))
        return sorted(coords)


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

    """many solutions"""

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

    """many solutions"""

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

    """many solutions"""

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


class PentacubesX1(Pentacubes):

    """many solutions"""

    width = 9
    height = 9
    depth = 5

    svg_rotation = 41.5

    def coordinates(self):
        coords = set(self.coordinates_cuboid(9, 3, 3, offset=(0,3,0)))
        coords.update(self.coordinates_cuboid(3, 9, 3, offset=(3,0,0)))
        coords.update(self.coordinates_cuboid(5, 1, 1, offset=(2,4,3)))
        coords.update(self.coordinates_cuboid(1, 5, 1, offset=(4,2,3)))
        coords.add(self.coordinate_offset(4, 4, 4, None))
        return sorted(coords)


class PentacubesAstroidBlock(Pentacubes):

    """many solutions"""

    width = 9
    height = 9
    depth = 5

    def coordinates(self):
        coords = set(
            list(self.coordinates_cuboid(9, 1, 5, offset=(0,4,0)))
            + list(self.coordinates_cuboid(1, 9, 5, offset=(4,0,0))))
        for x, y in Puzzle2D.coordinates_diamond(4, offset=(1,1)):
            for z in range(5):
                coords.add(self.coordinate_offset(x, y, z, None))
        return sorted(coords)


class PentacubesDiamondWall(Pentacubes):

    """
    many solutions

    design by Nick Maeder
    """

    width = 9
    height = 9
    depth = 5

    def coordinates(self):
        layer = (
            set(Puzzle2D.coordinates_diamond(5))
            - (set(Puzzle2D.coordinates_diamond(3, offset=(2,2)))
               - set(((4,4),))))
        coords = set(
            self.coordinate_offset(x, y, z, None)
            for x, y in layer for z in range(self.depth))
        return sorted(coords)


class PentacubesRibbedWall(Pentacubes):

    """
    0 solutions?

    design by Nick Maeder
    """

    width = 7
    height = 7
    depth = 5

    transform_solution_matrix = Puzzle3D.swap_yz_transform

    def coordinates(self):
        layer = (
            set(Puzzle2D.coordinates_rectangle(5, 5, offset=(1,1)))
            - (set(Puzzle2D.coordinates_rectangle(3, 3, offset=(2,2)))
               - set(((3,3),))))
        for i in (1, 3, 5):
            layer.update(((0,i), (i,0), (6,i), (i,6)))
        coords = set(
            self.coordinate_offset(x, y, z, None)
            for x, y in layer for z in range(5))
        return sorted(coords)


class PentacubesGrandPlatform(Pentacubes):

    """
    many solutions

    design from Kadon's Super Quintillions booklet
    """

    width = 9
    height = 9
    depth = 2

    transform_solution_matrix = Puzzle3D.cycle_xyz_transform

    def coordinates(self):
        coords = set(
            list(self.coordinates_cuboid(9, 9, 1))
            + list(self.coordinates_cuboid(8, 8, 1, offset=(0,0,1))))
        return sorted(coords)


class PentacubesSteppedPyramid1(Pentacubes):

    """many solutions"""

    width = 9
    height = 9
    depth = 5

    corner_offsets = ((0,0,0), (0,7,0), (7,0,0), (7,7,0))

    transform_solution_matrix = Puzzle3D.cycle_xyz_transform

    def coordinates(self):
        coords = set()
        for i in range(5):
            coords.update(set(
                self.coordinates_cuboid(9 - 2 * i, 9 - 2 * i, 1,
                                        offset=(i,i,i))))
        for offset in self.corner_offsets:
            coords.difference_update(set(
                self.coordinates_cuboid(2, 2, 5, offset=offset)))
        return sorted(coords)


class PentacubesSteppedPyramid2(Pentacubes):

    """many solutions"""

    width = 9
    height = 9
    depth = 5

    corner_offsets = ((2,2,0), (6,2,0), (6,6,0), (2,6,0))

    transform_solution_matrix = Puzzle3D.cycle_xyz_transform

    def coordinates(self):
        coords = set()
        for i in range(5):
            coords.update(set(
                self.coordinates_cuboid(9 - 2 * i, 9 - 2 * i, 1,
                                        offset=(i,i,i))))
        hole = Cartesian3DCoordSet(
            list(self.coordinates_cuboid(2, 2, 1))
            + [self.coordinate_offset(1, 1, 1, None)])
        for i, offset in enumerate(self.corner_offsets):
            coords.difference_update(
                hole.rotate0(i, 2).translate(offset))
        return sorted(coords)


class PentacubesSteppedPyramid3(PentacubesSteppedPyramid2):

    """many solutions"""

    corner_offsets = ((2,2,2), (6,2,2), (6,6,2), (2,6,2))


class PentacubesSteppedPyramid4(PentacubesSteppedPyramid2):

    """many solutions"""

    corner_offsets = ((1,1,1), (7,1,1), (7,7,1), (1,7,1))


class PentacubesSteppedPyramid5(Pentacubes):

    """many solutions"""

    width = 9
    height = 9
    depth = 5

    transform_solution_matrix = Puzzle3D.cycle_xyz_transform

    def coordinates(self):
        coords = set()
        for i in range(5):
            coords.update(set(
                self.coordinates_cuboid(9 - 2 * i, 9 - 2 * i, 1,
                                        offset=(i,i,i))))
        coords.difference_update(set(
            self.coordinates_cuboid(9, 1, 1, offset=(0,4,0))))
        coords.difference_update(set(
            self.coordinates_cuboid(1, 9, 1, offset=(4,0,0))))
        coords.difference_update(set(
            self.coordinates_cuboid(3, 3, 1, offset=(3,3,0))))
        coords.add(self.coordinate_offset(4, 4, 0, None))
        return sorted(coords)


class PentacubesSteppedPyramid6(Pentacubes):

    """many solutions"""

    width = 9
    height = 9
    depth = 5

    transform_solution_matrix = Puzzle3D.cycle_xyz_transform

    def coordinates(self):
        coords = set()
        for i in range(5):
            coords.update(set(
                self.coordinates_cuboid(9 - 2 * i, 9 - 2 * i, 1,
                                        offset=(i,i,i))))
        for d in (0, 1, 2, 6, 7, 8):
            for e in (0, 8):
                coords.discard(
                    self.coordinate_offset(e, d, 0, None))
                coords.discard(
                    self.coordinate_offset(d, e, 0, None))
        return sorted(coords)


class PentacubesSteppedPyramid_x1(Pentacubes):

    """0 solutions (inpossible due to corners)"""

    width = 9
    height = 9
    depth = 5

    transform_solution_matrix = Puzzle3D.cycle_xyz_transform

    def coordinates(self):
        coords = set()
        for i in range(5):
            coords.update(set(
                self.coordinates_cuboid(9 - 2 * i, 9 - 2 * i, 1,
                                        offset=(i,i,i))))
        for d in (0, 8):
            coords.difference_update(set(
                self.coordinates_cuboid(5, 1, 1, offset=(2,d,0))))
            coords.difference_update(set(
                self.coordinates_cuboid(1, 5, 1, offset=(d,2,0))))
        return sorted(coords)


class PentacubesCastle(Pentacubes):

    """
    many solutions

    design from Andrew Clarke's Poly Pages:
    http://www.recmath.com/PolyPages/PolyPages/index.htm?Polycubes.html#pentacubes
    """

    width = 7
    height = 7
    depth = 6

    transform_solution_matrix = Puzzle3D.swap_yz_transform

    def coordinates(self):
        coords = set(
            list(self.coordinates_cuboid(7, 7, 2))
            + list(self.coordinates_cuboid(3, 3, 4, offset=(2,2,2))))
        for i in (0, 2, 4, 6):
            for j in (0, 6):
                coords.add(self.coordinate_offset(i, j, 2, None))
                coords.add(self.coordinate_offset(j, i, 2, None))
        coords.remove(self.coordinate_offset(3, 3, 5, None))
        return sorted(coords)


class PentacubesSteppedPyramid11x7_1(Pentacubes):

    """
    many solutions

    design from `Torsten Sillke's pages [Problems for pentacubes 1992]
    <http://www.mathematik.uni-bielefeld.de/~sillke/CONTEST/pentaPRB>`_
    """

    width = 11
    height = 7
    depth = 4

    holes = set(((4,3,0), (5,3,0), (6,3,0)))

    transform_solution_matrix = Puzzle3D.swap_yz_transform

    def coordinates(self):
        coords = set()
        for i in range(self.depth):
            coords.update(set(self.coordinates_cuboid(
                self.width - 2 * i, self.height - 2 * i, 1, offset=(i,i,i))))
        coords -= self.holes
        return sorted(coords)


class PentacubesSteppedPyramid11x7_2(PentacubesSteppedPyramid11x7_1):

    """many solutions"""

    holes = set(((4,3,3), (5,3,3), (6,3,3)))


class PentacubesPanorama(Pentacubes):

    """
    many solutions

    design from `Torsten Sillke's pages [CFF Contest 36]
    <http://www.mathematik.uni-bielefeld.de/~sillke/CONTEST/cff-contest36>`_
    """

    width = 5
    height = 13
    depth = 5

    transform_solution_matrix = Puzzle3D.cycle_xyz_transform

    def coordinates(self):
        part = set()
        for i in range(self.depth):
            part.update(set((x,y,i) for (x, y) in
                Puzzle2D.coordinates_diamond(5 - i, offset=(i-2,i-2))))
        part = Cartesian3DCoordSet(part)
        part.intersection_update(set(self.coordinates_cuboid(5, 5, 5)))
        coords = part.copy()
        coords.update(part.translate((0,8,0)))
        part.intersection_update(
            set(self.coordinates_cuboid(3, 3, 3, offset=(1,1,2))))
        coords.update(part.translate((0,4,-2)))
        return sorted(coords)


class PentacubesCoolingFins(Pentacubes):

    """
    many solutions

    design from `Torsten Sillke's pages [10th Pentacube Contest, 1999]
    <http://www.mathematik.uni-bielefeld.de/~sillke/CONTEST/penta-contest>`_
    """

    width = 6
    height = 15
    depth = 2

    transform_solution_matrix = Puzzle3D.cycle_xyz_transform

    def coordinates(self):
        coords = set(
            self.coordinates_cuboid(self.width, self.height, self.depth))
        for y in range(1, 14, 2):
            coords -= set(self.coordinates_cuboid(5, 1, 1, offset=(1,y,1)))
        return sorted(coords)


class PentacubesDiamondTower(Pentacubes):

    """many solutions"""

    width = 7
    height = 7
    depth = 9

    transform_solution_matrix = Puzzle3D.swap_yz_transform

    def coordinates(self):
        coords = set(
            self.coordinate_offset(x, y, z, None)
            for x, y in Puzzle2D.coordinates_diamond(4) for z in range(5))
        for i in range(3):
            coords.update(set(
                self.coordinate_offset(x, y, i+5, None)
                for (x, y) in
                Puzzle2D.coordinates_diamond(3 - i, offset=(i+1,i+1))))
        coords.add(self.coordinate_offset(3, 3, 8, None))
        return sorted(coords)


class PentacubesCompoundCross1(Pentacubes):

    """
    0 solutions?

    design by Nick Maeder
    """

    width = 11
    height = 11
    depth = 5

    transform_solution_matrix = Puzzle3D.swap_yz_transform

    def coordinates(self):
        coords = set(
            list(self.coordinates_cuboid(11, 1, 5, offset=(0,5,0)))
            + list(self.coordinates_cuboid(1, 11, 5, offset=(5,0,0)))
            + list(self.coordinates_cuboid(3, 1, 5, offset=(4,2,0)))
            + list(self.coordinates_cuboid(3, 1, 5, offset=(4,8,0))) 
            + list(self.coordinates_cuboid(1, 3, 5, offset=(2,4,0))) 
            + list(self.coordinates_cuboid(1, 3, 5, offset=(8,4,0))))
        return sorted(coords)


class PentacubesCompoundCross2(Pentacubes):

    """0 solutions?"""

    width = 11
    height = 11
    depth = 5

    transform_solution_matrix = Puzzle3D.swap_yz_transform

    def coordinates(self):
        coords = set(
            list(self.coordinates_cuboid(11, 1, 5, offset=(0,5,0)))
            + list(self.coordinates_cuboid(1, 11, 5, offset=(5,0,0)))
            + list(self.coordinates_cuboid(3, 1, 5, offset=(4,1,0)))
            + list(self.coordinates_cuboid(3, 1, 5, offset=(4,9,0))) 
            + list(self.coordinates_cuboid(1, 3, 5, offset=(1,4,0))) 
            + list(self.coordinates_cuboid(1, 3, 5, offset=(9,4,0))))
        return sorted(coords)


class PentacubesOctagonalFrame1(Pentacubes):

    """
    many solutions

    design by Nick Maeder
    """

    width = 11
    height = 11
    depth = 2

    hole = (5,5,0)

    def coordinates(self):
        coords = set(self.coordinates_cuboid(11, 11, 2))
        cutout = Cartesian3DCoordSet(
            self.coordinate_offset(x, y, 0, None)
            for (x,y) in Puzzle2D.coordinates_diamond(3))
        for (x, y) in ((-2,-2), (-2,8), (8,-2), (8,8)):
            for z in (0,1):
                coords -= cutout.translate((x,y,z))
        for (x, y) in ((2,1), (2,5), (4,1), (4,5)):
            coords -= cutout.translate((x,y,1))
        coords -= set(self.coordinates_cuboid(9, 3, 1, offset=(1,4,1)))
        coords -= set(self.coordinates_cuboid(3, 9, 1, offset=(4,1,1)))
        coords.update(set(self.coordinates_cuboid(3, 3, 1, offset=(4,4,1))))
        coords.remove(self.hole)
        return sorted(coords)


class PentacubesOctagonalFrame2(PentacubesOctagonalFrame1):

    """many solutions"""

    hole = (5,5,1)


class PentacubesCornerSlant(Pentacubes):

    """
    0 solutions?

    design by Nick Maeder
    """

    width = 9
    height = 9
    depth = 9

    transform_solution_matrix = Puzzle3D.cycle_xyz_transform

    def coordinates(self):
        coords = set(self.coordinates_cuboid(9, 9, 1))
        for (tx, ty) in Puzzle2D.coordinates_triangle(8):
            coords.add(self.coordinate_offset(tx, 0, ty + 1, None))
            coords.add(self.coordinate_offset(0, tx, ty + 1, None))
        return sorted(coords)


class PentacubesPlus2x5x15(PentacubesPlus):

    """many solutions"""

    width = 15
    height = 5
    depth = 2

    transform_solution_matrix = Puzzle3D.swap_yz_transform


class PentacubesPlus2x3x25(PentacubesPlus):

    """many solutions"""

    width = 25
    height = 3
    depth = 2

    transform_solution_matrix = Puzzle3D.swap_yz_transform


class PentacubesPlus3x5x10(PentacubesPlus):

    """many solutions"""

    width = 10
    height = 5
    depth = 3

    transform_solution_matrix = Puzzle3D.swap_yz_transform


class PentacubesPlus5x5x6(PentacubesPlus):

    """many solutions"""

    width = 5
    height = 6
    depth = 5


class PentacubesPlus11x11x11OctahedralPlanes(PentacubesPlus):

    """
    0 solutions?

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


class PentacubesPlusDiamondPrism(PentacubesPlus):

    """many solutions"""

    width = 7
    height = 7
    depth = 6

    def coordinates(self):
        coords = set(
            self.coordinate_offset(x, y, z, None)
            for x, y in Puzzle2D.coordinates_diamond(4) for z in range(6))
        return sorted(coords)


class PentacubesPlusDiagonalWall1(PentacubesPlus):

    """many solutions"""

    width = 15
    height = 15
    depth = 2

    def coordinates(self):
        layer = (
            set(Puzzle2D.coordinates_triangle(15))
            - set(Puzzle2D.coordinates_triangle(9)))
        coords = set(
            self.coordinate_offset(x, y, z, None)
            for x, y in layer for z in range(2))
        return sorted(coords)

    transform_solution_matrix = Puzzle3D.cycle_xyz_transform


class PentacubesPlusDiagonalWall2(PentacubesPlus):

    """many solutions"""

    width = 8
    height = 8
    depth = 5

    def coordinates(self):
        layer = (
            set(Puzzle2D.coordinates_triangle(8))
            - set(Puzzle2D.coordinates_triangle(3)))
        coords = set(
            self.coordinate_offset(x, y, z, None)
            for x, y in layer for z in range(5))
        return sorted(coords)

    transform_solution_matrix = Puzzle3D.cycle_xyz_transform


class PentacubesPlusDiagonalWall3(PentacubesPlus):

    """many solutions"""

    width = 12
    height = 12
    depth = 2

    def coordinates(self):
        layer = (
            set(Puzzle2D.coordinates_triangle(12))
            - set(Puzzle2D.coordinates_triangle(2)))
        coords = set(
            self.coordinate_offset(x, y, z, None)
            for x, y in layer for z in range(2))
        return sorted(coords)

    transform_solution_matrix = Puzzle3D.cycle_xyz_transform


class PentacubesPlusDiagonalWall4(PentacubesPlus):

    """many solutions"""

    width = 12
    height = 12
    depth = 3

    def coordinates(self):
        layer = (
            set(Puzzle2D.coordinates_triangle(12))
            - set(Puzzle2D.coordinates_triangle(7)))
        coords = set(
            self.coordinate_offset(x, y, z, None)
            for x, y in layer for z in range(self.depth))
        return sorted(coords)

    transform_solution_matrix = Puzzle3D.cycle_xyz_transform


class PentacubesPlusDiagonalWall5(PentacubesPlus):

    """many solutions"""

    width = 9
    height = 9
    depth = 5

    def coordinates(self):
        layer = (
            set(Puzzle2D.coordinates_triangle(9))
            - set(Puzzle2D.coordinates_triangle(5)))
        coords = set(
            self.coordinate_offset(x, y, z, None)
            for x, y in layer for z in range(self.depth))
        return sorted(coords)

    transform_solution_matrix = Puzzle3D.cycle_xyz_transform


class PentacubesPlusDiagonalWall6(PentacubesPlus):

    """many solutions"""

    width = 11
    height = 11
    depth = 5

    def coordinates(self):
        layer = (
            set(Puzzle2D.coordinates_triangle(11))
            - set(Puzzle2D.coordinates_triangle(8)))
        coords = set(
            self.coordinate_offset(x, y, z, None)
            for x, y in layer for z in range(self.depth))
        return sorted(coords)

    transform_solution_matrix = Puzzle3D.cycle_xyz_transform


class PentacubesPlusDiagonalWall7(PentacubesPlus):

    """many solutions"""

    width = 7
    height = 7
    depth = 6

    def coordinates(self):
        layer = (
            set(Puzzle2D.coordinates_triangle(7))
            - set(Puzzle2D.coordinates_triangle(2)))
        coords = set(
            self.coordinate_offset(x, y, z, None)
            for x, y in layer for z in range(self.depth))
        return sorted(coords)

    transform_solution_matrix = Puzzle3D.cycle_xyz_transform


class PentacubesPlusDiagonalWall8(PentacubesPlus):

    """many solutions"""

    width = 6
    height = 6
    depth = 10

    def coordinates(self):
        layer = (
            set(Puzzle2D.coordinates_triangle(6))
            - set(Puzzle2D.coordinates_triangle(3)))
        coords = set(
            self.coordinate_offset(x, y, z, None)
            for x, y in layer for z in range(self.depth))
        return sorted(coords)

    transform_solution_matrix = Puzzle3D.cycle_xyz_transform


class PentacubesPlus5x5x10Steps(PentacubesPlus):

    """many solutions"""

    width = 10
    height = 5
    depth = 5

    def coordinates(self):
        coords = set(
            self.coordinate_offset(x, y, z, None)
            for y, z in Puzzle2D.coordinates_triangle(5) for x in range(10))
        return sorted(coords)


class PentacubesPlus9x5x6Steps(PentacubesPlus):

    """many solutions"""

    width = 6
    height = 9
    depth = 5

    transform_solution_matrix = Puzzle3D.swap_yz_transform

    def coordinates(self):
        coords = set(
            self.coordinate_offset(x, y, z, None)
            for y, z in Puzzle2D.coordinates_double_triangle(5)
            for x in range(6))
        return sorted(coords)


class PentacubesPlusDiagonalBlock1(PentacubesPlus):

    """many solutions"""

    width = 9
    height = 9
    depth = 2

    def coordinates(self):
        layer = set(
            (x, y) for (x, y) in Puzzle2D.coordinates_triangle(14)
            if x < self.width and y < self.height)
        coords = set(
            self.coordinate_offset(x, y, z, None)
            for x, y in layer for z in range(self.depth))
        return sorted(coords)

    transform_solution_matrix = Puzzle3D.cycle_xyz_transform


class PentacubesPlusSteppedPyramid1(PentacubesPlus):

    """many solutions"""

    width = 9
    height = 9
    depth = 3

    holes = set(((4,4,2), (3,4,2), (4,3,2), (5,4,2), (4,5,2)))

    transform_solution_matrix = Puzzle3D.cycle_xyz_transform

    def coordinates(self):
        coords = set()
        for i in range(3):
            coords.update(set(
                self.coordinates_cuboid(9 - 2 * i, 9 - 2 * i, 1,
                                        offset=(i,i,i))))
        coords -= self.holes
        return sorted(coords)


class PentacubesPlusSteppedPyramid2(PentacubesPlusSteppedPyramid1):

    """many solutions"""

    holes = set(((4,4,2), (2,2,2), (6,2,2), (2,6,2), (6,6,2)))


class NonConvexPentacubes2x5x14(NonConvexPentacubes):

    """many solutions"""

    width = 14
    height = 5
    depth = 2

    transform_solution_matrix = Puzzle3D.swap_yz_transform


class NonConvexPentacubes2x7x10(NonConvexPentacubes):

    """many solutions"""

    width = 10
    height = 7
    depth = 2

    transform_solution_matrix = Puzzle3D.swap_yz_transform


class NonConvexPentacubes4x5x7(NonConvexPentacubes):

    """many solutions"""

    width = 7
    height = 5
    depth = 4

    transform_solution_matrix = Puzzle3D.swap_yz_transform


class NonConvexPentacubesZigZag1(NonConvexPentacubes):

    """many solutions"""

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


class NonConvexPentacubesZigZag2(NonConvexPentacubes):

    """many solutions"""

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


class NonConvexPentacubesDiagonalWall(NonConvexPentacubes):

    """many solutions"""

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


class NonConvexPentacubesDiagonalWall2(NonConvexPentacubes):

    """many solutions"""

    width = 9
    height = 9
    depth = 4

    def coordinates(self):
        layer = (
            set(Puzzle2D.coordinates_triangle(9))
            - set(Puzzle2D.coordinates_triangle(4)))
        coords = set(
            self.coordinate_offset(x, y, z, None)
            for x, y in layer for z in range(self.depth))
        return sorted(coords)

    transform_solution_matrix = Puzzle3D.cycle_xyz_transform


class NonConvexPentacubesDiagonalWall3(NonConvexPentacubes):

    """many solutions"""

    width = 13
    height = 13
    depth = 2

    def coordinates(self):
        layer = (
            set(Puzzle2D.coordinates_triangle(13))
            - set(Puzzle2D.coordinates_triangle(6)))
        coords = set(
            self.coordinate_offset(x, y, z, None)
            for x, y in layer for z in range(self.depth))
        return sorted(coords)

    transform_solution_matrix = Puzzle3D.cycle_xyz_transform


class NonConvexPentacubesDiagonalWall4(NonConvexPentacubes):

    """many solutions"""

    width = 8
    height = 8
    depth = 4

    def coordinates(self):
        layer = (
            set(Puzzle2D.coordinates_triangle(8))
            - set(((0,0),)))
        coords = set(
            self.coordinate_offset(x, y, z, None)
            for x, y in layer for z in range(self.depth))
        return sorted(coords)

    transform_solution_matrix = Puzzle3D.cycle_xyz_transform


class NonConvexPentacubesDiagonalWall5(NonConvexPentacubes):

    """many solutions"""

    width = 6
    height = 6
    depth = 7

    def coordinates(self):
        layer = (
            set(Puzzle2D.coordinates_triangle(6))
            - set(((0,0),)))
        coords = set(
            self.coordinate_offset(x, y, z, None)
            for x, y in layer for z in range(self.depth))
        return sorted(coords)

    transform_solution_matrix = Puzzle3D.cycle_xyz_transform


class NonConvexPentacubesAztecPyramid(NonConvexPentacubes):

    """many solutions"""

    width = 10
    height = 10
    depth = 5

    def coordinates(self):
        return self.coordinates_aztec_pyramid(5)

    transform_solution_matrix = Puzzle3D.swap_yz_transform


class NonConvexPentacubesStackedSquares(NonConvexPentacubes):

    """many solutions"""

    width = 7
    height = 7
    depth = 7

    def coordinates(self):
        coords = set()
        for i in range(7):
            coords.update(set(
                self.coordinates_cuboid(7 - i, 7 - i, 1, offset=(0,i,i))))
        return sorted(coords)

    transform_solution_matrix = Puzzle3D.swap_yz_transform


class NonConvexPentacubes4x4x14Steps(PentacubesPlus):

    """0? solutions"""

    width = 14
    height = 4
    depth = 4

    def coordinates(self):
        coords = set(
            self.coordinate_offset(x, y, z, None)
            for y, z in Puzzle2D.coordinates_triangle(4) for x in range(14))
        return sorted(coords)


class NonConvexPentacubes7x7x5Steps(PentacubesPlus):

    """0? solutions"""

    width = 5
    height = 7
    depth = 7

    def coordinates(self):
        coords = set(
            self.coordinate_offset(x, y, z, None)
            for y, z in Puzzle2D.coordinates_triangle(7) for x in range(5))
        return sorted(coords)


class NonConvexPentacubesSteppedPyramid9x8(NonConvexPentacubes):

    """many solutions"""

    width = 9
    height = 8
    depth = 5

    holes = set()

    transform_solution_matrix = Puzzle3D.swap_yz_transform

    def coordinates(self):
        coords = set()
        for i in range(self.depth):
            coords.update(set(self.coordinates_cuboid(
                self.width - 2 * i, self.height - 2 * i, 1, offset=(i,i,i))))
        coords -= self.holes
        return sorted(coords)


class NonConvexPentacubesSteppedPyramid13x6(
    NonConvexPentacubesSteppedPyramid9x8):

    """many solutions"""

    width = 13
    height = 6
    depth = 3


class NonConvexPentacubesDiamondPyramid1(NonConvexPentacubes):

    """
    many solutions

    design from `Torsten Sillke's pages [1992]
    <http://www.mathematik.uni-bielefeld.de/~sillke/CONTEST/pentaPRB>`_
    """

    width = 13
    height = 13
    depth = 4

    transform_solution_matrix = Puzzle3D.swap_yz_transform

    def coordinates(self):
        coords = set()
        for i in range(self.depth):
            coords.update(set(
                self.coordinate_offset(x, y, i, None)
                for (x, y) in
                Puzzle2D.coordinates_diamond(7 - 2 * i, offset=(2*i,2*i))))
        return sorted(coords)


class NonConvexPentacubes5x5x8CrystalTower(NonConvexPentacubes):

    """many solutions"""

    width = 5
    height = 5
    depth = 8

    transform_solution_matrix = Puzzle3D.swap_yz_transform

    def coordinates(self):
        coords = set(self.coordinates_cuboid(5, 5, 4))
        for i in range(4):
            coords.update(set(
                self.coordinate_offset(x, y, i+4, None)
                for (x, y) in
                Puzzle2D.coordinates_diamond(4 - i, offset=(i-1,i-1))))
        coords.intersection_update(set(self.coordinates_cuboid(5, 5, 8)))
        return sorted(coords)


class NonConvexPentacubesOpenBox12x3x5(NonConvexPentacubes):

    """? solutions"""

    width = 3
    height = 12
    depth = 5

    transform_solution_matrix = Puzzle3D.cycle_xyz_transform

    def coordinates(self):
        return self.coordinates_open_box(self.width, self.height, self.depth)


class NonConvexPentacubesOpenBox10x3x6(NonConvexPentacubesOpenBox12x3x5):

    """? solutions"""

    width = 3
    height = 10
    depth = 6


class NonConvexPentacubesRingWall(NonConvexPentacubes):

    """0 solutions"""

    width = 6
    height = 6
    depth = 7

    transform_solution_matrix = Puzzle3D.swap_yz_transform

    def coordinates(self):
        return self.coordinates_ring_wall(self.width, self.height, self.depth)


class NonConvexPentacubesRingWall1(NonConvexPentacubes):

    """0 solutions"""

    width = 7
    height = 5
    depth = 7

    transform_solution_matrix = Puzzle3D.swap_yz_transform

    def coordinates(self):
        return self.coordinates_ring_wall(self.width, self.height, self.depth)


class NonConvexPentacubesRingWall8x4x7(NonConvexPentacubes):

    """1+ solutions"""

    width = 4
    height = 8
    depth = 7

    transform_solution_matrix = Puzzle3D.cycle_xyz_transform

    def coordinates(self):
        return self.coordinates_ring_wall(self.width, self.height, self.depth)


class NonConvexPentacubesRingWall3(NonConvexPentacubes):

    """0 solutions"""

    width = 9
    height = 3
    depth = 7

    transform_solution_matrix = Puzzle3D.swap_yz_transform

    def coordinates(self):
        return self.coordinates_ring_wall(self.width, self.height, self.depth)


class DorianCube(Pentacubes3x3x3):

    width = 5
    height = 5
    depth = 5
    
    def customize_piece_data(self):
        """Restrict the P piece to a single aspect."""
        Pentacubes3x3x3.customize_piece_data(self)
        self.piece_data['P5'][-1]['rotations'] = None
        self.piece_data['P5'][-1]['flips'] = None
        self.piece_data['P5'][-1]['axes'] = None
