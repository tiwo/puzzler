#!/usr/bin/env python
# -*- coding: utf-8 -*-
# $Id$

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2006 by David J. Goodger
# License: GPL 2 (see __init__.py)

import pdb
import sys
import copy
import datetime
from pprint import pprint, pformat
import coordsys


class Puzzle(object):

    """
    Abstract base class for puzzles.
    """

    height = 0
    width = 0
    depth = 0

    check_for_duplicates = False

    duplicate_conditions = ()
    """A list of dictionaries of default-value keyword arguments to
    `format_solution`, to generate all solution permutations."""

    secondary_columns = 0

    piece_data = {}
    """Mapping of piece names to 2-tuples:

    * list of unit coordinates (usually one unit, the origin, is implicit)
    * dictionary of aspect restrictions, keyword arguments to `make_aspects`;
      customized in `customize_piece_data` (make a copy.deepcopy first though)
    """

    def __init__(self):
        self.solutions = set()
        """Set of all permutations of solutions, for duplicate checking."""

        self.solution_coords = set(self.coordinates())
        """A set of all coordinates that make up the solution area/space."""

        self.aspects = {}
        """Mapping of piece name to a set of aspects (pieces in all
        orientations)."""

        self.customize_piece_data()
        for name, (data, kwargs) in self.piece_data.items():
            self.aspects[name] = self.make_aspects(data, **kwargs)

        self.pieces = {}
        """Mapping of piece name to a sorted list of 2-tuples: sorted
        coordinates & aspect objects.  Ensures reproducible results."""

        for name, aspects in self.aspects.items():
            self.pieces[name] = tuple(sorted((tuple(sorted(aspect)), aspect)
                                             for aspect in aspects))

        self.x_width = len(str(self.width - 1))
        """Maximum width of string representation of X coordinate."""

        self.y_width = len(str(self.height - 1))
        """Maximum width of string representation of Y coordinate."""

        self.z_width = len(str(self.depth - 1))
        """Maximum width of string representation of Z coordinate."""

        self.matrix = []
        """A list of lists; see puzzler.exact_cover.convert_matrix()."""

        self.matrix_columns = {}
        """Mapping of `self.matrix` column names to indices."""

        self.build_matrix_header()
        self.build_matrix()

    def coordinates(self):
        """
        A generator that yields all the coordinates of the solution space.

        Implement in subclasses.
        """
        raise NotImplementedError

    def customize_piece_data(self):
        """
        Make instance-specific customizations to a copy of `self.piece_data`.

        Override in subclasses.
        """
        pass

    def make_aspects(self, data, **kwargs):
        """
        Return a set of aspects (rotations & flips) of a puzzle piece
        described by `data`.  Puzzle-specific parameters control the range of
        aspect orientations.

        Implement in subclasses.
        """
        raise NotImplementedError

    def build_matrix_header(self):
        """
        Create and populate the first row of `self.matrix`, a list of column
        names.

        Implement in subclasses.
        """
        raise NotImplementedError

    def build_matrix(self):
        """
        Create and populate the data rows of `self.matrix`, lists of 0's and
        1's (or other true values).
        """
        self.build_regular_matrix(sorted(self.pieces.keys()))

    def record_solution(self, solution, solver, stream=sys.stdout, dated=False):
        """
        Output a formatted solution to `stream`.
        """
        formatted = self.format_solution(solution)
        if self.check_for_duplicates:
            if formatted in self.solutions:
                return
            self.store_solutions(solution, formatted)
        if dated:
            print >>stream, 'at %s,' % datetime.datetime.now(),
        print >>stream, solver.format_solution()
        print >>stream
        print >>stream, formatted
        print >>stream

    def record_dated_solution(self, solution, solver, stream=sys.stdout):
        """A dated variant of `self.record_solution`."""
        self.record_solution(solution, solver, stream=stream, dated=True)

    def format_solution(self, solution):
        """
        Return a puzzle-specific formatting of a solution.

        Implement in subclasses.
        """
        raise NotImplementedError

    def store_solutions(self, solution, formatted):
        """
        Store the formatted solution along with puzzle-specific variants
        (reflections, rotations) in `self.solutions`, to check for duplicates.
        """
        self.solutions.add(formatted)
        for conditions in self.duplicate_conditions:
            self.solutions.add(self.format_solution(solution, **conditions))


class Puzzle2D(Puzzle):

    duplicate_conditions = ({'x_reversed': True},
                            {'y_reversed': True},
                            {'x_reversed': True, 'y_reversed': True})

    def coordinates(self):
        for y in range(self.height):
            for x in range(self.width):
                yield coordsys.Cartesian2D((x, y))

    def make_aspects(self, units, flips=(False, True), rotations=(0, 1, 2, 3)):
        aspects = set()
        coord_list = ((0, 0),) + units
        for flip in flips or (0,):
            for rotation in rotations or (0,):
                aspect = coordsys.CartesianView2D(coord_list, rotation, flip)
                aspects.add(aspect)
        return aspects

    def build_matrix_header(self):
        headers = []
        for i, key in enumerate(sorted(self.pieces.keys())):
            self.matrix_columns[key] = i
            headers.append(key)
        for (x, y) in self.coordinates():
            header = '%0*i,%0*i' % (self.x_width, x, self.y_width, y)
            self.matrix_columns[header] = len(headers)
            headers.append(header)
        self.matrix.append(headers)

    def build_regular_matrix(self, keys):
        for key in keys:
            for coords, aspect in self.pieces[key]:
                for y in range(self.height - aspect.bounds[1]):
                    for x in range(self.width - aspect.bounds[0]):
                        translated = aspect.translate((x, y))
                        if translated.issubset(self.solution_coords):
                            self.build_matrix_row(key, translated)

    def build_matrix_row(self, name, coords):
        row = [0] * len(self.matrix[0])
        row[self.matrix_columns[name]] = name
        for coord in coords:
            label = '%0*i,%0*i' % (self.x_width, coord[0],
                                   self.y_width, coord[1])
            row[self.matrix_columns[label]] = label
        self.matrix.append(row)

    def format_solution(self, solution,
                        x_reversed=False, y_reversed=False):
        order_functions = (lambda x: x, reversed)
        x_reversed_fn = order_functions[x_reversed]
        y_reversed_fn = order_functions[1 - y_reversed] # reversed by default
        s_matrix = [[' '] * self.width for y in range(self.height)]
        for row in solution:
            piece = sorted(i.column.name for i in row.row_data())
            name = piece[-1]
            for cell_name in piece[:-1]:
                x, y = [int(d.strip()) for d in cell_name.split(',')]
                s_matrix[y][x] = name
        return '\n'.join(' '.join(x_reversed_fn(s_matrix[y])).rstrip()
                         for y in y_reversed_fn(range(self.height)))


class Puzzle3D(Puzzle):

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    yield coordsys.Cartesian3D((x, y, z))

    def make_aspects(self, units,
                     flips=(0, 1), axes=(0, 1, 2), rotations=(0, 1, 2, 3)):
        aspects = set()
        coord_list = ((0, 0, 0),) + units
        for axis in axes or (2,):
            coord_set = coordsys.CartesianView3D(coord_list)
            if axis != 2:
                coord_set = coord_set.rotate0(1, (1 - axis) % 3)
            coords = tuple(coord_set)
            for flip in flips or (0,):
                for rotation in rotations or (0,):
                    aspect = coordsys.CartesianView3D(
                        coords, rotation, axis, flip)
                    aspects.add(aspect)
        return aspects

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
        self.matrix.append(headers)

    def build_regular_matrix(self, keys):
        for key in keys:
            for coords, aspect in self.pieces[key]:
                for z in range(self.depth - aspect.bounds[2]):
                    for y in range(self.height - aspect.bounds[1]):
                        for x in range(self.width - aspect.bounds[0]):
                            translated = aspect.translate((x, y, z))
                            if translated.issubset(self.solution_coords):
                                self.build_matrix_row(key, translated)

    def build_matrix_row(self, name, coords):
        row = [0] * len(self.matrix[0])
        row[self.matrix_columns[name]] = name
        for coord in coords:
            label = '%0*i,%0*i,%0*i' % (self.x_width, coord[0],
                                        self.y_width, coord[1],
                                        self.z_width, coord[2])
            row[self.matrix_columns[label]] = label
        self.matrix.append(row)

    def format_solution(self, solution,
                        x_reversed=False, y_reversed=False, z_reversed=False):
        order_functions = (lambda x: x, reversed)
        x_reversed_fn = order_functions[x_reversed]
        y_reversed_fn = order_functions[1 - y_reversed] # reversed by default
        z_reversed_fn = order_functions[z_reversed]
        s_matrix = [[[' '] * self.width for y in range(self.height)]
                    for z in range(self.depth)]
        for row in solution:
            piece = sorted(i.column.name for i in row.row_data())
            name = piece[-1]
            for cell_name in piece[:-1]:
                x, y, z = [int(d.strip()) for d in cell_name.split(',')]
                s_matrix[z][y][x] = name
        return '\n'.join(
            '    '.join(' '.join(x_reversed_fn(s_matrix[z][y]))
                        for z in z_reversed_fn(range(self.depth))).rstrip()
            for y in y_reversed_fn(range(self.height)))


class Pentominoes(Puzzle2D):

    piece_data = {
        'F': (((-1,-1), ( 0,-1), ( 1,0), ( 0,1)), {}),
        'I': (((-2, 0), (-1, 0), ( 1,0), ( 2,0)), {}),
        'L': (((-2, 0), (-1, 0), ( 1,0), ( 1,1)), {}),
        'N': (((-2, 0), (-1, 0), ( 0,1), ( 1,1)), {}),
        'P': (((-1, 0), ( 1, 0), ( 0,1), ( 1,1)), {}),
        'T': (((-1,-1), (-1, 0), (-1,1), ( 1,0)), {}),
        'U': (((-1,-1), ( 0,-1), ( 0,1), (-1,1)), {}),
        'V': (((-2, 0), (-1, 0), ( 0,1), ( 0,2)), {}),
        'W': ((( 1,-1), ( 1, 0), ( 0,1), (-1,1)), {}),
        'X': (((-1, 0), ( 0,-1), ( 1,0), ( 0,1)), {}),
        'Y': (((-2, 0), (-1, 0), ( 1,0), ( 0,1)), {}),
        'Z': (((-1,-1), (-1, 0), ( 1,0), ( 1,1)), {}),}
    """(0,0) is implied."""

    symmetric_pieces = 'I T U V W X'.split()
    """Pieces with reflexive symmetry, identical to their mirror images."""

    asymmetric_pieces = 'F L P N Y Z'.split()
    """Pieces without reflexive symmetry, different from their mirror images."""


class Pentominoes6x10Matrix(Pentominoes):

    """2339 solutions"""

    height = 6
    width = 10

    def build_matrix(self):
        keys = sorted(self.pieces.keys())
        x_coords, x_aspect = self.pieces['X'][0]
        for y in range(2):
            for x in range(y==0, 4):
                translated = x_aspect.translate((x, y))
                self.build_matrix_row('X', translated)
        keys.remove('X')
        self.build_regular_matrix(keys)


class Pentominoes5x12Matrix(Pentominoes):

    """1010 solutions"""

    height = 5
    width = 12


class Pentominoes5x12MatrixA(Pentominoes5x12Matrix):

    def build_matrix(self):
        keys = sorted(self.pieces.keys())
        x_coords, x_aspect = self.pieces['X'][0]
        for x in range(1, 5):
            translated = x_aspect.translate((x, 0))
            self.build_matrix_row('X', translated)
        keys.remove('X')
        self.build_regular_matrix(keys)


class Pentominoes5x12MatrixB(Pentominoes5x12Matrix):

    """symmetry: X at center; remove flip of P"""

    def customize_piece_data(self):
        self.piece_data = copy.deepcopy(self.piece_data)
        self.piece_data['P'][-1]['flips'] = None

    def build_matrix(self):
        keys = sorted(self.pieces.keys())
        x_coords, x_aspect = self.pieces['X'][0]
        for x in range(5):
            translated = x_aspect.translate((x, 1))
            self.build_matrix_row('X', translated)
        keys.remove('X')
        self.build_regular_matrix(keys)


class Pentominoes4x15Matrix(Pentominoes):

    """368 solutions"""

    height = 4
    width = 15


class Pentominoes4x15MatrixA(Pentominoes4x15Matrix):

    def build_matrix(self):
        keys = sorted(self.pieces.keys())
        x_coords, x_aspect = self.pieces['X'][0]
        for x in range(1, 6):
            translated = x_aspect.translate((x, 0))
            self.build_matrix_row('X', translated)
        keys.remove('X')
        self.build_regular_matrix(keys)


class Pentominoes4x15MatrixB(Pentominoes4x15Matrix):

    """symmetry: X at center; remove flip of P"""

    def customize_piece_data(self):
        self.piece_data = copy.deepcopy(self.piece_data)
        self.piece_data['P'][-1]['flips'] = None

    def build_matrix(self):
        keys = sorted(self.pieces.keys())
        x_coords, x_aspect = self.pieces['X'][0]
        translated = x_aspect.translate((6, 0))
        self.build_matrix_row('X', translated)
        keys.remove('X')
        self.build_regular_matrix(keys)


class Pentominoes3x20Matrix(Pentominoes):

    """
    2 solutions.
    Symmetry: restrict I to y=0.
    """

    height = 3
    width = 20

    def build_matrix(self):
        keys = sorted(self.pieces.keys())
        x_coords, x_aspect = self.pieces['X'][0]
        for x in (1, 6):
            translated = x_aspect.translate((x, 0))
            self.build_matrix_row('X', translated)
        keys.remove('X')
        for key in keys:
            for coords, aspect in self.pieces[key]:
                for y in range(self.height - aspect.bounds[1]
                               - 2 * (key == 'I')):
                    for x in range(self.width - aspect.bounds[0]):
                        translated = aspect.translate((x, y))
                        self.build_matrix_row(key, translated)


class Pentominoes3x20LoopMatrix(Pentominoes):

    """
    2 solutions: same as non-loop `Pentominoes3x20Matrix`.
    Symmetry: fix X; restrict U to 2 quadrants; restrict I to y=0 & 1.
    """

    height = 3
    width = 20

    def customize_piece_data(self):
        self.piece_data = copy.deepcopy(self.piece_data)
        self.piece_data['U'][-1]['rotations'] = (2, 3)

    def build_matrix(self):
        keys = sorted(self.pieces.keys())
        x_coords, x_aspect = self.pieces['X'][0]
        translated = x_aspect.translate((1, 0))
        self.build_matrix_row('X', translated)
        keys.remove('X')
        for key in keys:
            for coords, aspect in self.pieces[key]:
                for y in range(self.height - aspect.bounds[1] - (key == 'I')):
                    for x in range(self.width):
                        translated = aspect.translate((x, y), (self.width, 0))
                        self.build_matrix_row(key, translated)


class Pentominoes3x20TubeMatrix(Pentominoes):

    """
    Symmetry: restrict X to dx=1 & 6, dy=0; remove flip of F.
    """

    height = 3
    width = 20

    check_for_duplicates = True

    def customize_piece_data(self):
        self.piece_data = copy.deepcopy(self.piece_data)
        self.piece_data['F'][-1]['flips'] = None

    def build_matrix(self):
        keys = sorted(self.pieces.keys())
        x_coords, x_aspect = self.pieces['X'][0]
        for x in (1, 6):
            translated = x_aspect.translate((x, 0))
            self.build_matrix_row('X', translated)
        keys.remove('X')
        for key in keys:
            for coords, aspect in self.pieces[key]:
                for y in range(self.height):
                    for x in range(self.width - aspect.bounds[0]):
                        translated = aspect.translate((x, y), (0, self.height))
                        self.build_matrix_row(key, translated)


class Pentominoes8x8CenterHoleMatrix(Pentominoes):

    """65 solutions"""

    height = 8
    width = 8

    def coordinates(self):
        for y in range(self.height):
            for x in range(self.width):
                if 3 <= x <= 4 and 3 <= y <= 4:
                    continue
                yield coordsys.Cartesian2D((x, y))


class Pentominoes8x8CenterHoleMatrixA(Pentominoes8x8CenterHoleMatrix):

    def build_matrix(self):
        keys = sorted(self.pieces.keys())
        x_coords, x_aspect = self.pieces['X'][0]
        for x, y in ((1, 0), (2, 0)):
            translated = x_aspect.translate((x, 0))
            self.build_matrix_row('X', translated)
        keys.remove('X')
        self.build_regular_matrix(keys)


class Pentominoes8x8CenterHoleMatrixB(Pentominoes8x8CenterHoleMatrix):

    """symmetry: X on diagonal; remove flip of P"""

    def customize_piece_data(self):
        self.piece_data = copy.deepcopy(self.piece_data)
        self.piece_data['P'][-1]['flips'] = None

    def build_matrix(self):
        keys = sorted(self.pieces.keys())
        x_coords, x_aspect = self.pieces['X'][0]
        translated = x_aspect.translate((1, 1))
        self.build_matrix_row('X', translated)
        keys.remove('X')
        self.build_regular_matrix(keys)


class SolidPentominoes(Puzzle3D, Pentominoes):

    def make_aspects(self, units,
                     flips=(0, 1), axes=(0, 1, 2), rotations=(0, 1, 2, 3)):
        units = tuple((x, y, 0) for (x, y) in units) # convert to 3D
        return Puzzle3D.make_aspects(self, units, flips, axes, rotations)


class SolidPentominoes2x3x10Matrix(SolidPentominoes):

    """12 solutions"""

    height = 3
    width = 10
    depth = 2

    def customize_piece_data(self):
        self.piece_data = copy.deepcopy(self.piece_data)
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


class SolidPentominoes2x5x6Matrix(SolidPentominoes):

    """264 solutions"""

    height = 5
    width = 6
    depth = 2


class SolidPentominoes2x5x6MatrixA(SolidPentominoes2x5x6Matrix):

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


class SolidPentominoes2x5x6MatrixB(SolidPentominoes2x5x6Matrix):

    """symmetry: X in center; remove flip of F"""

    def customize_piece_data(self):
        self.piece_data = copy.deepcopy(self.piece_data)
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


class SolidPentominoes3x4x5Matrix(SolidPentominoes):

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


class SolidPentominoesRingMatrix(SolidPentominoes):

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
                        yield coordsys.Cartesian3D((x, y, z))

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
        self.matrix.append(headers)

    def build_regular_matrix(self, keys):
        for key in keys:
            for coords, aspect in self.pieces[key]:
                for z in range(self.depth - aspect.bounds[2]):
                    for y in range(self.height - aspect.bounds[1]):
                        for x in range(self.width - aspect.bounds[0]):
                            translated = aspect.translate((x, y, z))
                            if translated.issubset(self.solution_coords):
                                self.build_matrix_row(key, translated)

    def format_solution(self, solution,
                        x_reversed=False, y_reversed=False, z_reversed=False):
        order_functions = (lambda x: x, reversed)
        x_reversed_fn = order_functions[x_reversed]
        y_reversed_fn = order_functions[1 - y_reversed] # reversed by default
        z_reversed_fn = order_functions[z_reversed]
        z_unreversed_fn = order_functions[1 - z_reversed]
        s_matrix = [[[' '] * self.width for y in range(self.height)]
                    for z in range(self.depth)]
        for row in solution:
            piece = sorted(i.column.name for i in row.row_data())
            name = piece[-1]
            for cell_name in piece[:-1]:
                x, y, z = [int(d.strip()) for d in cell_name.split(',')]
                s_matrix[z][y][x] = name
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


class SolidPentominoes3x3x9RingMatrix(SolidPentominoesRingMatrix):

    """3 solutions"""

    width = 9
    height = 3
    depth = 3

    def build_matrix(self):
        keys = sorted(self.pieces.keys())
        for coords, aspect in self.pieces['X']:
            if aspect.bounds[0] == 0:   # YZ plane
                for z in range(2):
                    self.build_matrix_row('X', aspect)
            if aspect.bounds[2] == 0:   # XY plane
                for x in range(4):
                    translated = aspect.translate((x, 0, 0))
                    self.build_matrix_row('X', translated)
        keys.remove('X')
        self.build_regular_matrix(keys)


class SolidPentominoes3x4x8RingMatrix(SolidPentominoesRingMatrix):

    """0 solutions"""

    width = 8
    height = 3
    depth = 4


class SolidPentominoes3x5x7RingMatrix(SolidPentominoesRingMatrix):

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


class SolidPentominoes3x6x6RingMatrix(SolidPentominoesRingMatrix):

    """0 solutions"""

    width = 6
    height = 3
    depth = 6


class SolidPentominoes5x3x5RingMatrix(SolidPentominoesRingMatrix):

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


class SolidPentominoes5x4x4RingMatrix(SolidPentominoesRingMatrix):

    """0 solutions"""

    width = 4
    height = 5
    depth = 4


class SolidPentominoes6x3x4RingMatrix(SolidPentominoesRingMatrix):

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


class SomaCubes(Puzzle3D):

    piece_data = {
        'V': (((0, 1, 0), (1, 0, 0)), {}),
        'L': (((0, 1, 0), (1, 0, 0), ( 2,  0,  0)), {}),
        'T': (((0, 1, 0), (1, 0, 0), ( 0, -1,  0)), {}),
        'Z': (((0, 1, 0), (1, 0, 0), ( 1, -1,  0)), {}),
        'a': (((0, 1, 0), (1, 0, 0), ( 1,  0,  1)), {}),
        'b': (((0, 1, 0), (1, 0, 0), ( 1,  0, -1)), {}),
        'p': (((0, 1, 0), (1, 0, 0), ( 0,  0,  1)), {})}
    """(0,0,0) is implied."""

    check_for_duplicates = False

    def format_solution(self, solution,
                        x_reversed=False, y_reversed=False, z_reversed=False,
                        xy_swapped=False, xz_swapped=False, yz_swapped=False):
        order_functions = (lambda x: x, reversed)
        x_reversed_fn = order_functions[x_reversed]
        y_reversed_fn = order_functions[1 - y_reversed] # reversed by default
        z_reversed_fn = order_functions[z_reversed]
        s_matrix = [[[' '] * self.width for y in range(self.height)]
                    for z in range(self.depth)]
        for row in solution:
            piece = sorted(i.column.name for i in row.row_data())
            name = piece[-1]
            for cell_name in piece[:-1]:
                x, y, z = (int(d.strip()) for d in cell_name.split(','))
                if xy_swapped:
                    x, y = y, x
                if xz_swapped:
                    x, z = z, x
                if yz_swapped:
                    y, z = z, y
                s_matrix[z][y][x] = name
        return '\n'.join(
            '    '.join(' '.join(x_reversed_fn(s_matrix[z][y]))
                        for z in z_reversed_fn(range(self.depth))).rstrip()
            for y in y_reversed_fn(range(self.height)))


class Soma3x3x3Matrix(SomaCubes):

    """
    240 solutions
    symmetry: T fixed (at edge, in XY plane, leg at right);
    restrict p to 4 aspects (one leg down)
    """

    height = 3
    width = 3
    depth = 3

    def customize_piece_data(self):
        self.piece_data = copy.deepcopy(self.piece_data)
        self.piece_data['T'][-1]['flips'] = None
        self.piece_data['T'][-1]['axes'] = None
        self.piece_data['T'][-1]['rotations'] = None
        self.piece_data['p'][-1]['flips'] = None
        self.piece_data['p'][-1]['axes'] = (1,)

    def build_matrix(self):
        keys = sorted(self.pieces.keys())
        assert len(self.pieces['T']) == 1
        t_coords, t_aspect = self.pieces['T'][0]
        self.build_matrix_row('T', t_aspect)
        keys.remove('T')
        self.build_regular_matrix(keys)


class SomaCrystalMatrix(SomaCubes):

    """2800 solutions."""

    height = 3
    width = 3
    depth = 5

    # no duplicate_conditions, due to chiral nature of a & b

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if x + y <= z:
                        yield coordsys.Cartesian3D((x, y, z))


class SomaLongWallMatrix(SomaCubes):

    """104 solutions."""

    height = 6
    width = 6
    depth = 2

    # no duplicate_conditions, due to chiral nature of a & b

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if 4 <= x + y <= 6 - z:
                        yield coordsys.Cartesian3D((x, y, z))


class SomaHighWallMatrix(SomaCubes):

    """46 solutions."""

    height = 5
    width = 5
    depth = 3

    check_for_duplicates = True
    duplicate_conditions = ({'z_reversed': True, 'xy_swapped': True},)

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if 3 <= x + y <= 4:
                        yield coordsys.Cartesian3D((x, y, z))


class SomaBenchMatrix(SomaCubes):

    """0 solutions."""

    height = 2
    width = 9
    depth = 2

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if y + z < 2:
                        yield coordsys.Cartesian3D((x, y, z))


class SomaStepsMatrix(SomaCubes):

    """164 solutions."""

    height = 3
    width = 5
    depth = 3

    check_for_duplicates = True
    duplicate_conditions = ({'x_reversed': True, 'y_reversed': True},)

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if z <= x <= 4 - z:
                        yield coordsys.Cartesian3D((x, y, z))


class SomaBathtubMatrix(SomaCubes):

    """158 solutions."""

    height = 3
    width = 5
    depth = 2

    check_for_duplicates = True
    duplicate_conditions = ({'x_reversed': True, 'y_reversed': True},)

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if z != 1 or x == 0 or x == 4 or y == 0 or y == 2:
                        yield coordsys.Cartesian3D((x, y, z))


class SomaCurvedWallMatrix(SomaCubes):

    """66 solutions."""

    height = 3
    width = 5
    depth = 3

    check_for_duplicates = True
    duplicate_conditions = ({'x_reversed': True, 'z_reversed': True},)

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if   ((y == 2 and (1 <= x <= 3))
                          or (y == 1 and x != 2)
                          or (y == 0 and (x == 0 or x == 4))):
                        yield coordsys.Cartesian3D((x, y, z))


class SomaSquareWallMatrix(SomaCubes):

    """0 solutions."""

    height = 3
    width = 5
    depth = 3

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if y == 2 or x == 0 or x == 4:
                        yield coordsys.Cartesian3D((x, y, z))


class SomaSofaMatrix(SomaCubes):

    """32 solutions."""

    height = 3
    width = 5
    depth = 3

    check_for_duplicates = True
    duplicate_conditions = ({'yz_swapped': True, 'x_reversed': True},)

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if z == 0 or y == 0 or ((x == 0 or x == 4) and z == y == 1):
                        yield coordsys.Cartesian3D((x, y, z))


class SomaCornerstoneMatrix(SomaCubes):

    """10 solutions."""

    height = 5
    width = 5
    depth = 5

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if   ((z == 0 and x + y <= 4)
                          or (x == 0 and z + y <= 4)
                          or (z == x == 1 and y <= 1)):
                        yield coordsys.Cartesian3D((x, y, z))


class Soma_W_Matrix(SomaCubes):

    """0 solutions."""

    height = 5
    width = 5
    depth = 3

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if   ((x == 0 or x == 2 or y == 0 or y == 2)
                          and (2 <= x + y <= 4)):
                        yield coordsys.Cartesian3D((x, y, z))


class SomaSkew1Matrix(SomaCubes):

    """244 solutions."""

    height = 3
    width = 5
    depth = 3

    check_for_duplicates = True
    duplicate_conditions = ({'x_reversed': True, 'y_reversed': True},)

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if 2 <= x + y <= 4:
                        yield coordsys.Cartesian3D((x, y, z))


class SomaSkew2Matrix(SomaCubes):

    """14 solutions."""

    height = 3
    width = 7
    depth = 3

    check_for_duplicates = True
    duplicate_conditions = ({'x_reversed': True, 'y_reversed': True},)

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if 4 <= x + 2 * y <= 6:
                        yield coordsys.Cartesian3D((x, y, z))


class SomaSteamerMatrix(SomaCubes):

    """152 solutions."""

    height = 5
    width = 5
    depth = 3

    check_for_duplicates = True
    duplicate_conditions = ({'x_reversed': True, 'y_reversed': True},)

    def coordinates(self):
        for z in range(self.depth):
            for y in range(z, self.height - z):
                for x in range(z, self.width - z):
                    if 2 + 2 * z <= x + y + z <= 6:
                        yield coordsys.Cartesian3D((x, y, z))


class TetraSticks(Puzzle):

    piece_data = {
        'I': ((((0,0),(4,0)),), {}),
        'L': ((((0,0),(3,0)), ((3,0),(3,1))), {}),
        'Y': ((((0,0),(3,0)), ((2,0),(2,1))), {}),
        'V': ((((0,0),(2,0)), ((2,0),(2,2))), {}),
        'T': ((((0,0),(2,0)), ((1,0),(1,2))), {}),
        'X': ((((0,1),(2,1)), ((1,0),(1,2))), {}),
        'U': ((((0,0),(2,0)), ((0,0),(0,1)), ((2,0),(2,1))), {}),
        'N': ((((0,0),(2,0)), ((2,0),(2,1)), ((2,1),(3,1))), {}),
        'J': ((((0,0),(2,0)), ((2,0),(2,1)), ((2,1),(1,1))), {}),
        'H': ((((0,0),(2,0)), ((1,0),(1,1)), ((1,1),(2,1))), {}),
        'F': ((((0,0),(2,0)), ((0,0),(0,1)), ((1,0),(1,1))), {}),
        'Z': ((((0,0),(0,1)), ((0,1),(2,1)), ((2,1),(2,2))), {}),
        'R': ((((0,0),(0,1)), ((0,1),(2,1)), ((1,1),(1,2))), {}),
        'W': ((((0,0),(1,0)), ((1,0),(1,1)), ((1,1),(2,1)), ((2,1),(2,2))), {}),
        'P': ((((0,0),(0,1)), ((0,1),(1,1)), ((1,1),(1,0)), ((1,0),(2,0))), {}),
        'O': ((((0,0),(1,0)), ((1,0),(1,1)), ((1,1),(0,1)), ((0,1),(0,0))), {})}

    symmetric_pieces = 'I O T U V W X'.split()
    """Pieces with reflexive symmetry, identical to their mirror images."""

    asymmetric_pieces = 'F H J L N P R Y Z'.split()
    """Pieces without reflexive symmetry, different from their mirror images."""

    welded_pieces = 'F H R T X Y'.split()
    """Pieces with junction points (where 3 or more segments join)."""

    unwelded_pieces = 'I J L N O P U V W Z '.split()
    """Pieces without junction points (max. 2 segments join)."""

    def make_aspects(self, segments, flips=(0, 1), rotations=(0, 1, 2, 3)):
        aspects = set()
        polystick = coordsys.CartesianPath2D(segments)
        for flip in flips or (0,):
            for rotation in rotations or (0,):
                aspect = polystick.oriented(rotation, flip, normalized=True)
                aspects.add(aspect)
        return aspects


class PolySticks123(object):

    piece_data = {
        'I1': ((((0,0),(1,0)),), {}),
        'I2': ((((0,0),(2,0)),), {}),
        'V2': ((((0,0),(1,0)), ((0,0),(0,1))), {}),
        'I3': ((((0,0),(3,0)),), {}),
        'L3': ((((0,0),(2,0)), ((2,0),(2,1))), {}),
        'T3': ((((0,0),(2,0)), ((1,0),(1,1))), {}),
        'Z3': ((((0,1),(1,1)), ((1,1),(1,0)), ((1,0),(2,0))), {}),
        'U3': ((((0,1),(0,0)), ((0,0),(1,0)), ((1,0),(1,1))), {}),}


class TetraSticksMatrix(TetraSticks):

    def coordinates(self):
        return []

    def build_matrix_header(self):
        headers = []
        for i, key in enumerate(sorted(self.pieces.keys())):
            self.matrix_columns[key] = i
            headers.append(key)
        for y in range(self.height + 1):
            for x in range(self.width):
                header = '%0*i,%0*ih' % (
                    self.x_width, x, self.y_width, y)
                self.matrix_columns[header] = len(headers)
                headers.append(header)
        for x in range(self.width + 1):
            for y in range(self.height):
                header = '%0*i,%0*iv' % (
                    self.x_width, x, self.y_width, y)
                self.matrix_columns[header] = len(headers)
                headers.append(header)
        primary = len(headers)
        for y in range(1, self.height):
            for x in range(1, self.width):
                header = '%0*i,%0*ii' % (
                    self.x_width, x, self.y_width, y)
                self.matrix_columns[header] = len(headers)
                headers.append(header)
        self.secondary_columns = len(headers) - primary
        self.matrix.append(headers)

    def build_regular_matrix(self, keys):
        for key in keys:
            for coords, aspect in self.pieces[key]:
                for y in range(self.height + 1 - aspect.bounds[1]):
                    for x in range(self.width + 1 - aspect.bounds[0]):
                        translated = aspect.translate((x, y))
                        self.build_matrix_row(key, translated)

    def build_matrix_row(self, name, path):
        row = [0] * len(self.matrix[0])
        row[self.matrix_columns[name]] = name
        for label in path.labels((self.x_width, self.y_width)):
            if not label.endswith('i') or label in self.matrix_columns:
                row[self.matrix_columns[label]] = label
        self.matrix.append(row)

    def format_solution(self, solution,
                        x_reversed=False, y_reversed=False, xy_swapped=False,
                        rotation=False):
        order_functions = (lambda x: x, reversed)
        x_reversed_fn = order_functions[x_reversed]
        y_reversed_fn = order_functions[1 - y_reversed] # reversed by default
        h_matrix = [[' '] * self.width for y in range(self.height + 1)]
        v_matrix = [[' '] * (self.width + 1) for y in range(self.height)]
        matrices = {'h': h_matrix, 'v': v_matrix}
        title = ''
        for row in solution:
            piece = sorted(i.column.name for i in row.row_data())
            name = piece[-1]
            if piece[0] == '!':
                title = '(%s omitted)\n' % name
                continue
            for segment_name in piece[:-1]:
                direction = segment_name[-1]
                if direction == 'i':
                    continue
                x, y = (int(d.strip()) for d in segment_name[:-1].split(','))
                x, y, direction = self.rotate_segment(x, y, direction, rotation)
                if xy_swapped:
                    x, y = y, x
                    direction = 'hv'[direction == 'h']
                matrices[direction][y][x] = name
        lines = []
        for y in range(self.height + 1):
            lines.append(' ' + ' '.join(
                ('-%s--' % name)[:4]
                for name in x_reversed_fn(h_matrix[y])).rstrip())
            if y != self.height:
                lines.append(
                    '%s\n%s'
                    % ('    '.join(
                    name[0] for name in x_reversed_fn(v_matrix[y])).rstrip(),
                       '    '.join(
                    (name + '|')[1]
                    for name in x_reversed_fn(v_matrix[y])).rstrip()))
        return title + '\n'.join(y_reversed_fn(lines))

    def rotate_segment(self, x, y, direction, rotation):
        quadrant = rotation % 4
        if quadrant:
            coords = (x, y)
            x = (coords[quadrant % 2] * (-2 * ((quadrant + 1) // 2 % 2) + 1)
                 + self.width * ((quadrant + 1) // 2 % 2))
            y = (coords[(quadrant + 1) % 2] * (-2 * (quadrant // 2 % 2) + 1)
                 + self.height * (quadrant // 2 % 2))
            if  ((direction == 'v' and quadrant == 1)
                 or (direction == 'h' and quadrant == 2)):
                x -= 1
            elif ((direction == 'v' and quadrant == 2)
                  or (direction == 'h' and quadrant == 3)):
                y -= 1
            if quadrant != 2:
                direction = 'hv'[direction == 'h']
        return x, y, direction


class WeldedTetraSticks4x4Matrix(TetraSticksMatrix):

    """
    4 solutions (perfect solutions, i.e. no pieces cross).
    2 solutions are perfectly symmetrical in reflection.
    The other 2 solutions are isomorphic in reflection if we allow reflection.

    But we don't allow reflection while solving the puzzle, so we shouldn't
    allow reflection when counting solutions either.
    """

    width = 4
    height = 4

    check_for_duplicates = True
    duplicate_conditions = ({'rotation': 1},
                            {'rotation': 2},
                            {'rotation': 3},)

    def customize_piece_data(self):
        self.piece_data = copy.deepcopy(self.piece_data)
        for key in TetraSticksMatrix.unwelded_pieces:
            del self.piece_data[key]
        for key in TetraSticksMatrix.asymmetric_pieces:
            if key not in self.piece_data:
                continue
            self.piece_data[key][-1]['flips'] = None
            self.piece_data[key+'*'] = copy.deepcopy(self.piece_data[key])
            self.piece_data[key+'*'][-1]['flips'] = (1,)


class TetraSticks5x5Matrix(TetraSticksMatrix):

    """
    1795 solutions total:

    * 72 solutions omitting H
    * 382 omitting J
    * 607 omitting L
    * 530 omitting N
    * 204 omitting Y

    All are perfect solutions (i.e. no pieces cross).
    """

    width = 5
    height = 5

    check_for_duplicates = True
    duplicate_conditions = ({'xy_swapped': True},)

    def customize_piece_data(self):
        self.piece_data = copy.deepcopy(self.piece_data)
        self.piece_data['!'] = ((), {})

    def build_matrix(self):
        keys = sorted(self.pieces.keys())
        for name in 'HJLNY':
            row = [0] * len(self.matrix[0])
            row[self.matrix_columns['!']] = name
            row[self.matrix_columns[name]] = name
            self.matrix.append(row)
        x_coords, x_aspect = self.pieces['X'][0]
        self.build_matrix_row('X', x_aspect)
        for x in range(2):
            translated = x_aspect.translate((x, 1))
            self.build_matrix_row('X', translated)
        keys.remove('X')
        self.build_regular_matrix(keys)

    def make_aspects(self, segments, flips=(0, 1), rotations=(0, 1, 2, 3)):
        if segments:
            return TetraSticksMatrix.make_aspects(
                self, segments, flips=flips, rotations=rotations)
        return set()


class PolySticks1234Matrix(TetraSticksMatrix, PolySticks123):

    piece_data = copy.deepcopy(TetraSticks.piece_data)
    piece_data.update(copy.deepcopy(PolySticks123.piece_data))


class PolySticks1234_6x6Matrix(PolySticks1234Matrix):

    """
    ? solutions (very large number; over 35000 unique solutions in first
    position of X, I, & I1)
    (perfect solutions, i.e. no pieces cross).
    """

    width = 6
    height = 6


class PolySticks1234_6x6MatrixA(PolySticks1234_6x6Matrix):

    check_for_duplicates = True
    duplicate_conditions = ({'xy_swapped': True},)

    def build_matrix(self):
        keys = sorted(self.pieces.keys())
        x_coords, x_aspect = self.pieces['X'][0]
        self.build_matrix_row('X', x_aspect)
        translated = x_aspect.translate((1, 1))
        self.build_matrix_row('X', translated)
        keys.remove('X')
        self.build_regular_matrix(keys)


class PolySticks1234_6x6MatrixB(PolySticks1234_6x6Matrix):

    def build_matrix(self):
        keys = sorted(self.pieces.keys())
        x_coords, x_aspect = self.pieces['X'][0]
        translated = x_aspect.translate((0, 1))
        self.build_matrix_row('X', translated)
        keys.remove('X')
        self.build_regular_matrix(keys)


class PolySticks1234_6x6MatrixC(PolySticks1234_6x6Matrix):

    check_for_duplicates = True
    duplicate_conditions = ({'y_reversed': True},)

    def build_matrix(self):
        keys = sorted(self.pieces.keys())
        x_coords, x_aspect = self.pieces['X'][0]
        for x in range(2):
            translated = x_aspect.translate((x, 2))
            self.build_matrix_row('X', translated)
        keys.remove('X')
        self.build_regular_matrix(keys)


class PolySticks1234_6x6MatrixD(PolySticks1234_6x6Matrix):

    """symmetry: X at center; remove flip & rotation of P (fix one aspect)"""

    def customize_piece_data(self):
        self.piece_data = copy.deepcopy(self.piece_data)
        self.piece_data['P'][-1]['flips'] = None
        self.piece_data['P'][-1]['rotations'] = None

    def build_matrix(self):
        keys = sorted(self.pieces.keys())
        x_coords, x_aspect = self.pieces['X'][0]
        translated = x_aspect.translate((2, 2))
        self.build_matrix_row('X', translated)
        keys.remove('X')
        self.build_regular_matrix(keys)


class Polyhexes(Puzzle2D):

    """
    The shape of the matrix is defined by the `coordinates` generator method.
    The `width` and `height` attributes define the maximum bounds only.
    """

    check_for_duplicates = True

    def coordinates(self):
        for y in range(self.height):
            for x in range(self.width):
                yield coordsys.Hexagonal2D((x, y))

    def make_aspects(self, units, flips=(False, True),
                     rotations=(0, 1, 2, 3, 4, 5)):
        aspects = set()
        coord_list = ((0, 0),) + units
        for flip in flips or (0,):
            for rotation in rotations or (0,):
                aspect = coordsys.HexagonalView2D(coord_list, rotation, flip)
                aspects.add(aspect)
        return aspects

    def format_solution(self, solution,
                        rotate_180=False, row_reversed=False):
        s_matrix = [[self.empty_cell] * self.width for y in range(self.height)]
        for row in solution:
            piece = sorted(i.column.name for i in row.row_data())
            name = piece[-1]
            for cell_name in piece[:-1]:
                x, y = [int(d.strip()) for d in cell_name.split(',')]
                s_matrix[y][x] = name
        if rotate_180:
            s_matrix = [list(reversed(s_matrix[y]))
                        for y in reversed(range(self.height))]
        if row_reversed:
            out = []
            trim = (self.height - 1) // 2
            for y in range(self.height):
                index = self.height - 1 - y
                out.append(([self.empty_cell] * index
                            + s_matrix[index]
                            + [self.empty_cell] * y)[trim:-trim])
            s_matrix = out
        return self.format_hex_grid(s_matrix)

    empty_cell = '  '

    def empty_content(self, cell, x, y):
        return self.empty_cell

    def cell_content(self, cell, x, y):
        return cell

    def format_hex_grid(self, s_matrix, content=None):
        if content is None:
            content = self.empty_content
        width = len(s_matrix[0])
        height = len(s_matrix)
        output = []
        for x in range(width - 1, -1, -1):
            # padding for slanted top row:
            output.append([' ' * (x * 3 + 1)])
        for y in range(height - 1, -1, -1):
            output.append([])
            if s_matrix[y][0] != self.empty_cell:
                # leftmost edge:
                output.append(['\\'])
            else:
                output.append([' '])
            for x in range(width):
                cell = s_matrix[y][x]
                left_wall = right_wall = ' '
                ceiling = self.empty_cell
                if x > 0 and y < (height - 1):
                    if s_matrix[y + 1][x - 1] != cell:
                        left_wall = '/'
                elif cell != self.empty_cell:
                    left_wall = '/'
                if x < (width - 1):
                    if s_matrix[y][x + 1] != cell:
                        right_wall = '\\'
                elif cell != self.empty_cell:
                    right_wall = '\\'
                output[-2 - x].append(
                    left_wall + content(cell, x, y) + right_wall)
                if y < (height - 1):
                    if s_matrix[y + 1][x] != cell:
                        ceiling = '__'
                elif cell != self.empty_cell:
                    ceiling = '__'
                output[-3 - x].append(ceiling)
        for y in range(height - 1, 0, -1):
            if s_matrix[y][-1] != self.empty_cell:
                # rightmost bottom right edges:
                output[-width - 2 * y].append('/')
        for x in range(width):
            if s_matrix[0][x] != self.empty_cell:
                output[-x - 1].append('__/')
        for i in range(len(output)):
            output[i] = ''.join(output[i]).rstrip()
        while not output[-1].strip():
            output.pop()
        while not output[0].strip():
            output.pop(0)
        return '\n'.join(output) + '\n'


class Polyhexes123(object):

    piece_data = {
        'H1': ((), {}),
        'I2': ((( 1, 0),), {}),
        'I3': ((( 1, 0), ( 2, 0)), {}),
        'V3': ((( 1, 0), ( 1, 1)), {}),
        'A3': ((( 1, 0), ( 0, 1)), {}),}
    """(0,0) is implied."""

    symmetric_pieces = piece_data.keys() # all of them
    """Pieces with reflexive symmetry, identical to their mirror images."""

    asymmetric_pieces = ()
    """Pieces without reflexive symmetry, different from their mirror images."""


class Tetrahexes(Polyhexes):

    piece_data = {
        'I4': ((( 1, 0), ( 2, 0), ( 3, 0)), {}),
        'J4': ((( 1, 0), ( 2, 0), ( 2, 1)), {}),
        'P4': ((( 1, 0), ( 2, 0), ( 1, 1)), {}),
        'S4': ((( 1, 0), ( 1, 1), ( 2, 1)), {}),
        'U4': (((-1, 1), ( 1, 0), ( 1, 1)), {}),
        'Y4': ((( 1, 0), ( 2,-1), ( 1, 1)), {}),
        'O4': ((( 1, 0), ( 0, 1), ( 1, 1)), {}),}
    """(0,0) is implied."""

    symmetric_pieces = 'I4 O4 U4 Y4'.split()
    """Pieces with reflexive symmetry, identical to their mirror images."""

    asymmetric_pieces = 'L4 P4 S4'.split()
    """Pieces without reflexive symmetry, different from their mirror images."""


class Polyhex1234(Polyhexes123, Tetrahexes):

    piece_data = copy.deepcopy(Tetrahexes.piece_data)
    piece_data.update(copy.deepcopy(Polyhexes123.piece_data))

    symmetric_pieces = (tuple(Polyhexes123.symmetric_pieces)
                        + tuple(Tetrahexes.symmetric_pieces))

    asymmetric_pieces = (tuple(Polyhexes123.asymmetric_pieces)
                         + tuple(Tetrahexes.asymmetric_pieces))


class Pentahexes(Polyhexes):

    piece_data = {
        'I5': ((( 1, 0), ( 2, 0), ( 3, 0), ( 4, 0)), {}),
        'J5': ((( 1, 0), ( 2, 0), ( 3, 0), ( 3, 1)), {}),
        'P5': ((( 1, 0), ( 2, 0), ( 2, 1), ( 3, 0)), {}),
        'E5': ((( 1, 0), ( 1, 1), ( 2, 0), ( 3, 0)), {}),
        'N5': ((( 1, 0), ( 2, 0), ( 2, 1), ( 3, 1)), {}),
        'L5': ((( 1, 0), ( 2, 0), ( 2, 1), ( 2, 2)), {}),
        'r5': ((( 1, 0), ( 2, 0), ( 2, 1), ( 1, 2)), {}),
        'p5': ((( 1, 0), ( 2, 0), ( 1, 1), ( 2, 1)), {}),
        'u5': ((( 1, 0), ( 2, 0), ( 0, 1), ( 2, 1)), {}),
        'C5': ((( 1, 0), ( 2, 0), ( 2, 1), (-1, 1)), {}),
        'S5': ((( 1, 0), ( 2, 0), ( 2, 1), ( 0,-1)), {}),
        'q5': ((( 1, 0), ( 2, 0), ( 2, 1), ( 1,-1)), {}),
        'T5': ((( 1, 0), ( 2, 0), ( 2, 1), ( 2,-1)), {}),
        'Y5': ((( 1, 0), ( 2, 0), ( 2, 1), ( 3,-1)), {}),
        'D5': ((( 1, 0), ( 2, 0), ( 0, 1), ( 1, 1)), {}),
        'X5': ((( 1, 0), ( 2, 0), ( 0, 1), ( 2,-1)), {}),
        'A5': ((( 1, 0), ( 2, 0), ( 1, 1), ( 2,-1)), {}),
        'V5': ((( 1, 0), ( 2, 0), ( 0, 1), ( 0, 2)), {}),
        'U5': ((( 1, 0), ( 1, 1), (-1, 1), (-1, 2)), {}),
        'y5': ((( 1, 0), ( 1, 1), ( 0, 2), ( 2, 1)), {}),
        'G5': ((( 1, 0), ( 1, 1), ( 2, 1), ( 3, 0)), {}),
        'W5': ((( 1, 0), ( 1, 1), ( 2, 1), ( 2, 2)), {}),}
    """(0,0) is implied."""

    symmetric_pieces = 'I5 E5 L5 C5 Y5 D5 X5 A5 V5 U5 W5'.split()
    """Pieces with reflexive symmetry, identical to their mirror images."""

    asymmetric_pieces = 'J5 P5 N5 r5 p5 u5 S5 q5 T5 y5 G5'.split()
    """Pieces without reflexive symmetry, different from their mirror images."""


class Tetrahex4x7Matrix(Tetrahexes):

    """9 solutions"""

    height = 4
    width = 7

    duplicate_conditions = ({'rotate_180': True},)


class Tetrahex7x7TriangleMatrix(Tetrahexes):

    """0 solutions"""

    height = 7
    width = 7

    def coordinates(self):
        for y in range(self.height):
            for x in range(self.width):
                if x + y < self.height:
                    yield coordsys.Hexagonal2D((x, y))


class Tetrahex3x10ClippedMatrix(Tetrahexes):

    """2 solutions"""

    height = 3
    width = 10

    duplicate_conditions = ({'row_reversed': True},
                            {'rotate_180': True},
                            {'row_reversed': True, 'rotate_180': True},)

    def coordinates(self):
        max = self.width + self.height - 2
        for y in range(self.height):
            for x in range(self.width):
                if (x + y != 0) and (x + y != max):
                    yield coordsys.Hexagonal2D((x, y))


class TetrahexCoinMatrix(Tetrahexes):

    """4 solutions"""

    height = 5
    width = 7

    duplicate_conditions = ({'row_reversed': True},
                            {'rotate_180': True},
                            {'row_reversed': True, 'rotate_180': True},)

    def coordinates(self):
        max = self.width + self.height - 3
        for y in range(self.height):
            for x in range(self.width):
                if (x + y > 1) and (x + y < max) and not (x == 3 and y == 2):
                    yield coordsys.Hexagonal2D((x, y))


class Pentahex10x11Matrix(Pentahexes):

    """? (many) solutions"""

    height = 10
    width = 11

    duplicate_conditions = ({'rotate_180': True},)


class Pentahex5x22Matrix(Pentahexes):

    """? (many) solutions"""

    height = 5
    width = 22

    duplicate_conditions = ({'rotate_180': True},)


class Polyhex1234_4x10Matrix(Polyhex1234):

    """? (many) solutions"""

    height = 4
    width = 10

    duplicate_conditions = ({'rotate_180': True},)


class Polyhex1234_5x8Matrix(Polyhex1234):

    """? (many) solutions"""

    height = 5
    width = 8

    duplicate_conditions = ({'rotate_180': True},)


class Polyiamonds(Puzzle3D):

    """
    The shape of the matrix is defined by the `coordinates` generator method.
    The `width` and `height` attributes define the maximum bounds only.
    """

    depth = 2                           # triangle orientation: up=0, down=1

    check_for_duplicates = True

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    yield coordsys.Triangular3D((x, y, z))

    def make_aspects(self, units, flips=(False, True),
                     rotations=(0, 1, 2, 3, 4, 5)):
        aspects = set()
        coord_list = ((0, 0, 0),) + units
        for flip in flips or (0,):
            for rotation in rotations or (0,):
                aspect = coordsys.TriangularView3D(
                    coord_list, rotation, 0, flip) # 0 is axis, ignored
                aspects.add(aspect)
        return aspects

    def format_solution(self, solution,
                        rotate_180=False, row_reversed=False, xy_swapped=False):
        s_matrix = [[[self.empty_cell] * self.width
                     for y in range(self.height)]
                    for z in range(self.depth)]
        for row in solution:
            piece = sorted(i.column.name for i in row.row_data())
            name = piece[-1]
            for cell_name in piece[:-1]:
                x, y, z = [int(d.strip()) for d in cell_name.split(',')]
                s_matrix[z][y][x] = name
        if rotate_180:
            s_matrix = [[list(reversed(s_matrix[z][y]))
                         for y in reversed(range(self.height))]
                        for z in reversed(range(self.depth))]
        if row_reversed:
            out = []
            trim = (self.height - 1) // 2
            for y in range(self.height):
                index = self.height - 1 - y
                out.append(([self.empty_cell] * index
                            + s_matrix[index]
                            + [self.empty_cell] * y)[trim:-trim])
            s_matrix = out
        if xy_swapped:
            assert self.height == self.width, \
                   'Unable to swap x & y: dimensions not equal!'
            s_matrix = [[[s_matrix[z][x][y]
                          for x in range(self.height)]
                         for y in range(self.width)]
                        for z in range(self.depth)]
        return self.format_triangular_grid(s_matrix)

    empty_cell = '  '

    def empty_content(self, cell, x, y, z):
        return self.empty_cell

    def cell_content(self, cell, x, y, z):
        return cell

    def format_triangular_grid(self, s_matrix, content=None):
        if content is None:
            content = self.empty_content
        width = len(s_matrix[0][0])
        height = len(s_matrix[0])
        top = ['   ' * height]
        left_margin = len(top[0])
        for x in range(width):
            bottom = '_ '[s_matrix[1][-1][x] == self.empty_cell]
            top.append(bottom * 6)
        output = [''.join(top).rstrip()]
        for y in range(height - 1, -1, -1):
            padding = ' ' * 3 * y
            line1 = ['  ' + padding]
            line2 = [' ' + padding]
            line3 = [padding]
            for x in range(width):
                cell = s_matrix[0][y][x]
                left = bottom = ' '
                if ( x == 0 and cell != self.empty_cell
                     or x > 0 and s_matrix[1][y][x - 1] != cell):
                    left = '/'
                if ( y == 0 and cell != self.empty_cell
                     or y > 0 and s_matrix[1][y - 1][x] != cell):
                    bottom = '_'
                line1.append(left)
                line2.append(left + content(cell, x, y, 0))
                line3.append((bottom, left)[left != ' '] + bottom * 4)
                cell = s_matrix[1][y][x]
                left = ' '
                if s_matrix[0][y][x] != cell:
                    left = '\\'
                line1.append(left + '    ')
                line2.append(left + content(cell, x, y, 1))
                line3.append((bottom, left)[left != ' '])
            right = '/ '[cell == self.empty_cell]
            for line in line1, line2, line3:
                line = (''.join(line) + right).rstrip()
                output.append(line)
                left_margin = min(left_margin, len(line) - len(line.lstrip()))
        return '\n'.join(line[left_margin:] for line in output) + '\n'


class Hexiamonds(Polyiamonds):

    piece_data = {
        'I6': ((( 0, 0, 1), ( 1, 0, 0), ( 1, 0, 1), ( 2, 0, 0), ( 2, 0, 1)),
               {}),                     # Rhomboid or Bar
        'P6': ((( 0, 0, 1), ( 1, 0, 0), ( 1, 0, 1), ( 2, 0, 0), ( 1, 1, 0)),
               {}),                     # Sphinx
        'J6': ((( 0, 0, 1), ( 1, 0, 0), ( 1, 0, 1), ( 2, 0, 0), ( 0,-1, 1)),
               {}),                     # Club or Crook
        'E6': ((( 0, 0, 1), ( 1, 0, 0), ( 1, 0, 1), ( 2, 0, 0), ( 1,-1, 1)),
               {}),                     # Crown
        'V6': ((( 0, 0, 1), ( 1, 0, 0), ( 1, 0, 1), ( 0, 1, 0), ( 0, 1, 1)),
               {}),                     # Lobster
        'H6': ((( 0, 0, 1), ( 1, 0, 0), ( 1, 0, 1), ( 1,-1, 1), ( 2,-1, 0)),
               {}),                     # Pistol or Signpost
        'S6': ((( 0, 0, 1), ( 1, 0, 0), ( 1, 0, 1), ( 0,-1, 1), ( 1, 1, 0)),
               {}),                     # Snake
        'X6': ((( 0, 0, 1), ( 1, 0, 0), ( 1, 0, 1), ( 0, 1, 0), ( 1,-1, 1)),
               {}),                     # Butterfly
        'C6': ((( 0, 0, 1), ( 1, 0, 0), ( 1, 0, 1), ( 1, 1, 0), ( 1, 1, 1)),
               {}),                     # Bat or Chevron
        'G6': ((( 0, 0, 1), ( 1, 0, 0), ( 1, 0, 1), ( 1, 1, 0), ( 0, 1, 1)),
               {}),                     # Shoe or Hook
        'F6': ((( 0, 0, 1), ( 1, 0, 0), ( 1, 0, 1), ( 0, 1, 0), ( 1, 1, 0)),
               {}),                     # Yacht
        'O6': ((( 0, 0, 1), ( 1, 0, 0), ( 0,-1, 1), ( 1,-1, 0), ( 1,-1, 1)),
               {}),                     # Hexagon
        }
    """(0,0,0) is implied."""

    symmetric_pieces = 'E6 V6 X6 L6 O6'.split()
    """Pieces with reflexive symmetry, identical to their mirror images."""

    asymmetric_pieces = 'I6 P6 J6 H6 S6 G6 F6'.split()
    """Pieces without reflexive symmetry, different from their mirror images."""


class Hexiamonds4x9Matrix(Hexiamonds):

    """74 solutions"""

    height = 4
    width = 9

    duplicate_conditions = ({'rotate_180': True},)


class Hexiamonds6x6Matrix(Hexiamonds):

    """156 solutions"""

    height = 6
    width = 6

    duplicate_conditions = ({'rotate_180': True},
                            {'xy_swapped': True},
                            {'rotate_180': True, 'xy_swapped': True},)


class Hexiamonds4x11TrapeziumMatrix(Hexiamonds):

    """76 solutions"""

    height = 4
    width = 11

    check_for_duplicates = False

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if x + y + z < self.width:
                        yield coordsys.Triangular3D((x, y, z))

    def customize_piece_data(self):
        self.piece_data = copy.deepcopy(self.piece_data)
        self.piece_data['I6'][-1]['flips'] = None


class Hexiamonds6x9TrapeziumMatrix(Hexiamonds4x11TrapeziumMatrix):

    """0 solutions (impossible due to parity)"""

    height = 6
    width = 9


class Hexiamonds4x10LongHexagonMatrix(Hexiamonds):

    """856 solutions"""

    height = 4
    width = 10

    duplicate_conditions = ({'rotate_180': True},)

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if 1 < x + y + z <= self.width + 1:
                        yield coordsys.Triangular3D((x, y, z))

    def customize_piece_data(self):
        self.piece_data = copy.deepcopy(self.piece_data)
        self.piece_data['I6'][-1]['flips'] = None


class HexiamondsSnowflakeMatrix(Hexiamonds):

    """55 solutions"""

    height = 8
    width = 8

    check_for_duplicates = False

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
                        yield coordsys.Triangular3D((x, y, z))

    def customize_piece_data(self):
        self.piece_data = copy.deepcopy(self.piece_data)
        self.piece_data['J6'][-1]['rotations'] = None


class HexiamondsRingMatrix(Hexiamonds):

    """
    0 solutions

    8-unit high hexagon with a central 4-unit hexagonal hole.
    """

    height = 8
    width = 8

    check_for_duplicates = False

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if ( 3 < x + y + z < 12
                         and not (1 < x < 6 and 1 < y < 6
                                  and 5 < x + y + z < 10)):
                        yield coordsys.Triangular3D((x, y, z))


class HexiamondsRing2Matrix(Hexiamonds):

    """
    11 solutions

    8-unit high hexagon with a 4-unit hexagonal hole offset one unit from the
    center.
    """

    height = 8
    width = 8

    check_for_duplicates = False

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if ( 3 < x + y + z < 12
                         and not (2 < x < 7 and 1 < y < 6
                                  and 6 < x + y + z < 11)):
                        yield coordsys.Triangular3D((x, y, z))

    def customize_piece_data(self):
        self.piece_data = copy.deepcopy(self.piece_data)
        self.piece_data['I6'][-1]['flips'] = None


class HexiamondsCrescentMatrix(Hexiamonds):

    """
    87 solutions

    8-unit high hexagon with a 4-unit hexagonal bite removed from one corner.
    """

    height = 8
    width = 8

    check_for_duplicates = False

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if ( 3 < x + y + z < 12
                         and not (x > 3 and 1 < y < 6 and 7 < x + y + z)):
                        yield coordsys.Triangular3D((x, y, z))

    def customize_piece_data(self):
        self.piece_data = copy.deepcopy(self.piece_data)
        self.piece_data['I6'][-1]['flips'] = None


class HexiamondsCrescent2Matrix(Hexiamonds):

    """
    2 solutions

    8-unit high hexagon with a 4-unit hexagonal bite removed from one side.
    """

    height = 8
    width = 8

    check_for_duplicates = False

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if ( 3 < x + y + z < 12
                         and not (2 < x < 7 and 2 < y < 7 and 7 < x + y + z)):
                        yield coordsys.Triangular3D((x, y, z))

    def customize_piece_data(self):
        self.piece_data = copy.deepcopy(self.piece_data)
        self.piece_data['I6'][-1]['flips'] = None


if __name__ == '__main__':
    p = Pentominoes6x10Matrix()
    print 'matrix length =', len(p.matrix)
    print 'first 20 rows:'
    pprint(p.matrix[:20], width=720)
