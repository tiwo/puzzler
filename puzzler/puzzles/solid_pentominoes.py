#!/usr/bin/env python
# $Id$

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2015 by David J. Goodger
# License: GPL 2 (see __init__.py)

"""
Concrete solid pentomino puzzles.
"""

from puzzler.puzzles import Puzzle3D, Puzzle2D
from puzzler.puzzles.polycubes import SolidPentominoes
from puzzler.coordsys import Cartesian3D


class SolidPentominoes2x3x10(SolidPentominoes):

    """12 solutions"""

    height = 3
    width = 10
    depth = 2

    def customize_piece_data(self):
        self.piece_data['F'][-1]['flips'] = None

    def build_matrix(self):
        keys = sorted(self.pieces.keys())
        for x_coords, x_aspect in self.pieces['X']:
            if not x_aspect.bounds[-1]: # get the one in the XY plane
                break
        for x in range(4):
            translated = x_aspect.translate((x, 0, 0))
            self.build_matrix_row('X', translated)
        keys.remove('X')
        self.build_regular_matrix(keys)

    transform_solution_matrix = Puzzle3D.swap_yz_transform


class SolidPentominoes2x5x6(SolidPentominoes):

    """264 solutions"""

    height = 5
    width = 6
    depth = 2

    @classmethod
    def components(cls):
        return (SolidPentominoes2x5x6A, SolidPentominoes2x5x6B)

    transform_solution_matrix = Puzzle3D.swap_yz_transform


class SolidPentominoes2x5x6A(SolidPentominoes2x5x6):

    def build_matrix(self):
        keys = sorted(self.pieces.keys())
        for x_coords, x_aspect in self.pieces['X']:
            if not x_aspect.bounds[-1]: # get the one in the XY plane
                break
        for x in range(2):
            translated = x_aspect.translate((x, 0, 0))
            self.build_matrix_row('X', translated)
        keys.remove('X')
        self.build_regular_matrix(keys)


class SolidPentominoes2x5x6B(SolidPentominoes2x5x6):

    """symmetry: X in center; remove flip of F"""

    def customize_piece_data(self):
        self.piece_data['F'][-1]['flips'] = None

    def build_matrix(self):
        keys = sorted(self.pieces.keys())
        for x_coords, x_aspect in self.pieces['X']:
            if not x_aspect.bounds[-1]: # get the one in the XY plane
                break
        for x in range(2):
            translated = x_aspect.translate((x, 1, 0))
            self.build_matrix_row('X', translated)
        keys.remove('X')
        self.build_regular_matrix(keys)


class SolidPentominoes3x4x5(SolidPentominoes):

    """
    3940 solutions
    """

    height = 4
    width = 5
    depth = 3

    check_for_duplicates = True

    duplicate_conditions = ({'x_reversed': True},
                            {'z_reversed': True},
                            {'x_reversed': True, 'z_reversed': True})

    def build_matrix_i(self, y_range, z_range):
        keys = sorted(self.pieces.keys())
        for coords, aspect in self.pieces['I']:
            if aspect.bounds[0]: # get the one on the X axis
                break
        for z in z_range:
            for y in y_range:
                translated = aspect.translate((0, y, z))
                self.build_matrix_row('I', translated)
        keys.remove('I')
        return keys

    def build_matrix(self):
        keys = self.build_matrix_i((0, 1), (0, 1))
        self.build_regular_matrix(keys)

    transform_solution_matrix = Puzzle3D.swap_yz_transform


class SolidPentominoesRing(SolidPentominoes):

    check_for_duplicates = True

    duplicate_conditions = ({'x_reversed': True},
                            {'y_reversed': True},
                            {'z_reversed': True},
                            {'x_reversed': True, 'y_reversed': True},
                            {'x_reversed': True, 'z_reversed': True},
                            {'y_reversed': True, 'z_reversed': True},
                            {'x_reversed': True,
                             'y_reversed': True,
                             'z_reversed': True})

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if ( (x == 0) or (x == self.width - 1)
                         or (z == 0) or (z == self.depth - 1)):
                        yield (x, y, z)

    def build_matrix_header(self):
        headers = []
        for i, key in enumerate(sorted(self.pieces.keys())):
            self.matrix_columns[key] = i
            headers.append(key)
        for (x, y, z) in self.coordinates():
            header = '%0*i,%0*i,%0*i' % (
                self.x_width, x, self.y_width, y, self.z_width, z)
            self.matrix_columns[header] = len(headers)
            headers.append(header)
        self.matrix.append(tuple(headers))

    def build_regular_matrix(self, keys):
        for key in keys:
            for coords, aspect in self.pieces[key]:
                for z in range(self.depth - aspect.bounds[2]):
                    for y in range(self.height - aspect.bounds[1]):
                        for x in range(self.width - aspect.bounds[0]):
                            translated = aspect.translate((x, y, z))
                            if translated.issubset(self.solution_coords):
                                self.build_matrix_row(key, translated)

    def format_solution(self, solution, normalized=True,
                        x_reversed=False, y_reversed=False, z_reversed=False):
        order_functions = (lambda x: x, reversed)
        x_reversed_fn = order_functions[x_reversed]
        y_reversed_fn = order_functions[1 - y_reversed] # reversed by default
        z_reversed_fn = order_functions[z_reversed]
        z_unreversed_fn = order_functions[1 - z_reversed]
        s_matrix = self.build_solution_matrix(solution)
        lines = []
        left_index = [0, -1][x_reversed]
        right_index = -1 - left_index
        for y in y_reversed_fn(range(self.height)):
            back = ' '.join(x_reversed_fn(s_matrix[0][y]))
            front = ' '.join(x_reversed_fn(s_matrix[-1][y]))
            if z_reversed:
                back, front = front, back
            left = ' '.join(s_matrix[z][y][left_index]
                            for z in z_reversed_fn(range(self.depth)))
            right = ' '.join(
                s_matrix[z][y][right_index]
                for z in z_unreversed_fn(range(self.depth)))
            lines.append(('%s    %s    %s    %s'
                          % (left, front, right, back)).rstrip())
        return '\n'.join(lines)


class SolidPentominoes3x3x9Ring(SolidPentominoesRing):

    """3 solutions"""

    width = 9
    height = 3
    depth = 3

    def build_matrix(self):
        keys = sorted(self.pieces.keys())
        for coords, aspect in self.pieces['X']:
            if aspect.bounds[0] == 0:   # YZ plane
                self.build_matrix_row('X', aspect)
            if aspect.bounds[2] == 0:   # XY plane
                for x in range(4):
                    translated = aspect.translate((x, 0, 0))
                    self.build_matrix_row('X', translated)
        keys.remove('X')
        self.build_regular_matrix(keys)


class SolidPentominoes3x4x8Ring(SolidPentominoesRing):

    """0 solutions"""

    width = 8
    height = 3
    depth = 4


class SolidPentominoes3x5x7Ring(SolidPentominoesRing):

    """1 solution"""

    width = 7
    height = 3
    depth = 5

    def build_matrix(self):
        keys = sorted(self.pieces.keys())
        for coords, aspect in self.pieces['X']:
            if aspect.bounds[0] == 0:   # YZ plane
                for z in range(2):
                    translated = aspect.translate((0, 0, z))
                    self.build_matrix_row('X', translated)
            if aspect.bounds[2] == 0:   # XY plane
                for x in range(3):
                    translated = aspect.translate((x, 0, 0))
                    self.build_matrix_row('X', translated)
        keys.remove('X')
        self.build_regular_matrix(keys)


class SolidPentominoes3x6x6Ring(SolidPentominoesRing):

    """0 solutions"""

    width = 6
    height = 3
    depth = 6


class SolidPentominoes5x3x5Ring(SolidPentominoesRing):

    """186 solutions"""

    width = 5
    height = 5
    depth = 3

    def build_matrix(self):
        keys = sorted(self.pieces.keys())
        for coords, aspect in self.pieces['X']:
            if aspect.bounds[0] == 0:   # YZ plane
                for y in range(2):
                    translated = aspect.translate((0, y, 0))
                    self.build_matrix_row('X', translated)
            if aspect.bounds[2] == 0:   # XY plane
                for y in range(2):
                    for x in range(2):
                        translated = aspect.translate((x, y, 0))
                        self.build_matrix_row('X', translated)
        keys.remove('X')
        self.build_regular_matrix(keys)


class SolidPentominoes5x4x4Ring(SolidPentominoesRing):

    """0 solutions"""

    width = 4
    height = 5
    depth = 4


class SolidPentominoes6x3x4Ring(SolidPentominoesRing):

    """46 solutions"""

    width = 4
    height = 6
    depth = 3

    def build_matrix(self):
        keys = sorted(self.pieces.keys())
        for coords, aspect in self.pieces['X']:
            if aspect.bounds[0] == 0 or aspect.bounds[2] == 0: # YZ or XY plane
                for y in range(2):
                    translated = aspect.translate((0, y, 0))
                    self.build_matrix_row('X', translated)
        keys.remove('X')
        self.build_regular_matrix(keys)


class SolidPentominoes4x4x8Crystal(SolidPentominoes):

    """251 solutions"""

    width = 4
    height = 8
    depth = 4

    def customize_piece_data(self):
        self.piece_data['F'][-1]['flips'] = None

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    total = x + y + z
                    xz_total = x + z
                    if total < 8 and (y > 3 or xz_total < 4):
                        yield (x, y, z)


class SolidPentominoes5x5x4Steps(SolidPentominoes):

    """137 solutions"""

    width = 4
    height = 5
    depth = 5

    check_for_duplicates = True

    duplicate_conditions = ({'x_reversed': True},
                            {'yz_swapped': True},
                            {'x_reversed': True,
                             'yz_swapped': True},)

    def customize_piece_data(self):
        self.piece_data['F'][-1]['flips'] = None

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    total = x + y + z
                    if y + z < self.height:
                        yield (x, y, z)


class SolidPentominoes4x4x6Steps(SolidPentominoes5x5x4Steps):

    """279 solutions"""

    width = 6
    height = 4
    depth = 4


class SolidPentominoes3x3x10Steps(SolidPentominoes5x5x4Steps):

    """9 solutions"""

    width = 10
    height = 3
    depth = 3


class SolidPentominoes3x3x12Tower(SolidPentominoes):

    """0 solutions"""

    width = 3
    height = 12
    depth = 3

    def coordinates(self):
        for y in range(self.height):
            for x, z in ((0,1), (1,0), (1,1), (1,2), (2,1)):
                yield (x, y, z)


class SolidPentominoes3x5x7Slope(SolidPentominoes):

    """ solutions"""

    width = 5
    height = 7
    depth = 3

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if x + y + z < self.height:
                        yield (x, y, z)


class SolidPentominoes6x6x6Crystal1(SolidPentominoes):

    """2 solutions"""

    width = 6
    height = 6
    depth = 6

    extras = ((1,1,4), (1,4,1), (4,1,1), (2,2,2))

    def customize_piece_data(self):
        self.piece_data['P'][-1]['flips'] = None
        self.piece_data['P'][-1]['axes'] = None

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if x + y + z < 6:
                        yield (x, y, z)
        for coord in self.extras:
            yield coord


class SolidPentominoes6x6x6Crystal2(SolidPentominoes6x6x6Crystal1):

    """1 solution"""

    extras = ((1,2,3), (2,2,2), (3,2,1), (1,4,1))

    check_for_duplicates = True

    duplicate_conditions = ({'xz_swapped': True},)

    def customize_piece_data(self):
        return


class SolidPentominoes6x6x6Crystal3(SolidPentominoes6x6x6Crystal1):

    """9 solutions"""

    extras = ((1,2,3), (3,1,2), (2,3,1), (2,2,2))

    def customize_piece_data(self):
        self.piece_data['P'][-1]['axes'] = None


class SolidPentominoes6x6x6Crystal4(SolidPentominoes6x6x6Crystal1):

    """2 solutions"""

    extras = ((0,5,1), (1,4,1), (1,5,0), (1,5,1))

    check_for_duplicates = True

    duplicate_conditions = ({'xz_swapped': True},)

    def customize_piece_data(self):
        return


class SolidPentominoes6x6x6Crystal5(SolidPentominoes6x6x6Crystal4):

    """4 solutions"""

    extras = ((1,3,2), (2,2,2), (2,3,1), (2,3,2))


class SolidPentominoes6x6x6CrystalX1(SolidPentominoes6x6x6Crystal1):

    """0 solutions"""

    extras = ((1,1,4), (2,1,3), (3,1,2), (4,1,1))

    def customize_piece_data(self):
        return


class SolidPentominoes6x6x6CrystalX2(SolidPentominoes6x6x6Crystal1):

    """0 solutions"""

    extras = ((3,3,0), (3,0,3), (0,3,3), (2,2,2))

    def customize_piece_data(self):
        return


class SolidPentominoes6x6x6CrystalX3(SolidPentominoes6x6x6Crystal4):

    """0 solutions"""

    extras = ((2,1,3), (3,0,3), (3,1,2), (3,1,3))


class SolidPentominoes6x6x6CrystalX4(SolidPentominoes6x6x6Crystal4):

    """0 solutions"""

    extras = ((1,3,2), (2,2,2), (2,2,1), (1,4,1))


class SolidPentominoes7x7x7Crystal(SolidPentominoes):

    """0 solutions"""

    width = 7
    height = 7
    depth = 7

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if x + y + z < 6:
                        yield (x, y, z)
        for x, y, z in ((0,0,6), (0,6,0), (6,0,0), (2,2,2)):
            yield (x, y, z)


class SolidPentominoesTower1(SolidPentominoes):

    """
    27 solutions

    Design by David Klarner
    """

    width = 3
    height = 8
    depth = 3

    extras = ((0,7,1), (1,7,0), (1,7,2), (2,7,1))

    def coordinates(self):
        coords = (
            set(self.coordinates_cuboid(3, 7, 3))
            - set(self.coordinates_cuboid(1, 7, 1, offset=(1,0,1))))
        coords.update(set(self.coordinate_offset(x, y, z, None)
                          for x, y, z in self.extras))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['F'][-1]['flips'] = None
        self.piece_data['F'][-1]['axes'] = None

    def build_matrix(self):
        keys = sorted(self.pieces.keys())
        for coords, aspect in self.pieces['F']:
            for y in range(6):
                translated = aspect.translate((0, y, 0))
                if translated.issubset(self.solution_coords):
                    self.build_matrix_row('F', translated)
        keys.remove('F')
        self.build_regular_matrix(keys)


class SolidPentominoesTower2(SolidPentominoesTower1):

    """
    10 solutions

    Design by David Klarner
    """

    extras = ((0,7,0), (0,7,2), (2,7,0), (2,7,2))


class SolidPentominoesTower3(SolidPentominoesTower1):

    """
    many solutions

    Design by Leslie Young via Kadon's Quintillions booklet
    """

    extras = ((0,6,1), (1,6,0), (1,6,1), (1,6,2), (2,6,1), (1,7,1))

    def coordinates(self):
        coords = set(self.coordinates_cuboid(3, 6, 3))
        coords.update(set(self.coordinate_offset(x, y, z, None)
                          for x, y, z in self.extras))
        return sorted(coords)

    def customize_piece_data(self):
        pass

    def build_matrix(self):
        SolidPentominoes.build_matrix(self)


class SolidPentominoesOhnosBlock(SolidPentominoes):

    """
    1 solution

    Design by Yoshio Ohno, from Kadon's Quintillions booklet
    (title: 'A Gift From Japan')
    """

    width = 6
    height = 6
    depth = 3

    extras = ((0,2), (2,5), (3,0), (5,3))

    def coordinates(self):
        coords = set(self.coordinates_cuboid(4, 4, 3, offset=(1,1,0)))
        coords.update(set(self.coordinate_offset(x, y, z, None)
                          for x, y in self.extras for z in range(3)))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['L'][-1]['rotations'] = None
        self.piece_data['L'][-1]['flips'] = None


class SolidPentominoesSpinnerBlock(SolidPentominoesOhnosBlock):

    """42 solutions"""

    extras = ((0,1), (1,5), (4,0), (5,4))

    def customize_piece_data(self):
        pass

    check_for_duplicates = True
    duplicate_conditions = ({'z_reversed': True},)

    def build_aspects(self):
        names = sorted(self.piece_data.keys())
        data, kwargs = self.piece_data['L']
        self.aspects['L'] = self.make_aspects(
            data, flips=None, axes=None, rotations=None)
        self.aspects['L'].update(self.make_aspects(
            data, flips=None, axes=(1,), rotations=None))
        names.remove('L')
        self.build_regular_aspects(names)


class SolidPentominoesCornerWalls(SolidPentominoes):

    """253 solutions"""

    width = 5
    height = 5
    depth = 5

    def coordinates(self):
        coords = (
            set(self.coordinates_cuboid(5, 5, 5))
            - set(self.coordinates_cuboid(4, 4, 4, offset=(1,1,1)))
            - set(((0,0,0),)))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['F'][-1]['axes'] = None
        self.piece_data['F'][-1]['flips'] = None


class SolidPentominoesCornerPiece(SolidPentominoes):

    """
    70 solutions

    Design from Kadon's Quintillions booklet
    """

    width = 5
    height = 6
    depth = 5

    def coordinates(self):
        coords = set(
            list(self.coordinates_cuboid(5, 6, 1))
            + list(self.coordinates_cuboid(1, 6, 5))
            + list(self.coordinates_cuboid(1, 6, 1, offset=(1,0,1))))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['F'][-1]['rotations'] = (0, 1)
        self.piece_data['F'][-1]['flips'] = None


class SolidPentominoesThreeWalls(SolidPentominoes):

    """
    90 solutions

    Design from Kadon's Quintillions booklet
    """

    width = 7
    height = 6
    depth = 4

    check_for_duplicates = True
    duplicate_conditions = ({'y_reversed': True},)

    def coordinates(self):
        coords = set(
            list(self.coordinates_cuboid(7, 6, 1))
            + list(self.coordinates_cuboid(1, 6, 3, offset=(3,0,1))))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['F'][-1]['rotations'] = (0, 1)
        self.piece_data['F'][-1]['flips'] = None


class SolidPentominoesEmptyBottle(SolidPentominoes):

    """
    49 solutions

    Design from Kadon's Quintillions booklet
    """

    width = 3
    height = 9
    depth = 3

    def coordinates(self):
        coords = (
            set(list(self.coordinates_cuboid(3, 7, 3))
                + list(self.coordinates_cuboid(1, 2, 1, offset=(1,7,1))))
            - set(self.coordinates_cuboid(1, 5, 1, offset=(1,1,1))))
        return sorted(coords)

    def build_aspects(self):
        names = sorted(self.piece_data.keys())
        data, kwargs = self.piece_data['F']
        self.aspects['F'] = self.make_aspects(
            data, flips=None, axes=None)
        self.aspects['F'].update(self.make_aspects(
            data, flips=None, axes=(1,), rotations=None))
        names.remove('F')
        self.build_regular_aspects(names)

    def build_matrix(self):
        keys = sorted(self.pieces.keys())
        for coords, aspect in self.pieces['F']:
            if aspect.bounds[-1]:       # the one in the XZ plane
                translated = aspect.translate((0, 0, 0))
                self.build_matrix_row('F', translated)
            else:                       # the ones in the XY plane
                for y in range(5):
                    translated = aspect.translate((0, y, 0))
                    self.build_matrix_row('F', translated)
        keys.remove('F')
        self.build_regular_matrix(keys)


class SolidPentominoesCondominiumB(SolidPentominoes):

    """
    1 solution

    Design from Kadon's Quintillions booklet
    """

    width = 3
    height = 9
    depth = 4

    transform_solution_matrix = Puzzle3D.cycle_xyz_transform

    def coordinates(self):
        coords = set(
            list(self.coordinates_cuboid(1, 5, 4, offset=(0,4,0)))
            + list(self.coordinates_cuboid(1, 5, 4, offset=(1,2,0)))
            + list(self.coordinates_cuboid(1, 5, 4, offset=(2,0,0))))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['F'][-1]['rotations'] = (0, 1)
        self.piece_data['F'][-1]['flips'] = None


class SolidPentominoesCrossBlock1(SolidPentominoes):

    """92 solutions"""

    width = 4
    height = 4
    depth = 5

    transform_solution_matrix = Puzzle3D.swap_yz_transform

    @classmethod
    def components(cls):
        return (SolidPentominoesCrossBlock1A, SolidPentominoesCrossBlock1B)

    def coordinates(self):
        coords = set(
            self.coordinate_offset(x, y, z, None)
            for x, y in Puzzle2D.coordinates_aztec_diamond(2)
            for z in range(5))
        return sorted(coords)


class SolidPentominoesCrossBlock1A(SolidPentominoesCrossBlock1):

    """Limit the F pentomino to asymmetrical positions."""

    def build_aspects(self):
        names = sorted(self.piece_data.keys())
        data, kwargs = self.piece_data['F']
        self.aspects['F'] = self.make_aspects(
            data, flips=None, rotations=None, axes=None)
        self.aspects['F'].update(self.make_aspects(
            data, flips=None, axes=(1,), rotations=(0, 1)))
        names.remove('F')
        self.build_regular_aspects(names)

    def build_matrix(self):
        keys = sorted(self.pieces.keys())
        for coords, aspect in self.pieces['F']:
            if aspect.bounds[-1]:       # the ones in the XZ plane
                for x in range(2):
                    for z in range(3):
                        translated = aspect.translate((x, 1, z))
                        self.build_matrix_row('F', translated)
            else:                       # the one in the XY plane
                for x, y in ((0,1), (1,0), (1,1)):
                    for z in range(2):
                        translated = aspect.translate((x, y, z))
                        self.build_matrix_row('F', translated)
        keys.remove('F')
        self.build_regular_matrix(keys)


class SolidPentominoesCrossBlock1B(SolidPentominoesCrossBlock1):

    """
    Limit the F pentomino to symmetrical positions, and limit the X pentomino
    to one half of the puzzle.
    """

    def build_aspects(self):
        names = sorted(self.piece_data.keys())
        data, kwargs = self.piece_data['F']
        self.aspects['F'] = self.make_aspects(
            data, flips=None, rotations=None, axes=None)
        names.remove('F')
        self.build_regular_aspects(names)

    def build_matrix(self):
        keys = sorted(self.pieces.keys())
        assert len(self.pieces['F']) == 1
        coords, aspect = self.pieces['F'][0]
        for x, y in ((0,1), (1,0), (1,1)):
            translated = aspect.translate((x, y, 2))
            self.build_matrix_row('F', translated)
        keys.remove('F')
        for coords, aspect in self.pieces['X']:
            if aspect.bounds[-1]:       # the ones in the XZ & YZ planes
                for x in range(3):
                    for y in range(3):
                        translated = aspect.translate((x, y, 0))
                        if translated.issubset(self.solution_coords):
                            self.build_matrix_row('X', translated)
            else:                       # the one in the XY plane
                for x in range(2):
                    for y in range(2):
                        for z in range(3):
                            translated = aspect.translate((x, y, z))
                            if translated.issubset(self.solution_coords):
                                self.build_matrix_row('X', translated)
        keys.remove('X')
        self.build_regular_matrix(keys)


class SolidPentominoesCrossBlock2(SolidPentominoes):

    """0 solutions"""

    width = 5
    height = 5
    depth = 3

    transform_solution_matrix = Puzzle3D.swap_yz_transform

    @classmethod
    def components(cls):
        return (
            SolidPentominoesCrossBlock2A, SolidPentominoesCrossBlock2B,
            SolidPentominoesCrossBlock2C)

    def coordinates(self):
        coords = (
            set(list(self.coordinates_cuboid(5, 3, 3, offset=(0,1,0)))
                + list(self.coordinates_cuboid(3, 5, 3, offset=(1,0,0))))
            - set(self.coordinates_cuboid(1, 1, 3, offset=(2,2,0))))
        return sorted(coords)

class SolidPentominoesCrossBlock2A(SolidPentominoesCrossBlock2):

    """Limit the F pentomino to asymmetrical positions."""

    def build_aspects(self):
        names = sorted(self.piece_data.keys())
        data, kwargs = self.piece_data['F']
        self.aspects['F'] = self.make_aspects(
            data, flips=None, rotations=None, axes=None)
        self.aspects['F'].update(self.make_aspects(
            data, flips=None, axes=(1,), rotations=(0, 1)))
        names.remove('F')
        self.build_regular_aspects(names)

    def build_matrix(self):
        keys = sorted(self.pieces.keys())
        for coords, aspect in self.pieces['F']:
            if aspect.bounds[-1]:       # the ones in the XZ plane
                for x in range(3):
                    for y in range(2):
                        translated = aspect.translate((x, y, 0))
                        if translated.issubset(self.solution_coords):
                            self.build_matrix_row('F', translated)
            else:                       # the one in the XY plane
                for x, y in ((0,2), (2,0), (2,1)):
                    translated = aspect.translate((x, y, 0))
                    self.build_matrix_row('F', translated)
        keys.remove('F')
        self.build_regular_matrix(keys)


class SolidPentominoesCrossBlock2B(SolidPentominoesCrossBlock2):

    """
    Limit the F pentomino to symmetrical positions, and limit the I pentomino
    to one half of the puzzle.
    """

    def build_aspects(self):
        names = sorted(self.piece_data.keys())
        data, kwargs = self.piece_data['F']
        self.aspects['F'] = self.make_aspects(
            data, flips=None, rotations=None, axes=None)
        names.remove('F')
        self.build_regular_aspects(names)

    def build_matrix(self):
        keys = sorted(self.pieces.keys())
        assert len(self.pieces['F']) == 1
        coords, aspect = self.pieces['F'][0]
        for x, y in ((0,2), (2,0), (2,1)):
            translated = aspect.translate((x, y, 1))
            self.build_matrix_row('F', translated)
        keys.remove('F')
        for coords, aspect in self.pieces['I']:
            if not aspect.bounds[-1]:   # the ones in the XY plane
                for x in range(5):
                    for y in range(5):
                        translated = aspect.translate((x, y, 0))
                        if translated.issubset(self.solution_coords):
                            self.build_matrix_row('I', translated)
        keys.remove('I')
        self.build_regular_matrix(keys)


class SolidPentominoesCrossBlock2C(SolidPentominoesCrossBlock2):

    """
    Limit the F pentomino to symmetrical positions, and limit the I pentomino
    to the central layer of the puzzle.
    """

    def build_aspects(self):
        names = sorted(self.piece_data.keys())
        data, kwargs = self.piece_data['F']
        self.aspects['F'] = self.make_aspects(
            data, flips=None, rotations=None, axes=None)
        names.remove('F')
        self.build_regular_aspects(names)

    def build_matrix(self):
        keys = sorted(self.pieces.keys())
        assert len(self.pieces['F']) == 1
        coords, aspect = self.pieces['F'][0]
        for x, y in ((0,2), (2,0), (2,1)):
            translated = aspect.translate((x, y, 1))
            self.build_matrix_row('F', translated)
        keys.remove('F')
        for coords, aspect in self.pieces['I']:
            if not aspect.bounds[-1]:   # the ones in the XY plane
                for x in range(5):
                    for y in range(5):
                        translated = aspect.translate((x, y, 1))
                        if translated.issubset(self.solution_coords):
                            self.build_matrix_row('I', translated)
        keys.remove('I')
        self.build_regular_matrix(keys)


class SolidPentominoesCrossBlock3(SolidPentominoes):

    """10 solutions"""

    width = 6
    height = 6
    depth = 2

    #transform_solution_matrix = Puzzle3D.swap_yz_transform

    def coordinates(self):
        coords = (
            set(list(self.coordinates_cuboid(6, 4, 2, offset=(0,1,0)))
                + list(self.coordinates_cuboid(4, 6, 2, offset=(1,0,0))))
            - set(self.coordinates_cuboid(2, 2, 1, offset=(2,2,1))))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['F'][-1]['rotations'] = None
        self.piece_data['F'][-1]['flips'] = None


class SolidPentominoesCrossBlock_x1(SolidPentominoes):

    """0 solutions"""

    width = 6
    height = 6
    depth = 3

    def coordinates(self):
        coords = set(
            list(self.coordinates_cuboid(6, 2, 3, offset=(0,2,0)))
            + list(self.coordinates_cuboid(2, 6, 3, offset=(2,0,0))))
        return sorted(coords)


class SolidPentominoesOpenBox8x3x3(SolidPentominoes):

    """many solutions"""

    width = 8
    height = 3
    depth = 3

    transform_solution_matrix = Puzzle3D.swap_yz_transform

    def coordinates(self):
        return self.coordinates_open_box(self.width, self.height, self.depth)


class SolidPentominoesOpenBox6x3x4(SolidPentominoesOpenBox8x3x3):

    """many solutions"""

    width = 6
    height = 3
    depth = 4


class SolidPentominoes5x5x5QuarterPyramid(SolidPentominoes):

    """
    55-cube shape, so 11 pieces are used and one piece must be omitted.

    320 solutions:

    * 11 omitting F
    * 7 omitting I
    * none omitting L
    * 4 omitting N
    * none omitting P
    * 22 omitting T
    * 4 omitting U
    * 12 omitting V
    * 10 omitting W
    * 223 omitting X
    * 2 omitting Y
    * 25 omitting Z
    """

    width = 9
    height = 5
    depth = 5

    # These 9 coordinates form a minimal cover for all 12 pentominoes
    # (with Z=0 for solid pentominoes):
    omitted_piece_coordinates = (
        (0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (1,3), (1,4), (2,2))

    # Since there are only 9 coordinates for the omitted piece, only 1 piece
    # can fit.  By setting these 9 coordinates as secondary columns, the extra
    # 4 coordinates are ignored.
    secondary_columns = 9

    # These are the fixed positions for omitted pieces, to prevent duplicates.
    omitted_piece_positions = {
        'F': ((0,1), (1,0), (1,1), (1,2), (2,2)),
        'I': ((1,0), (1,1), (1,2), (1,3), (1,4)),
        'L': ((0,0), (1,0), (1,1), (1,2), (1,3)),
        'N': ((0,0), (0,1), (0,2), (1,2), (1,3)),
        'P': ((0,0), (0,1), (0,2), (1,0), (1,1)),
        'T': ((0,2), (1,0), (1,1), (1,2), (2,2)),
        'U': ((0,0), (0,1), (0,2), (1,0), (1,2)),
        'V': ((0,0), (0,1), (0,2), (1,2), (2,2)),
        'W': ((0,0), (0,1), (1,1), (1,2), (2,2)),
        'X': ((0,2), (1,1), (1,2), (1,3), (2,2)),
        'Y': ((0,2), (1,0), (1,1), (1,2), (1,3)),
        'Z': ((0,0), (1,0), (1,1), (1,2), (2,2)),}

    omitted_cover_offset = (6,0,0)

    transform_solution_matrix = Puzzle3D.cycle_xyz_transform

    def coordinates(self):
        coords = set()
        for i in range(5):
            coords.update(
                set(self.coordinates_cuboid(5 - i, 5 - i, 1, offset=(0,0,i))))
        self.regular_solution_coords = coords.copy()
        dx, dy, dz = self.omitted_cover_offset
        for (x, y) in self.omitted_piece_coordinates:
            coords.add((x + dx, y + dy, dz))
        return sorted(coords)

    def build_matrix(self):
        self.build_rows_for_omitted_pieces()
        self.build_regular_matrix(
            sorted(self.piece_data.keys()),
            solution_coords=self.regular_solution_coords)

    def build_rows_for_omitted_pieces(self):
        #import pdb ; pdb.set_trace()
        dx, dy, dz = self.omitted_cover_offset
        for key, coords in self.omitted_piece_positions.items():
            coords3d = [(x + dx, y + dy, dz) for (x, y) in coords]
            self.build_matrix_row(key, coords3d)

    def build_aspects(self):
        """
        To eliminate duplicates from symmetry, limit the P pentomino to:

        * the XY plane, where flips are disallowed; and
        * the XZ plane (full freedom).
        """
        all_pieces_but_P = sorted(self.piece_data.keys())
        all_pieces_but_P.remove('P')
        self.build_regular_aspects(all_pieces_but_P)
        data, kwargs = self.piece_data['P']
        self.aspects['P'] = self.make_aspects(data, flips=None, axes=(2,))
        self.aspects['P'].update(self.make_aspects(data, axes=(1,)))
        self.pieces['P'] = tuple(
            sorted((tuple(sorted(aspect)), aspect)
                   for aspect in self.aspects['P']))


class SolidPentominoesCrossTower(SolidPentominoes):

    """
    7 solutions

    Design from `Thimo Rosenkranz's pentoma.de <http://www.pentoma.de>`_.
    """

    width = 5
    height = 5
    depth = 8

    transform_solution_matrix = Puzzle3D.cycle_xyz_transform

    check_for_duplicates = True

    duplicate_conditions = ({'x_reversed': True},)

    def coordinates(self):
        coords = set(
            list(self.coordinates_cuboid(5, 1, 6, offset=(0,2,0)))
            + list(self.coordinates_cuboid(1, 5, 6, offset=(2,0,0)))
            + [Cartesian3D(coord)
               for coord in ((1,2,6), (2,1,6), (2,2,6), (2,3,6), (3,2,6),
                             (2,2,7))])
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P'][-1]['flips'] = None
        self.piece_data['P'][-1]['axes'] = (0,)


class SolidPentominoesInfinityTower(SolidPentominoes):

    """
    1 solution

    Design from `Thimo Rosenkranz's pentoma.de <http://www.pentoma.de>`_.
    """

    width = 5
    height = 5
    depth = 4

    transform_solution_matrix = Puzzle3D.cycle_xyz_transform

    def coordinates(self):
        coords = set(
            list(self.coordinates_ring_wall(3, 3, 4, offset=(0,2,0)))
            + list(self.coordinates_ring_wall(3, 3, 4, offset=(2,0,0))))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P'][-1]['flips'] = None
        self.piece_data['P'][-1]['axes'] = (0,)
        self.piece_data['P'][-1]['rotations'] = (0, 1)


class SolidPentominoesSquareTower1(SolidPentominoes):

    """
    1 solution

    Design from `Thimo Rosenkranz's pentoma.de <http://www.pentoma.de>`_.
    """

    width = 5
    height = 5
    depth = 5

    transform_solution_matrix = Puzzle3D.cycle_xyz_transform

    check_for_duplicates = True

    duplicate_conditions = ({'x_reversed': True},)

    _offsets = ((0,2), (2,0), (2,4), (4,2))

    def coordinates(self):
        coords = set(self.coordinates_ring_wall(3, 3, 5, offset=(1,1,0)))
        for (x, y) in self._offsets:
            coords.update(set(self.coordinates_cuboid(1, 1, 5, offset=(x,y,0))))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P'][-1]['flips'] = None
        self.piece_data['P'][-1]['axes'] = (0,)
        self.piece_data['P'][-1]['rotations'] = (0, 1)


class SolidPentominoesSquareTower2(SolidPentominoesSquareTower1):

    """
    54 solutions

    Design from `Thimo Rosenkranz's pentoma.de <http://www.pentoma.de>`_.
    """

    _offsets = ((0,3), (1,4), (3,0), (4,1))

    check_for_duplicates = False


class SolidPentominoesSquareTower3(SolidPentominoesSquareTower1):

    """27 solutions"""

    _offsets = ((0,3), (1,0), (3,4), (4,1))

    check_for_duplicates = False


class SolidPentominoesSquareTower4(SolidPentominoesSquareTower1):

    """8 solutions"""

    _offsets = ((0,3), (0,4), (4,0), (4,1))

    check_for_duplicates = False

    def customize_piece_data(self):
        self.piece_data['P'][-1]['flips'] = None
        self.piece_data['P'][-1]['rotations'] = (0, 1)


class SolidPentominoesStairstepWalls1(SolidPentominoes):

    """34 solutions"""

    width = 8
    height = 8
    depth = 6

    transform_solution_matrix = Puzzle3D.cycle_xyz_transform

    holes = set()

    def coordinates(self):
        coords = set()
        for i in range(self.depth):
            coords.update(
                set(self.coordinates_cuboid(1, 8-i, 1, offset=(0,0,i))))
            coords.update(
                set(self.coordinates_cuboid(8-i, 1, 1, offset=(0,0,i))))
        coords -= self.holes
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P'][-1]['axes'] = (0,)


class SolidPentominoesStairstepWalls2(SolidPentominoesStairstepWalls1):

    """1 solution"""

    depth = 8

    holes = set(
        list(SolidPentominoes.coordinates_cuboid(1, 2, 1, offset=(0,1,0)))
        + list(SolidPentominoes.coordinates_cuboid(2, 1, 1, offset=(1,0,0))))


class SolidPentominoesStairstepWalls_x3(SolidPentominoesStairstepWalls1):

    """0 solutions"""

    depth = 7

    holes = set(
        list(SolidPentominoes.coordinates_cuboid(1, 2, 1, offset=(0,2,0)))
        + list(SolidPentominoes.coordinates_cuboid(2, 1, 1, offset=(2,0,0))))

    holes = set(
        list(SolidPentominoes.coordinates_cuboid(1, 2, 1, offset=(0,3,0)))
        + list(SolidPentominoes.coordinates_cuboid(2, 1, 1, offset=(3,0,0))))

    holes = set(
        list(SolidPentominoes.coordinates_cuboid(1, 2, 1, offset=(0,4,0)))
        + list(SolidPentominoes.coordinates_cuboid(2, 1, 1, offset=(4,0,0))))

    holes = set(SolidPentominoes.coordinates_cuboid(2, 2, 1))
