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
import math
import re
from pprint import pprint, pformat
import coordsys
import colors


class DataError(RuntimeError): pass


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

    empty_cell = ' '

    margin = 1

    piece_data = {}
    """Mapping of piece names to 2-tuples (a copy.deepcopy is made first):

    * list of unit coordinates (usually one unit, the origin, is implicit)
    * dictionary of aspect restrictions, keyword arguments to `make_aspects`;
      customized in `customize_piece_data`
    """

    piece_colors = None
    """Mapping of piece names to colors.  The '0' name is reserved for
    formatting solution coordinates."""

    svg_header = '''\
<?xml version="1.0" standalone="no"?>
<!-- Created by Polyform Puzzler (http://puzzler.sourceforge.net/) -->
<svg width="%(width)s" height="%(height)s" viewBox="0 0 %(width)s %(height)s"
     xmlns="http://www.w3.org/2000/svg"
     xmlns:xlink="http://www.w3.org/1999/xlink">
'''
    svg_footer = '</svg>\n'
    svg_g_start = '<g>\n'
    svg_g_end = '</g>\n'

    svg_polygon = '''\
<polygon fill="%(color)s" stroke="%(stroke)s" stroke-width="%(stroke_width)s"
         points="%(points)s">
<desc>%(name)s</desc>
</polygon>
'''

    svg_stroke = 'white'
    """Polygon outline color."""

    svg_stroke_width = '1'
    """Width of polygon outline."""

    svg_unit_length = 10
    """Unit side length in pixels."""

    svg_unit_width = svg_unit_length
    """Unit width in pixels."""

    svg_unit_height = svg_unit_length
    """Unit height in pixels."""

    x3d_header = '''\
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE X3D PUBLIC "ISO//Web3D//DTD X3D 3.0//EN"
 "http://www.web3d.org/specifications/x3d-3.0.dtd">
<X3D profile="Immersive" version="2.0">
<Scene>
'''

    x3d_footer = '</Scene>\n</X3D>\n'

    @classmethod
    def components(cls):
        """Return a tuple of puzzle component classes (sub-puzzles)."""
        return (cls,)

    def __init__(self, init_puzzle=True):
        """
        Use `init_puzzle` to speed up initialization when not actually solving
        the puzzle.
        """

        self.solutions = set()
        """Set of all permutations of solutions, for duplicate checking."""

        self.solution_coords = set(self.coordinates())
        """A set of all coordinates that make up the solution area/space."""

        self.aspects = {}
        """Mapping of piece name to a set of aspects (pieces in all
        orientations)."""

        self.pieces = {}
        """Mapping of piece name to a sorted list of 2-tuples: sorted
        coordinates & aspect objects.  Ensures reproducible results."""

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

        # Make an object-local deep copy of the dict:
        self.piece_data = copy.deepcopy(self.piece_data)
        # Now we can modify it as we like:
        self.customize_piece_data()

        if init_puzzle:
            self.init_puzzle()

    def init_puzzle(self):
        """Initialize the puzzle pieces and matrix."""
        for name, (data, kwargs) in self.piece_data.items():
            self.aspects[name] = self.make_aspects(data, **kwargs)
        for name, aspects in self.aspects.items():
            self.pieces[name] = tuple(sorted((tuple(sorted(aspect)), aspect)
                                             for aspect in aspects))
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
        Make instance-specific customizations to copies of `self.piece_data`
        and `self.piece_colors`.

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

    def build_regular_matrix(self, keys):
        """
        Build `self.matrix` rows from puzzle pieces listed in `keys`.

        Implement in subclasses.
        """
        raise NotImplementedError

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

    def format_svg(self, solution=None, s_matrix=None):
        """
        Return a puzzle-specific SVG formatting of a solution.

        Implement in subclasses.
        """
        raise NotImplementedError

    def write_svg(self, output_path, solution=None, s_matrix=None):
        try:
            svg = self.format_svg(solution, s_matrix)
        except NotImplementedError:
            print >>sys.stderr, (
                'Warning: SVG output not supported by this puzzle.\n')
        else:
            try:
                svg_file = open(output_path, 'w')
                svg_file.write(svg)
            finally:
                svg_file.close()

    def format_x3d(self, solution=None, s_matrix=None):
        """
        Return a puzzle-specific X3D formatting of a solution.

        Implement in subclasses.
        """
        raise NotImplementedError

    def write_x3d(self, output_path, solution=None, s_matrix=None):
        try:
            x3d = self.format_x3d(solution, s_matrix)
        except NotImplementedError:
            print >>sys.stderr, (
                'Warning: X3D output not supported by this puzzle.\n')
        else:
            try:
                x3d_file = open(output_path, 'w')
                x3d_file.write(x3d)
            finally:
                x3d_file.close()

    solution_header = re.compile(r'^solution (\d)+:$', re.IGNORECASE)

    def read_solution(self, input_path):
        if input_path == '-':
            input_file = sys.stdin
        else:
            input_file = open(input_path, 'r')
            try:
                for line in input_file:
                    match = self.solution_header.match(line)
                    if match:
                        number = int(match.group(1))
                        break
                else:
                    raise DataError('Input does not contain a solution record.')
                record = []
                for line in input_file:
                    line = line.strip()
                    if not line:
                        break
                    record.append(line)
            finally:
                input_file.close()
        s_matrix = self.convert_record_to_solution_matrix(record)
        return s_matrix

    def convert_record_to_solution_matrix(self, record):
        """
        `record` is a list of strings, the solution record.

        Implement in subclasses
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
        s_matrix = self.build_solution_matrix(solution)
        return '\n'.join(''.join('%-2s' % name
                                 for name in x_reversed_fn(s_matrix[y])
                                 ).rstrip()
                         for y in y_reversed_fn(range(self.height)))

    def empty_solution_matrix(self, margin=0):
        s_matrix = [[self.empty_cell] * (self.width + 2 * margin)
                    for y in range(self.height + 2 * margin)]
        return s_matrix

    def build_solution_matrix(self, solution, margin=0):
        s_matrix = self.empty_solution_matrix(margin)
        for row in solution:
            name = row[-1]
            for cell_name in row[:-1]:
                x, y = [int(d.strip()) for d in cell_name.split(',')]
                s_matrix[y + margin][x + margin] = name
        return s_matrix

    def format_svg(self, solution=None, s_matrix=None):
        if s_matrix:
            assert solution is None, ('Provide only one of solution '
                                      '& s_matrix arguments, not both.')
        else:
            s_matrix = self.build_solution_matrix(solution, margin=1)
        polygons = []
        for y in range(1, self.height + 1):
            for x in range(1, self.width + 1):
                if s_matrix[y][x] == self.empty_cell:
                    continue
                polygons.append(self.build_polygon(s_matrix, x, y))
        header = self.svg_header % {
            'height': (self.height + 2) * self.svg_unit_length,
            'width': (self.width + 2) * self.svg_unit_length}
        return '%s%s%s%s%s' % (header, self.svg_g_start, ''.join(polygons),
                               self.svg_g_end, self.svg_footer)

    def build_polygon(self, s_matrix, x, y):
        points = self.get_polygon_points(s_matrix, x, y)
        name = s_matrix[y][x]
        color = self.piece_colors[name]
        # Erase cells of this piece:
        for x, y in self.get_piece_cells(s_matrix, x, y):
            s_matrix[y][x] = self.empty_cell
        points_str = ' '.join('%.3f,%.3f' % (x, y) for (x, y) in points)
        return self.svg_polygon % {'color': color,
                                   'stroke': self.svg_stroke,
                                   'stroke_width': self.svg_stroke_width,
                                   'points': points_str,
                                   'name': name}

    edge_trace = {(+1,  0): ((( 0, -1), ( 0, -1)), # right
                             (( 0,  0), (+1,  0)),
                             (None,     ( 0, +1))),
                  (-1,  0): (((-1,  0), ( 0, +1)), # left
                             ((-1, -1), (-1,  0)),
                             (None,     ( 0, -1))),
                  ( 0, +1): ((( 0,  0), (+1,  0)), # up
                             ((-1,  0), ( 0, +1)),
                             (None,     (-1,  0))),
                  ( 0, -1): (((-1, -1), (-1,  0)), # down
                             (( 0, -1), ( 0, -1)),
                             (None,     (+1,  0))),}
    """Mapping of counterclockwise (x,y)-direction vector to list (ordered by
    test) of 2-tuples: examination cell coordinate delta & new direction
    vector."""

    def get_polygon_points(self, s_matrix, x, y):
        """
        Return a list of coordinate tuples, the corner points of the polygon
        for the piece at (x,y).
        """
        cell_content = s_matrix[y][x]
        unit = self.svg_unit_length
        height = (self.height + 2) * unit
        points = [(x * unit, height - y * unit)]
        direction = (+1, 0)             # to the right
        start = (x, y)
        x += 1
        while (x, y) != start:
            for delta, new_direction in self.edge_trace[direction]:
                if ( delta is None
                     or cell_content != '0'
                     and s_matrix[y + delta[1]][x + delta[0]] == cell_content):
                    break
            if new_direction != direction:
                direction = new_direction
                points.append((x * unit, height - y * unit))
            x += direction[0]
            y += direction[1]
        return points

    def get_piece_cells(self, s_matrix, x, y):
        cell_content = s_matrix[y][x]
        coord = self.coord_class((x, y))
        cells = set([coord])
        if cell_content != '0':
            self._get_piece_cells(cells, coord, s_matrix, cell_content)
        return cells

    def _get_piece_cells(self, cells, coord, s_matrix, cell_content):
        for neighbor in coord.neighbors():
            x, y = neighbor
            if neighbor not in cells and s_matrix[y][x] == cell_content:
                cells.add(neighbor)
                self._get_piece_cells(cells, neighbor, s_matrix, cell_content)

    def format_coords_svg(self):
        s_matrix = self.empty_solution_matrix(margin=self.margin)
        for x, y in self.solution_coords:
            s_matrix[y + self.margin][x + self.margin] = '0'
        return self.format_svg(s_matrix=s_matrix)

    def convert_record_to_solution_matrix(self, record):
        s_matrix = self.empty_solution_matrix(self.margin)
        for row in record:
            parts = row.split()
            name = parts[-1]
            for coords in parts[:-1]:
                x, y = coords.split(',')
                s_matrix[int(y) + self.margin][int(x) + self.margin] = name
        return s_matrix


class Puzzle3D(Puzzle):

    margin = 0
    piece_width = 2                     # for format_solution
    svg_x_width = 9
    svg_x_height = -2
    svg_y_height = 10
    svg_z_height = -3
    svg_z_width = -6
    svg_stroke_width = '0.5'
    svg_defs_start = '<defs>\n'
    svg_cube_def = '''\
<symbol id="cube%(name)s">
<polygon fill="%(color)s" stroke="%(stroke)s"
         stroke-width="%(stroke_width)s" stroke-linejoin="round"
         points="0,13 9,15 15,12 15,2 6,0 0,3" />
<polygon fill="black" fill-opacity="0.25" stroke="%(stroke)s"
         stroke-width="%(stroke_width)s" stroke-linejoin="round"
         points="9,15 15,12 15,2 9,5" />
<polygon fill="white" fill-opacity="0.30" stroke="%(stroke)s"
         stroke-width="%(stroke_width)s" stroke-linejoin="round"
         points="0,3 9,5 15,2 6,0" />
</symbol>
'''
    svg_defs_end = '</defs>\n'
    svg_cube = '<use xlink:href="#cube%(name)s" x="%(x).3f" y="%(y).3f" />\n'

    x3d_box = '''\
<Transform translation="%(x)s %(y)s %(z)s">
  <Shape>
    <Appearance>
      <Material diffuseColor="%(color)s"/>
    </Appearance>
    <Box size="1 1 1"/>
  </Shape>
</Transform>
'''

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
                        x_reversed=False, y_reversed=False, z_reversed=False,
                        xy_swapped=False, xz_swapped=False, yz_swapped=False):
        order_functions = (lambda x: x, reversed)
        x_reversed_fn = order_functions[x_reversed]
        y_reversed_fn = order_functions[1 - y_reversed] # reversed by default
        z_reversed_fn = order_functions[z_reversed]
        #s_matrix = self.build_solution_matrix(solution)
        s_matrix = self.empty_solution_matrix()
        for row in solution:
            name = row[-1]
            for cell_name in row[:-1]:
                x, y, z = (int(d.strip()) for d in cell_name.split(','))
                if xy_swapped:
                    x, y = y, x
                if xz_swapped:
                    x, z = z, x
                if yz_swapped:
                    y, z = z, y
                s_matrix[z][y][x] = name
        return '\n'.join(
            '    '.join(''.join('%-*s' % (self.piece_width, name)
                                for name in x_reversed_fn(s_matrix[z][y]))
                        for z in z_reversed_fn(range(self.depth))).rstrip()
            for y in y_reversed_fn(range(self.height)))

    def empty_solution_matrix(self, margin=0):
        s_matrix = [[[self.empty_cell] * (self.width + 2 * margin)
                     for y in range(self.height + 2 * margin)]
                    for z in range(self.depth + 2 * margin)]
        return s_matrix

    def build_solution_matrix(self, solution, margin=0):
        s_matrix = self.empty_solution_matrix(margin)
        for row in solution:
            name = row[-1]
            for cell_name in row[:-1]:
                x, y, z = [int(d.strip()) for d in cell_name.split(',')]
                s_matrix[z + margin][y + margin][x + margin] = name
        return s_matrix

    def format_svg(self, solution=None, s_matrix=None):
        if s_matrix:
            assert solution is None, ('Provide only one of solution '
                                      '& s_matrix arguments, not both.')
        else:
            s_matrix = self.build_solution_matrix(solution)
        s_matrix = self.transform_solution_matrix(s_matrix)
        s_depth = len(s_matrix)
        s_height = len(s_matrix[0])
        s_width = len(s_matrix[0][0])
        height = (s_height * abs(self.svg_y_height)
                  + s_depth * abs(self.svg_z_height)
                  + s_width * abs(self.svg_x_height)
                  + 2 * self.svg_unit_length)
        width = (s_width * abs(self.svg_x_width)
                  + s_depth * abs(self.svg_z_width)
                  + 2 * self.svg_unit_length)
        cube_defs = []
        for name in sorted(self.piece_colors.keys()):
            color = self.piece_colors[name]
            cube_defs.append(
                self.svg_cube_def % {'color': color,
                                     'stroke': self.svg_stroke,
                                     'stroke_width': self.svg_stroke_width,
                                     'name': name})
        cubes = []
        for z in range(s_depth):
            for y in range(s_height):
                for x in range(s_width):
                    name = s_matrix[z][y][x]
                    if name == self.empty_cell:
                        continue
                    cubes.append(
                        self.svg_cube
                        % {'name': name,
                           'x': (x * self.svg_x_width
                                 + (z + 1 - s_depth) * self.svg_z_width
                                 + self.svg_unit_length),
                           'y': (height
                                 - (y * self.svg_y_height
                                    + (z - s_depth) * self.svg_z_height
                                    + (x - s_width) * self.svg_x_height
                                    + 2 * self.svg_unit_length))})
        header = self.svg_header % {'height': height, 'width': width}
        defs = '%s%s%s' % (self.svg_defs_start, ''.join(cube_defs),
                           self.svg_defs_end)
        return '%s%s%s%s%s%s' % (header, defs, self.svg_g_start,
                                 ''.join(cubes), self.svg_g_end,
                                 self.svg_footer)

    def format_coords_svg(self):
        s_matrix = self.empty_solution_matrix(margin=self.margin)
        for x, y, z in self.solution_coords:
            s_matrix[z + self.margin][y + self.margin][x + self.margin] = '0'
        return self.format_svg(s_matrix=s_matrix)

    def format_x3d(self, solution=None, s_matrix=None):
        if s_matrix:
            assert solution is None, ('Provide only one of solution '
                                      '& s_matrix arguments, not both.')
        else:
            s_matrix = self.build_solution_matrix(solution)
        s_matrix = self.transform_solution_matrix(s_matrix)
        s_depth = len(s_matrix)
        s_height = len(s_matrix[0])
        s_width = len(s_matrix[0][0])
        cubes = []
        for z in range(s_depth):
            for y in range(s_height):
                for x in range(s_width):
                    name = s_matrix[z][y][x]
                    if name == self.empty_cell:
                        continue
                    cubes.append(
                        self.x3d_box
                        % {'name': name, 'x': x, 'y': y, 'z': z,
                           'color': colors.x3d[self.piece_colors[name]]})
        return '%s%s%s' % (self.x3d_header, ''.join(cubes), self.x3d_footer)

    def transform_solution_matrix(self, s_matrix):
        """Transform for rendering `s_matrix`.  Override in subclasses."""
        return s_matrix

    def swap_yz_transform(self, s_matrix):
        """Common solution matrix transform: Z, Y = reversed(Y), Z."""
        return [[[s_matrix[z][y][x] for x in range(self.width)]
                 for z in range(self.depth)]
                for y in reversed(range(self.height))]

    def cycle_xyz_transform(self, s_matrix):
        """Common solution matrix transform: cycle X Y & Z dimensions."""
        return [[[s_matrix[z][y][x] for y in range(self.height)]
                 for z in range(self.depth)]
                for x in range(self.width)]

    def convert_record_to_solution_matrix(self, record):
        s_matrix = self.empty_solution_matrix(self.margin)
        for row in record:
            parts = row.split()
            name = parts[-1]
            for coords in parts[:-1]:
                x, y, z = (int(coord) + self.margin
                           for coord in coords.split(','))
                s_matrix[z][y][x] = name
        return s_matrix


class PuzzlePseudo3D(Puzzle3D):

    """The Z dimension is used for direction/orientation."""

    def empty_solution_matrix(self, margin=0):
        s_matrix = [[[self.empty_cell] * (self.width + 2 * margin)
                     for y in range(self.height + 2 * margin)]
                    for z in range(self.depth)]
        return s_matrix

    def build_solution_matrix(self, solution, margin=0):
        s_matrix = self.empty_solution_matrix(margin)
        for row in solution:
            name = row[-1]
            for cell_name in row[:-1]:
                x, y, z = [int(d.strip()) for d in cell_name.split(',')]
                s_matrix[z][y + margin][x + margin] = name
        return s_matrix

    def format_coords_svg(self):
        s_matrix = self.empty_solution_matrix(margin=self.margin)
        for x, y, z in self.solution_coords:
            s_matrix[z][y + self.margin][x + self.margin] = '0'
        return self.format_svg(s_matrix=s_matrix)

    def format_x3d(self, solution=None, s_matrix=None):
        raise NotImplementedError


class Pentominoes(Puzzle2D):

    coord_class = coordsys.Cartesian2D

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

    piece_colors = {
        'I': 'blue',
        'X': 'red',
        'F': 'green',
        'L': 'lime',
        'N': 'navy',
        'P': 'magenta',
        'T': 'darkorange',
        'U': 'turquoise',
        'V': 'blueviolet',
        'W': 'maroon',
        'Y': 'gold',
        'Z': 'plum',
        '0': 'gray'}


class Pentominoes6x10(Pentominoes):

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


class Pentominoes5x12(Pentominoes):

    """1010 solutions"""

    height = 5
    width = 12

    @classmethod
    def components(cls):
        return (Pentominoes5x12A, Pentominoes5x12B)


class Pentominoes5x12A(Pentominoes5x12):

    def build_matrix(self):
        keys = sorted(self.pieces.keys())
        x_coords, x_aspect = self.pieces['X'][0]
        for x in range(1, 5):
            translated = x_aspect.translate((x, 0))
            self.build_matrix_row('X', translated)
        keys.remove('X')
        self.build_regular_matrix(keys)


class Pentominoes5x12B(Pentominoes5x12):

    """symmetry: X at center; remove flip of P"""

    def customize_piece_data(self):
        self.piece_data['P'][-1]['flips'] = None

    def build_matrix(self):
        keys = sorted(self.pieces.keys())
        x_coords, x_aspect = self.pieces['X'][0]
        for x in range(5):
            translated = x_aspect.translate((x, 1))
            self.build_matrix_row('X', translated)
        keys.remove('X')
        self.build_regular_matrix(keys)


class Pentominoes4x15(Pentominoes):

    """368 solutions"""

    height = 4
    width = 15

    @classmethod
    def components(cls):
        return (Pentominoes4x15A, Pentominoes4x15B)


class Pentominoes4x15A(Pentominoes4x15):

    def build_matrix(self):
        keys = sorted(self.pieces.keys())
        x_coords, x_aspect = self.pieces['X'][0]
        for x in range(1, 6):
            translated = x_aspect.translate((x, 0))
            self.build_matrix_row('X', translated)
        keys.remove('X')
        self.build_regular_matrix(keys)


class Pentominoes4x15B(Pentominoes4x15):

    """symmetry: X at center; remove flip of P"""

    def customize_piece_data(self):
        self.piece_data['P'][-1]['flips'] = None

    def build_matrix(self):
        keys = sorted(self.pieces.keys())
        x_coords, x_aspect = self.pieces['X'][0]
        translated = x_aspect.translate((6, 0))
        self.build_matrix_row('X', translated)
        keys.remove('X')
        self.build_regular_matrix(keys)


class Pentominoes3x20(Pentominoes):

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


class Pentominoes3x20Loop(Pentominoes):

    """
    2 solutions: same as non-loop `Pentominoes3x20`.
    Symmetry: fix X; restrict U to 2 quadrants; restrict I to y=0 & 1.
    """

    height = 3
    width = 20

    def customize_piece_data(self):
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


class Pentominoes3x20Tube(Pentominoes):

    """
    Symmetry: restrict X to dx=1 & 6, dy=0; remove flip of F.
    """

    height = 3
    width = 20

    check_for_duplicates = True

    def customize_piece_data(self):
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


class Pentominoes8x8CenterHole(Pentominoes):

    """65 solutions"""

    height = 8
    width = 8

    @classmethod
    def components(cls):
        return (Pentominoes8x8CenterHoleA,
                Pentominoes8x8CenterHoleB)

    def coordinates(self):
        for y in range(self.height):
            for x in range(self.width):
                if 3 <= x <= 4 and 3 <= y <= 4:
                    continue
                yield coordsys.Cartesian2D((x, y))


class Pentominoes8x8CenterHoleA(Pentominoes8x8CenterHole):

    def build_matrix(self):
        keys = sorted(self.pieces.keys())
        x_coords, x_aspect = self.pieces['X'][0]
        for x, y in ((1, 0), (2, 0)):
            translated = x_aspect.translate((x, 0))
            self.build_matrix_row('X', translated)
        keys.remove('X')
        self.build_regular_matrix(keys)


class Pentominoes8x8CenterHoleB(Pentominoes8x8CenterHole):

    """symmetry: X on diagonal; remove flip of P"""

    def customize_piece_data(self):
        self.piece_data['P'][-1]['flips'] = None

    def build_matrix(self):
        keys = sorted(self.pieces.keys())
        x_coords, x_aspect = self.pieces['X'][0]
        translated = x_aspect.translate((1, 1))
        self.build_matrix_row('X', translated)
        keys.remove('X')
        self.build_regular_matrix(keys)


class OneSidedPentominoes(Pentominoes):

    def customize_piece_data(self):
        """
        Disable flips on all pieces, and add flipped versions of asymmetric
        pieces.
        """
        self.piece_colors = copy.deepcopy(self.piece_colors)
        for key in self.piece_data.keys():
            self.piece_data[key][-1]['flips'] = None
        for key in self.asymmetric_pieces:
            self.piece_data[key.lower()] = copy.deepcopy(self.piece_data[key])
            self.piece_data[key.lower()][-1]['flips'] = (1,)
            self.piece_colors[key.lower()] = self.piece_colors[key]

    def format_solution(self, *args, **kwargs):
        """Convert solutions to uppercase to avoid duplicates."""
        solution = Pentominoes.format_solution(self, *args, **kwargs)
        return solution.upper()


class OneSidedPentominoes3x30(OneSidedPentominoes):

    height = 3
    width = 30

    check_for_duplicates = True

    duplicate_conditions = ({'x_reversed': True},
                            {'y_reversed': True},
                            {'x_reversed': True, 'y_reversed': True})


class OneSidedPentominoes5x18(OneSidedPentominoes3x30):

    height = 5
    width = 18


class OneSidedPentominoes6x15(OneSidedPentominoes3x30):

    height = 6
    width = 15


class OneSidedPentominoes9x10(OneSidedPentominoes3x30):

    height = 9
    width = 10


class SolidPentominoes(Puzzle3D, Pentominoes):

    def make_aspects(self, units,
                     flips=(0, 1), axes=(0, 1, 2), rotations=(0, 1, 2, 3)):
        units = tuple((x, y, 0) for (x, y) in units) # convert to 3D
        return Puzzle3D.make_aspects(self, units, flips, axes, rotations)


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
                for z in range(2):
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
                        yield coordsys.Cartesian3D((x, y, z))


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
                        yield coordsys.Cartesian3D((x, y, z))


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
                yield coordsys.Cartesian3D((x, y, z))


class Tetracubes(Puzzle3D):

    piece_data = {
        'I':  ((( 1,  0,  0), ( 2,  0,  0), ( 3,  0,  0)), {}),
        'L':  (((-1,  0,  0), ( 1,  0,  0), ( 1,  1,  0)), {}),
        'T':  ((( 1,  0,  0), ( 2,  0,  0), ( 1,  1,  0)), {}),
        'S':  (((-1,  0,  0), ( 0,  1,  0), ( 1,  1,  0)), {}),
        'O':  ((( 1,  0,  0), ( 0,  1,  0), ( 1,  1,  0)), {}),
        'V1': ((( 0,  1,  0), ( 1,  0,  0), ( 0,  1,  1)), {}),
        'V2': ((( 0,  1,  0), ( 1,  0,  0), ( 0,  0,  1)), {}),
        'V3': ((( 0,  1,  0), ( 1,  0,  0), ( 1,  0,  1)), {}),}
    """(0,0,0) is implied.  The names are based on Kadon's 'Poly-4 Supplement'
    names.  See http://www.gamepuzzles.com/poly4.htm."""

    piece_colors = {
        'I': 'blue',
        'O': 'magenta',
        'T': 'green',
        'S': 'lime',
        'L': 'blueviolet',
        'V1': 'gold',
        'V2': 'red',
        'V3': 'navy',
        '0': 'gray'}


class Tetracubes2x4x4(Tetracubes):

    """1390 solutions"""

    width = 4
    height = 4
    depth = 2

    transform_solution_matrix = Puzzle3D.swap_yz_transform

    def customize_piece_data(self):
        self.piece_data['V2'][-1]['rotations'] = None
        self.piece_data['V2'][-1]['flips'] = None
        self.piece_data['V2'][-1]['axes'] = None


class Tetracubes2x2x8(Tetracubes):

    """224 solutions"""

    width = 8
    height = 2
    depth = 2

    def customize_piece_data(self):
        self.piece_data['V2'][-1]['rotations'] = None
        self.piece_data['V2'][-1]['flips'] = None
        self.piece_data['V2'][-1]['axes'] = None


class Pentacubes(Puzzle3D):

    non_planar_piece_data = {
        'L1': (((-1,  0,  0), ( 1,  0,  0), ( 1,  1,  0), (-1,  0,  1)), {}),
        'L2': (((-1,  0,  0), ( 1,  0,  0), ( 1,  1,  0), ( 0,  0,  1)), {}),
        'L3': (((-1,  0,  0), ( 1,  0,  0), ( 1,  1,  0), ( 1,  0,  1)), {}),
        'L4': (((-1,  0,  0), ( 1,  0,  0), ( 1,  1,  0), ( 1,  1,  1)), {}),
        'J1': (((-1,  0,  0), ( 1,  0,  0), ( 1,  1,  0), (-1,  0, -1)), {}),
        'J2': (((-1,  0,  0), ( 1,  0,  0), ( 1,  1,  0), ( 0,  0, -1)), {}),
        'J4': (((-1,  0,  0), ( 1,  0,  0), ( 1,  1,  0), ( 1,  1, -1)), {}),
        'N1': (((-1,  0,  0), ( 0,  1,  0), ( 1,  1,  0), (-1,  0, -1)), {}),
        'N2': (((-1,  0,  0), ( 0,  1,  0), ( 1,  1,  0), ( 0,  0, -1)), {}),
        'S1': (((-1,  0,  0), ( 0,  1,  0), ( 1,  1,  0), (-1,  0,  1)), {}),
        'S2': (((-1,  0,  0), ( 0,  1,  0), ( 1,  1,  0), ( 0,  0,  1)), {}),
        'T1': (((-1, -1,  0), (-1,  0,  0), (-1,  1,  0), (-1,  0,  1)), {}),
        'T2': (((-1, -1,  0), (-1,  0,  0), (-1,  1,  0), ( 0,  0,  1)), {}),
        'V1': (((-1,  0,  0), ( 0,  1,  0), (-1,  0,  1), (-1, -1,  1)), {}),
        'V2': (((-1,  0,  0), ( 0,  1,  0), ( 0,  1,  1), ( 1,  1,  1)), {}),
        'Q':  ((( 1,  0,  0), ( 0,  1,  0), ( 1,  1,  0), ( 0,  0,  1)), {}),
        'A':  ((( 1,  0,  0), ( 1,  1,  0), ( 0,  0,  1), ( 1,  1,  1)), {}),}
    """(0,0,0) is implied.  The names are based on Kadon's 'Superquints' names.
    Kadon's 'J3' piece is a duplicate of the 'L3' piece.
    See http://www.gamepuzzles.com/sqnames.htm."""

    piece_colors = {
        'L1': 'darkseagreen',
        'L2': 'peru',
        'L3': 'rosybrown',
        'L4': 'yellowgreen',
        'J1': 'steelblue',
        'J2': 'gray',
        'J4': 'lightcoral',
        'N1': 'olive',
        'N2': 'teal',
        'S1': 'tan',
        'S2': 'indigo',
        'T1': 'yellow',
        'T2': 'orangered',
        'V1': 'darkorchid',
        'V2': 'tomato',
        'Q':  'thistle',
        'A':  'cadetblue',
        '0':  'gray'}

    piece_width = 3                     # for format_solution

    def customize_piece_data(self):
        """
        Combine piece data from Pentominoes with `self.non_planar_piece_data`.
        Subclasses should extend this method, not override.
        """
        self.piece_data = {}
        for name, (data, kwargs) in SolidPentominoes.piece_data.items():
            self.piece_data[name] = (tuple((x, y, 0) for (x, y) in data), {})
        self.piece_data.update(copy.deepcopy(self.non_planar_piece_data))
        self.piece_colors = copy.deepcopy(self.piece_colors)
        self.piece_colors.update(SolidPentominoes.piece_colors)


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
                        yield coordsys.Cartesian3D((x, y, z))

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
                        yield coordsys.Cartesian3D((x, y, z))

    transform_solution_matrix = Puzzle3D.swap_yz_transform


class Pentacubes2x11x11Frame(Pentacubes):

    """ solutions"""

    width = 11
    height = 11
    depth = 2

    def coordinates(self):
        for y in range(self.height):
            for x in range(self.width):
                yield coordsys.Cartesian3D((x, y, 0))
        for y in range(2, self.height - 2):
            for x in range(2, self.width - 2):
                if ( x == 2 or x == self.width - 3
                     or y == 2 or y == self.height - 3):
                    yield coordsys.Cartesian3D((x, y, 1))

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
                    yield coordsys.Cartesian3D((x, y, z))


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
                        yield coordsys.Cartesian3D((x, y, z))


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
                    yield coordsys.Cartesian3D((x, y, z))


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
                        yield coordsys.Cartesian3D((x, y, z))

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
                        yield coordsys.Cartesian3D((x, y, z))

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
                            yield coordsys.Cartesian3D((x, y, z))
                    elif 11 < x + y < 15:
                        yield coordsys.Cartesian3D((x, y, z))

    transform_solution_matrix = Puzzle3D.swap_yz_transform


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
                        yield coordsys.Cartesian3D((x, y, z))
        yield coordsys.Cartesian3D((1, 19, 1))


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
                        yield coordsys.Cartesian3D((x, y, z))
        yield coordsys.Cartesian3D((1, 19, 1))


class Pentacubes3x3x17Tower(Pentacubes):

    """ solutions"""

    width = 3
    height = 17
    depth = 3

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height - 1):
                for x in range(self.width):
                    yield coordsys.Cartesian3D((x, y, z))
        yield coordsys.Cartesian3D((1, 16, 1))


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
                        yield coordsys.Cartesian3D((x, y, z))
        yield coordsys.Cartesian3D((0, 18, 0))


class Pentacubes5x9x9Fortress(Pentacubes):

    """ solutions"""

    width = 9
    height = 9
    depth = 5

    def coordinates(self):
        for y in range(self.height):
            for x in range(self.width):
                yield coordsys.Cartesian3D((x, y, 0))
        for z in range(1, self.depth):
            for i in range(self.height):
                if z <= abs(i - 4):
                    yield coordsys.Cartesian3D((0, i, z))
                    yield coordsys.Cartesian3D((8, i, z))
                    if 0 < i < self.width - 1:
                        yield coordsys.Cartesian3D((i, 0, z))
                        yield coordsys.Cartesian3D((i, 8, z))

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
                        yield coordsys.Cartesian3D((x, y, z))


class PentacubesPlus(Pentacubes):

    """
    Also known as 'Super Deluxe Quintillions', these are the pentacubes with a
    second L3 piece (a.k.a. J3), allowing the construction of box shapes.  See
    http://www.gamepuzzles.com/polycube.htm#SQd.
    """

    def customize_piece_data(self):
        """Add J3, a copy of L3."""
        Pentacubes.customize_piece_data(self)
        self.piece_data['J3'] = copy.deepcopy(self.piece_data['L3'])
        self.piece_colors['J3'] = self.piece_colors['L3']

    def format_solution(self, solution,
                        x_reversed=False, y_reversed=False, z_reversed=False):
        """
        Consider J3 and L3 as the same piece for solution counting purposes.
        """
        solution = Pentacubes.format_solution(
            self, solution, x_reversed=x_reversed, y_reversed=y_reversed,
            z_reversed=z_reversed)
        return solution.replace('J3', 'L3')


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

    piece_colors = {
        'V': 'blue',
        'p': 'red',
        'T': 'green',
        'Z': 'lime',
        'L': 'blueviolet',
        'a': 'gold',
        'b': 'navy',
        '0': 'gray'}

    check_for_duplicates = False

    def format_solution(self, solution,
                        x_reversed=False, y_reversed=False, z_reversed=False,
                        xy_swapped=False, xz_swapped=False, yz_swapped=False):
        order_functions = (lambda x: x, reversed)
        x_reversed_fn = order_functions[x_reversed]
        y_reversed_fn = order_functions[1 - y_reversed] # reversed by default
        z_reversed_fn = order_functions[z_reversed]
        s_matrix = self.empty_solution_matrix()
        for row in solution:
            name = row[-1]
            for cell_name in row[:-1]:
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


class Soma3x3x3(SomaCubes):

    """
    240 solutions
    symmetry: T fixed (at edge, in XY plane, leg at right);
    restrict p to 4 aspects (one leg down)
    """

    height = 3
    width = 3
    depth = 3

    def customize_piece_data(self):
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


class SomaCrystal(SomaCubes):

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

    def transform_solution_matrix(self, s_matrix):
        return [[[s_matrix[z][y][x]
                  for y in range(self.height)]
                 for z in range(self.depth - 1, -1, -1)]
                for x in range(self.width)]

class SomaLongWall(SomaCubes):

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

    transform_solution_matrix = Puzzle3D.cycle_xyz_transform


class SomaHighWall(SomaCubes):

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

    transform_solution_matrix = Puzzle3D.cycle_xyz_transform


class SomaBench(SomaCubes):

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


class SomaSteps(SomaCubes):

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

    transform_solution_matrix = Puzzle3D.swap_yz_transform


class SomaBathtub(SomaCubes):

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


class SomaCurvedWall(SomaCubes):

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

    def transform_solution_matrix(self, s_matrix):
        return [[[s_matrix[z][y][x] for x in range(self.width)]
                 for z in range(self.depth)]
                for y in range(self.height - 1, -1, -1)]


class SomaSquareWall(SomaCubes):

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


class SomaSofa(SomaCubes):

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


class SomaCornerstone(SomaCubes):

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


class Soma_W(SomaCubes):

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


class SomaSkew1(SomaCubes):

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

    transform_solution_matrix = Puzzle3D.swap_yz_transform


class SomaSkew2(SomaCubes):

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

    transform_solution_matrix = Puzzle3D.swap_yz_transform


class SomaSteamer(SomaCubes):

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

    transform_solution_matrix = Puzzle3D.cycle_xyz_transform


class Polysticks(Puzzle):

    def coordinates(self):
        # coordinates not yet used (or generated) by polystick puzzles
        return []

    def make_aspects(self, segments, flips=(0, 1), rotations=(0, 1, 2, 3)):
        aspects = set()
        polystick = coordsys.CartesianPath2D(segments)
        for flip in flips or (0,):
            for rotation in rotations or (0,):
                aspect = polystick.oriented(rotation, flip, normalized=True)
                aspects.add(aspect)
        return aspects

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
        h_matrix, v_matrix, omitted, prefix = self.build_solution_matrices(
            solution, xy_swapped, rotation)
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
        return prefix + '\n'.join(y_reversed_fn(lines))

    def build_solution_matrices(self, solution,
                                xy_swapped=False, rotation=False, margin=0):
        h_matrix = [[' '] * (self.width + 2 * margin)
                    for y in range(self.height + 2 * margin + 1)]
        v_matrix = [[' '] * (self.width + 2 * margin + 1)
                    for y in range(self.height + 2 * margin)]
        matrices = {'h': h_matrix, 'v': v_matrix}
        omitted = []
        prefix = []
        for row in solution:
            name = row[-1]
            if row[0] == '!':
                omitted.append(name)
                prefix.append('(%s omitted)\n' % name)
                continue
            for segment_coords in row[:-1]:
                direction = segment_coords[-1]
                if direction == 'i':
                    continue
                x, y = (int(d.strip()) for d in segment_coords[:-1].split(','))
                x, y, direction = self.rotate_segment(x, y, direction, rotation)
                if xy_swapped:
                    x, y = y, x
                    direction = 'hv'[direction == 'h']
                matrices[direction][y + margin][x + margin] = name
        return h_matrix, v_matrix, omitted, '\n'.join(prefix)

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


class Tetrasticks(Polysticks):

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
    """Coordinate pairs are end-points of line segments."""

    symmetric_pieces = 'I O T U V W X'.split()
    """Pieces with reflexive symmetry, identical to their mirror images."""

    asymmetric_pieces = 'F H J L N P R Y Z'.split()
    """Pieces without reflexive symmetry, different from their mirror images."""

    welded_pieces = 'F H R T X Y'.split()
    """Pieces with junction points (where 3 or more segments join)."""

    unwelded_pieces = 'I J L N O P U V W Z '.split()
    """Pieces without junction points (max. 2 segments join)."""


class Polysticks123Data(object):

    piece_data = {
        'I1': ((((0,0),(1,0)),), {}),
        'I2': ((((0,0),(2,0)),), {}),
        'V2': ((((0,0),(1,0)), ((0,0),(0,1))), {}),
        'I3': ((((0,0),(3,0)),), {}),
        'L3': ((((0,0),(2,0)), ((2,0),(2,1))), {}),
        'T3': ((((0,0),(2,0)), ((1,0),(1,1))), {}),
        'Z3': ((((0,1),(1,1)), ((1,1),(1,0)), ((1,0),(2,0))), {}),
        'U3': ((((0,1),(0,0)), ((0,0),(1,0)), ((1,0),(1,1))), {}),}


class WeldedTetrasticks4x4(Tetrasticks):

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
        for key in self.unwelded_pieces:
            del self.piece_data[key]
        for key in self.asymmetric_pieces:
            if key not in self.piece_data:
                continue
            self.piece_data[key][-1]['flips'] = None
            self.piece_data[key+'*'] = copy.deepcopy(self.piece_data[key])
            self.piece_data[key+'*'][-1]['flips'] = (1,)


class Tetrasticks5x5(Tetrasticks):

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
            return Tetrasticks.make_aspects(
                self, segments, flips=flips, rotations=rotations)
        return set()


class Polysticks1234(Tetrasticks, Polysticks123Data):

    piece_data = copy.deepcopy(Tetrasticks.piece_data)
    piece_data.update(copy.deepcopy(Polysticks123Data.piece_data))


class Polysticks1234_6x6(Polysticks1234):

    """
    ? solutions (very large number; over 35000 unique solutions in first
    position of X, I, & I1)
    (perfect solutions, i.e. no pieces cross).
    """

    width = 6
    height = 6

    @classmethod
    def components(cls):
        return (Polysticks1234_6x6A,
                Polysticks1234_6x6B,
                Polysticks1234_6x6C,
                Polysticks1234_6x6D)


class Polysticks1234_6x6A(Polysticks1234_6x6):

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


class Polysticks1234_6x6B(Polysticks1234_6x6):

    def build_matrix(self):
        keys = sorted(self.pieces.keys())
        x_coords, x_aspect = self.pieces['X'][0]
        translated = x_aspect.translate((0, 1))
        self.build_matrix_row('X', translated)
        keys.remove('X')
        self.build_regular_matrix(keys)


class Polysticks1234_6x6C(Polysticks1234_6x6):

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


class Polysticks1234_6x6D(Polysticks1234_6x6):

    """symmetry: X at center; remove flip & rotation of P (fix one aspect)"""

    def customize_piece_data(self):
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

    duplicate_conditions = ()

    svg_unit_height = Puzzle3D.svg_unit_length * math.sqrt(3) / 2

    coord_class = coordsys.Hexagonal2D

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
        s_matrix = self.build_solution_matrix(solution)
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

    def format_coords(self):
        s_matrix = self.empty_solution_matrix()
        for x, y in self.solution_coords:
            s_matrix[y][x] = '* '
        return self.format_hex_grid(s_matrix)

    def format_svg(self, solution=None, s_matrix=None):
        if s_matrix:
            assert solution is None, ('Provide only one of solution '
                                      '& s_matrix arguments, not both.')
        else:
            s_matrix = self.build_solution_matrix(solution, margin=1)
        polygons = []
        for y in range(1, self.height + 1):
            for x in range(1, self.width + 1):
                if s_matrix[y][x] == self.empty_cell:
                    continue
                polygons.append(self.build_polygon(s_matrix, x, y))
        header = self.svg_header % {
            'height': (self.height + 2) * self.svg_unit_height,
            'width': (self.width + self.height / 2.0 + 2) * self.svg_unit_width}
        return '%s%s%s%s%s' % (header, self.svg_g_start, ''.join(polygons),
                               self.svg_g_end, self.svg_footer)

    edge_trace = {0: ( 0, -1),
                  1: (+1, -1),
                  2: (+1,  0),
                  3: ( 0, +1),
                  4: (-1, +1),
                  5: (-1,  0)}
    """Mapping of counterclockwise edges to examination cell coordinate
    delta."""

    _sqrt3 = math.sqrt(3)
    corner_offsets = {0: (0.0, 1 / _sqrt3),
                      1: (0.0, 0.0),
                      2: (0.5, -_sqrt3 / 6),
                      3: (1.0, 0.0),
                      4: (1.0, 1 / _sqrt3),
                      5: (0.5, _sqrt3 / 2)}
    """Offset of corners from the lower left-hand corner of hexagon."""

    def get_polygon_points(self, s_matrix, x, y):
        """
        Return a list of coordinate tuples, the corner points of the polygon
        for the piece at (x,y).
        """
        cell_content = s_matrix[y][x]
        unit = self.svg_unit_length
        yunit = self.svg_unit_height
        height = (self.height + 2) * yunit
        base_x = (x + (y - 1) / 2.0) * unit
        base_y = height - y * yunit
        # the first 2 edges (3 corners) are known:
        points = [(base_x + self.corner_offsets[corner][0] * unit,
                   base_y - self.corner_offsets[corner][1] * unit)
                  for corner in range(3)]
        corner = 2                   # right & up
        start = (x, y, 0)
        while (x, y, corner) != start:
            delta = self.edge_trace[corner]
            points.append((base_x + self.corner_offsets[corner][0] * unit,
                           base_y - self.corner_offsets[corner][1] * unit))
            if ( cell_content != '0'
                 and s_matrix[y + delta[1]][x + delta[0]] == cell_content):
                corner = (corner - 1) % 6
                x += delta[0]
                y += delta[1]
                base_x = (x + (y - 1) / 2.0) * unit
                base_y = height - y * yunit
            else:
                corner = (corner + 1) % 6
        return points


class Polyhexes123Data(object):

    piece_data = {
        'H1': ((), {}),
        'I2': ((( 1, 0),), {}),
        'I3': ((( 1, 0), ( 2, 0)), {}),
        'V3': ((( 1, 0), ( 1, 1)), {}),
        'A3': ((( 1, 0), ( 0, 1)), {}),}
    """(0,0) is implied."""

    symmetric_pieces = piece_data.keys() # all of them

    asymmetric_pieces = []

    piece_colors = {
        'H1': 'gray',
        'I2': 'steelblue',
        'I3': 'teal',
        'V3': 'plum',
        'A3': 'olive',
        '0': 'gray'}


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

    asymmetric_pieces = 'J4 P4 S4'.split()
    """Pieces without reflexive symmetry, different from their mirror images."""

    piece_colors = {
        'I4': 'blue',
        'O4': 'red',
        'Y4': 'green',
        'U4': 'lime',
        'J4': 'blueviolet',
        'P4': 'gold',
        'S4': 'navy',
        '0': 'gray'}


class Polyhex1234(Polyhexes123Data, Tetrahexes):

    symmetric_pieces = (Polyhexes123Data.symmetric_pieces
                        + Tetrahexes.symmetric_pieces)

    asymmetric_pieces = (Polyhexes123Data.asymmetric_pieces
                         + Tetrahexes.asymmetric_pieces)

    def customize_piece_data(self):
        self.piece_data = copy.deepcopy(Tetrahexes.piece_data)
        self.piece_data.update(copy.deepcopy(Polyhexes123.piece_data))
        self.piece_colors = copy.deepcopy(Tetrahexes.piece_colors)
        self.piece_colors.update(Polyhexes123.piece_colors)


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

    piece_colors = {
        'I5': 'blue',
        'X5': 'red',
        'D5': 'green',
        'C5': 'lime',
        'V5': 'blueviolet',
        'W5': 'gold',
        'U5': 'navy',
        'E5': 'magenta',
        'L5': 'darkorange',
        'Y5': 'turquoise',
        'A5': 'maroon',
        'J5': 'darkseagreen',
        'P5': 'peru',
        'N5': 'plum',
        'r5': 'yellow',
        'p5': 'steelblue',
        'S5': 'gray',
        'u5': 'lightcoral',
        'q5': 'olive',
        'T5': 'teal',
        'y5': 'tan',
        'G5': 'indigo',
        '0': 'gray'}


class Tetrahex4x7(Tetrahexes):

    """9 solutions"""

    height = 4
    width = 7

    duplicate_conditions = ({'rotate_180': True},)


class Tetrahex7x7Triangle(Tetrahexes):

    """0 solutions"""

    height = 7
    width = 7

    def coordinates(self):
        for y in range(self.height):
            for x in range(self.width):
                if x + y < self.height:
                    yield coordsys.Hexagonal2D((x, y))


class Tetrahex3x10Clipped(Tetrahexes):

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


class TetrahexCoin(Tetrahexes):

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


class Pentahex10x11(Pentahexes):

    """? (many) solutions"""

    height = 10
    width = 11

    duplicate_conditions = ({'rotate_180': True},)


class Pentahex5x22(Pentahexes):

    """? (many) solutions"""

    height = 5
    width = 22

    duplicate_conditions = ({'rotate_180': True},)


class Pentahex15x11Trapezium(Pentahexes):

    height = 11
    width = 15

    def coordinates(self):
        for y in range(self.height):
            for x in range(self.width):
                if x + y < self.width:
                    yield coordsys.Hexagonal2D((x, y))


class Pentahex5x24Trapezium(Pentahex15x11Trapezium):

    height = 5
    width = 24


class PentahexHexagon1(Pentahexes):

    """ solutions"""

    height = 13
    width = 13

    duplicate_conditions = ({'rotate_180': True},)

    def coordinates(self):
        hole = set()
        for y in range(4, 9):
            for x in range(4, 9):
                if 9 < x + y < 15:
                    hole.add((x,y))
        hole.remove((8,6))
        hole.remove((4,6))
        for y in range(self.height):
            for x in range(self.width):
                if 5 < x + y < 19 and (x,y) not in hole:
                    yield coordsys.Hexagonal2D((x, y))


class PentahexHexagon2(Pentahexes):

    """ solutions"""

    height = 13
    width = 13

    duplicate_conditions = ({'rotate_180': True},)

    def coordinates(self):
        hole = set()
        for y in range(4, 9):
            for x in range(4, 9):
                if 9 < x + y < 15:
                    hole.add((x,y))
        hole.remove((7,4))
        hole.remove((5,8))
        for y in range(self.height):
            for x in range(self.width):
                if 5 < x + y < 19 and (x,y) not in hole:
                    yield coordsys.Hexagonal2D((x, y))


class PentahexHexagon3(Pentahexes):

    """ solutions"""

    height = 15
    width = 15

    duplicate_conditions = ({'rotate_180': True},)

    def coordinates(self):
        hole = set()
        for y in range(3, 12):
            for x in range(3, 12):
                if 9 < x + y < 19:
                    hole.add((x,y))
        hole.remove((11,7))
        hole.remove((3,7))
        for y in range(self.height):
            for x in range(self.width):
                if 6 < x + y < 22 and (x,y) not in hole:
                    yield coordsys.Hexagonal2D((x, y))


class PentahexHexagon4(Pentahexes):

    """ solutions"""

    height = 15
    width = 15

    duplicate_conditions = ({'rotate_180': True},)

    def coordinates(self):
        hole = set()
        for y in range(3, 12):
            for x in range(3, 12):
                if 9 < x + y < 19:
                    hole.add((x,y))
        hole.remove((5,11))
        hole.remove((9,3))
        for y in range(self.height):
            for x in range(self.width):
                if 6 < x + y < 22 and (x,y) not in hole:
                    yield coordsys.Hexagonal2D((x, y))


class PentahexTriangle1(Pentahexes):

    height = 15
    width = 15

    def coordinates(self):
        hole = set()
        for y in range(3, 7):
            for x in range(4, 8):
                if x + y < 11:
                    hole.add((x,y))
        for y in range(self.height):
            for x in range(self.width):
                if x + y < self.width and (x,y) not in hole:
                    yield coordsys.Hexagonal2D((x, y))


class PentahexTriangle2(Pentahexes):

    height = 15
    width = 15

    def coordinates(self):
        hole = set()
        for y in range(5, 9):
            for x in range(3, 7):
                if x + y < 12:
                    hole.add((x,y))
        for y in range(self.height):
            for x in range(self.width):
                if x + y < self.width and (x,y) not in hole:
                    yield coordsys.Hexagonal2D((x, y))


class PentahexTriangle3(Pentahexes):

    height = 15
    width = 15

    def coordinates(self):
        hole = set()
        for y in range(7, 11):
            for x in range(2, 6):
                if x + y < 13:
                    hole.add((x,y))
        for y in range(self.height):
            for x in range(self.width):
                if x + y < self.width and (x,y) not in hole:
                    yield coordsys.Hexagonal2D((x, y))


class PentahexTriangle4(Pentahexes):

    height = 15
    width = 15

    def coordinates(self):
        hole = set()
        for y in range(9, 13):
            for x in range(1, 5):
                if x + y < 14:
                    hole.add((x,y))
        for y in range(self.height):
            for x in range(self.width):
                if x + y < self.width and (x,y) not in hole:
                    yield coordsys.Hexagonal2D((x, y))


class PentahexTriangle5(Pentahexes):

    height = 15
    width = 15

    def coordinates(self):
        hole = set()
        for y in range(1, 5):
            for x in range(5, 9):
                if x + y < 10:
                    hole.add((x,y))
        for y in range(self.height):
            for x in range(self.width):
                if x + y < self.width and (x,y) not in hole:
                    yield coordsys.Hexagonal2D((x, y))


class PentahexTriangle6(Pentahexes):

    height = 15
    width = 15

    def coordinates(self):
        hole = set()
        for y in range(4, 7):
            for x in range(3, 7):
                if 7 < x + y < 12:
                    hole.add((x,y))
        for y in range(self.height):
            for x in range(self.width):
                if x + y < self.width and (x,y) not in hole:
                    yield coordsys.Hexagonal2D((x, y))


class PentahexHexagram1(Pentahexes):

    height = 17
    width = 17

    def coordinates(self):
        hole = self.hole_coordinates()
        coords = set()
        for y in range(4, 17):
            for x in range(4, 17):
                if x + y < 21 and (x,y) not in hole:
                    yield coordsys.Hexagonal2D((x, y))
                    coords.add((x,y))
        for y in range(13):
            for x in range(13):
                if x + y > 11 and (x,y) not in hole and (x,y) not in coords:
                    yield coordsys.Hexagonal2D((x, y))

    def hole_coordinates(self):
        return set(((7,7), (8,7), (9,7), (10,7),
                    (7,8), (8,8), (9,8),
                    (6,9), (7,9), (8,9), (9,9)))


class PentahexHexagram2(PentahexHexagram1):

    def hole_coordinates(self):
        return set(((8,6), (10,6),
                    (8,7), (9,7),
                    (7,8), (8,8), (9,8),
                    (7,9), (8,9),
                    (6,10), (8,10)))


class PentahexHexagram3(PentahexHexagram1):

    def hole_coordinates(self):
        return set(((9,6),
                    (8,7), (9,7),
                    (6,8), (7,8), (8,8), (9,8), (10,8),
                    (7,9), (8,9),
                    (7,10)))


class PentahexHexagram4(PentahexHexagram1):

    def hole_coordinates(self):
        return set(((8,6), (9,6), (10,6),
                    (8,7), (9,7),
                    (8,8),
                    (7,9), (8,9),
                    (6,10), (7,10), (8,10)))


class PentahexHexagram5(PentahexHexagram1):

    def hole_coordinates(self):
        return set(((9,6),
                    (7,7), (8,7), (9,7), (10,7),
                    (8,8),
                    (6,9), (7,9), (8,9), (9,9),
                    (7,10)))


class PentahexHexagram6(PentahexHexagram1):

    def hole_coordinates(self):
        return set(((8,7), (9,7),
                    (5,8), (6,8), (7,8), (8,8), (9,8), (10,8), (11,8),
                    (7,9), (8,9)))


class PentahexHexagram7(PentahexHexagram1):

    def hole_coordinates(self):
        return set(((9,5), (10,5),
                    (9,6),
                    (8,7), (9,7),
                    (8,8),
                    (7,9), (8,9),
                    (7,10),
                    (6,11), (7,11)))


class Polyhex1234_4x10(Polyhex1234):

    """? (many) solutions"""

    height = 4
    width = 10

    duplicate_conditions = ({'rotate_180': True},)


class Polyhex1234_5x8(Polyhex1234):

    """? (many) solutions"""

    height = 5
    width = 8

    duplicate_conditions = ({'rotate_180': True},)


class Polyiamonds(PuzzlePseudo3D):

    """
    Polyiamonds use a pseudo-3D coordinate system: 2D + orientation.

    The shape of the matrix is defined by the `coordinates` generator method.
    The `width` and `height` attributes define the maximum bounds only.
    """

    margin = 1

    # triangle orientation (up=0, down=1):
    depth = 2

    check_for_duplicates = True

    # override Puzzle3D's 0.5px strokes:
    svg_stroke_width = Puzzle.svg_stroke_width

    svg_unit_height = Puzzle3D.svg_unit_length * math.sqrt(3) / 2

    # stroke-linejoin="round" to avoid long miters on acute angles:
    svg_polygon = '''\
<polygon fill="%(color)s" stroke="%(stroke)s"
         stroke-width="%(stroke_width)s" stroke-linejoin="round"
         points="%(points)s">
<desc>%(name)s</desc>
</polygon>
'''

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
        s_matrix = self.build_solution_matrix(solution)
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

    def format_coords(self):
        s_matrix = self.empty_solution_matrix()
        for x, y, z in self.solution_coords:
            s_matrix[z][y][x] = '* '
        return self.format_triangular_grid(s_matrix)

    def format_piece(self, name):
        coords, aspect = self.pieces[name][0]
        s_matrix = [[[self.empty_cell] * (aspect.bounds[0] + 1)
                     for y in range(aspect.bounds[1] + 1)]
                    for z in range(aspect.bounds[2] + 1)]
        for x, y, z in coords:
            s_matrix[z][y][x] = '* '
        return self.format_triangular_grid(s_matrix)

    empty_cell = '  '

    def empty_content(self, cell, x, y, z):
        return self.empty_cell

    def cell_content(self, cell, x, y, z):
        return cell

    def format_triangular_grid(self, s_matrix, content=None, large=False):
        if large and content is None:
            content = self.empty_content
        width = len(s_matrix[0][0])
        height = len(s_matrix[0])
        top = [' ' * (2 + large) * height]
        left_margin = len(top[0])
        for x in range(width):
            bottom = '_ '[s_matrix[1][-1][x] == self.empty_cell]
            top.append(bottom * 2 * (2 + large))
        output = [''.join(top).rstrip()]
        for y in range(height - 1, -1, -1):
            padding = ' ' * (2 + large) * y
            lines = [[' ' * (1 + large) + padding],
                     [padding]]
            if large:
                lines.insert(1, [' ' + padding])
            for x in range(width):
                cell = s_matrix[0][y][x]
                left = bottom = ' '
                if ( x == 0 and cell != self.empty_cell
                     or x > 0 and s_matrix[1][y][x - 1] != cell):
                    left = '/'
                if ( y == 0 and cell != self.empty_cell
                     or y > 0 and s_matrix[1][y - 1][x] != cell):
                    bottom = '_'
                lines[0].append(left)
                if large:
                    lines[1].append(left + content(cell, x, y, 0))
                lines[-1].append((bottom, left)[left != ' ']
                                 + bottom * 2 * (1 + large))
                cell = s_matrix[1][y][x]
                left = ' '
                if s_matrix[0][y][x] != cell:
                    left = '\\'
                lines[0].append(left + ' ' * (2 + 2 * large))
                if large:
                    lines[1].append(left + content(cell, x, y, 1))
                lines[-1].append((bottom, left)[left != ' '])
            right = '/ '[cell == self.empty_cell]
            for line in lines:
                line = (''.join(line) + right).rstrip()
                output.append(line)
                left_margin = min(left_margin, len(line) - len(line.lstrip()))
        return '\n'.join(line[left_margin:] for line in output) + '\n'

    def format_svg(self, solution=None, s_matrix=None):
        if s_matrix:
            assert solution is None, ('Provide only one of solution '
                                      '& s_matrix arguments, not both.')
        else:
            s_matrix = self.build_solution_matrix(solution, margin=1)
        polygons = []
        for y in range(1, self.height + 1):
            for x in range(1, self.width + 1):
                for z in range(self.depth):
                    if s_matrix[z][y][x] == self.empty_cell:
                        continue
                    polygons.append(self.build_polygon(s_matrix, x, y, z))
        header = self.svg_header % {
            'height': (self.height + 2) * self.svg_unit_height,
            'width': (self.width + self.height / 2.0 + 2) * self.svg_unit_width}
        return '%s%s%s%s%s' % (header, self.svg_g_start, ''.join(polygons),
                               self.svg_g_end, self.svg_footer)

    def build_polygon(self, s_matrix, x, y, z):
        points = self.get_polygon_points(s_matrix, x, y, z)
        name = s_matrix[z][y][x]
        color = self.piece_colors[name]
        # Erase cells of this piece:
        for x, y, z in self.get_piece_cells(s_matrix, x, y, z):
            s_matrix[z][y][x] = self.empty_cell
        points_str = ' '.join('%.3f,%.3f' % (x, y) for (x, y) in points)
        return self.svg_polygon % {'color': color,
                                   'stroke': self.svg_stroke,
                                   'stroke_width': self.svg_stroke_width,
                                   'points': points_str,
                                   'name': name}

    edge_trace = {(+1,  0): ((( 0, -1, 0), ( 0, -1)), # right
                             (( 0, -1, 1), (+1, -1)),
                             (( 0,  0, 0), (+1,  0)),
                             ((-1,  0, 1), ( 0, +1)),
                             (None,        (-1, +1))),
                  ( 0, +1): ((( 0, -1, 1), (+1, -1)), # up & right
                             (( 0,  0, 0), (+1,  0)),
                             ((-1,  0, 1), ( 0, +1)),
                             ((-1,  0, 0), (-1, +1)),
                             (None,        (-1,  0))),
                  (-1, +1): ((( 0,  0, 0), (+1,  0)), # up & left
                             ((-1,  0, 1), ( 0, +1)),
                             ((-1,  0, 0), (-1, +1)),
                             ((-1, -1, 1), (-1,  0)),
                             (None,        ( 0, -1))),
                  (-1,  0): (((-1,  0, 1), ( 0, +1)), # left
                             ((-1,  0, 0), (-1, +1)),
                             ((-1, -1, 1), (-1,  0)),
                             (( 0, -1, 0), ( 0, -1)),
                             (None,        (+1, -1))),
                  ( 0, -1): (((-1,  0, 0), (-1, +1)), # down & left
                             ((-1, -1, 1), (-1,  0)),
                             (( 0, -1, 0), ( 0, -1)),
                             (( 0, -1, 1), (+1, -1)),
                             (None,        (+1,  0))),
                  (+1, -1): (((-1, -1, 1), (-1,  0)), # down & right
                             (( 0, -1, 0), ( 0, -1)),
                             (( 0, -1, 1), (+1, -1)),
                             (( 0,  0, 0), (+1,  0)),
                             (None,        ( 0, +1)))}
    """Mapping of counterclockwise (x,y)-direction vector to list (ordered by
    test) of 2-tuples: examination cell coordinate delta & new direction
    vector."""

    def get_polygon_points(self, s_matrix, x, y, z):
        """
        Return a list of coordinate tuples, the corner points of the polygon
        for the piece at (x,y).
        """
        cell_content = s_matrix[z][y][x]
        xunit = self.svg_unit_width
        yunit = self.svg_unit_height
        height = (self.height + 2) * yunit
        if z == 0:
            direction = (+1, 0)         # to the right
        else:
            direction = (+1, -1)        # down & to the right
            y += 1                      # begin at top-left corner
        points = [((x + (y - 1) / 2.0) * xunit, height - y * yunit)]
        start = (x, y)
        x += direction[0]
        y += direction[1]
        while (x, y) != start:
            for delta, new_direction in self.edge_trace[direction]:
                if ( delta is None
                     or cell_content != '0'
                     and (s_matrix[delta[2]][y + delta[1]][x + delta[0]]
                          == cell_content)):
                    break
            if new_direction != direction:
                direction = new_direction
                points.append(((x + (y - 1) / 2.0) * xunit, height - y * yunit))
            x += direction[0]
            y += direction[1]
        return points

    def get_piece_cells(self, s_matrix, x, y, z):
        cell_content = s_matrix[z][y][x]
        coord = coordsys.Triangular3D((x, y, z))
        cells = set([coord])
        if cell_content != '0':
            self._get_piece_cells(cells, coord, s_matrix, cell_content)
        return cells

    def _get_piece_cells(self, cells, coord, s_matrix, cell_content):
        for neighbor in coord.neighbors():
            x, y, z = neighbor
            if neighbor not in cells and s_matrix[z][y][x] == cell_content:
                cells.add(neighbor)
                self._get_piece_cells(cells, neighbor, s_matrix, cell_content)

    def convert_record_to_solution_matrix(self, record):
        s_matrix = self.empty_solution_matrix(self.margin)
        for row in record:
            parts = row.split()
            name = parts[-1]
            for coords in parts[:-1]:
                x, y, z = (int(coord) for coord in coords.split(','))
                s_matrix[z][y + self.margin][x + self.margin] = name
        return s_matrix


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
               {}),}                    # Hexagon
    """(0,0,0) is implied."""

    symmetric_pieces = 'E6 V6 X6 L6 O6'.split()
    """Pieces with reflexive symmetry, identical to their mirror images."""

    asymmetric_pieces = 'I6 P6 J6 H6 S6 G6 F6'.split()
    """Pieces without reflexive symmetry, different from their mirror images."""

    piece_colors = {
        'I6': 'blue',
        'X6': 'red',
        'O6': 'green',
        'V6': 'gold',
        'J6': 'lime',
        'S6': 'navy',
        'P6': 'magenta',
        'E6': 'darkorange',
        'H6': 'turquoise',
        'C6': 'blueviolet',
        'G6': 'maroon',
        'F6': 'plum',
        '0': 'gray'}


class Hexiamonds4x9(Hexiamonds):

    """74 solutions"""

    height = 4
    width = 9

    duplicate_conditions = ({'rotate_180': True},)


class Hexiamonds6x6(Hexiamonds):

    """156 solutions"""

    height = 6
    width = 6

    duplicate_conditions = ({'rotate_180': True},
                            {'xy_swapped': True},
                            {'rotate_180': True, 'xy_swapped': True},)


class Hexiamonds4x11Trapezium(Hexiamonds):

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
        self.piece_data['I6'][-1]['flips'] = None


class Hexiamonds6x9Trapezium(Hexiamonds4x11Trapezium):

    """0 solutions (impossible due to parity)"""

    height = 6
    width = 9


class Hexiamonds4x10LongHexagon(Hexiamonds):

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
        self.piece_data['I6'][-1]['flips'] = None


class HexiamondsSnowflake(Hexiamonds):

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
        self.piece_data['J6'][-1]['rotations'] = None


class HexiamondsRing(Hexiamonds):

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


class HexiamondsRing2(Hexiamonds):

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
                        yield coordsys.Triangular3D((x, y, z))


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
                        yield coordsys.Triangular3D((x, y, z))


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
                        yield coordsys.Triangular3D((x, y, z))


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
                        yield coordsys.Triangular3D((x, y, z))


class HexiamondsCrescent(Hexiamonds):

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
        self.piece_data['I6'][-1]['flips'] = None


class HexiamondsCrescent2(Hexiamonds):

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
        self.piece_data['I6'][-1]['flips'] = None


class HexiamondsTrefoil(Hexiamonds):

    """640 solutions"""

    height = 8
    width = 8

    check_for_duplicates = False

    def coordinates(self):
        for z in range(self.depth):
            for y in range(2, 6):
                for x in range(4):
                    if 3 < x + y + z <= 7:
                        yield coordsys.Triangular3D((x, y, z))
            for y in range(4):
                for x in range(4, 8):
                    if 5 < x + y + z <= 9:
                        yield coordsys.Triangular3D((x, y, z))
            for y in range(4, 8):
                for x in range(2, 6):
                    if 7 < x + y + z <= 11:
                        yield coordsys.Triangular3D((x, y, z))

    def customize_piece_data(self):
        self.piece_data['I6'][-1]['rotations'] = None
        self.piece_data['I6'][-1]['flips'] = None


class Hexiamonds3Hexagons(Hexiamonds):

    """0 solutions"""

    height = 4
    width = 12

    check_for_duplicates = False

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(4):
                    if 1 < x + y + z <= 5:
                        yield coordsys.Triangular3D((x, y, z))
                for x in range(4, 8):
                    if 5 < x + y + z <= 9:
                        yield coordsys.Triangular3D((x, y, z))
                for x in range(8, 12):
                    if 9 < x + y + z <= 13:
                        yield coordsys.Triangular3D((x, y, z))


class HexiamondsCoin(Hexiamonds):

    """304 solutions"""

    height = 6
    width = 8

    duplicate_conditions = ({'rotate_180': True},)

    def coordinates(self):
        hole = set(((3,2,1), (3,3,0), (3,3,1), (4,2,0), (4,2,1), (4,3,0)))
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if ( 2 < x + y + z <= 10
                         and not (x, y, z) in hole):
                        yield coordsys.Triangular3D((x, y, z))

    def customize_piece_data(self):
        self.piece_data['I6'][-1]['flips'] = None


class Heptiamonds(Polyiamonds):

    piece_data = {
        'I7': ((( 0, 0, 1), ( 1, 0, 0), ( 1, 0, 1), ( 2, 0, 0), ( 2, 0, 1),
                ( 3, 0, 0)), {}),
        'P7': ((( 0, 0, 1), ( 1, 0, 0), ( 1, 0, 1), ( 2, 0, 0), ( 2, 0, 1),
                ( 0, 1, 0)), {}),
        'E7': ((( 0, 0, 1), ( 1, 0, 0), ( 1, 0, 1), ( 2, 0, 0), ( 2, 0, 1),
                ( 1, 1, 0)), {}),
        'L7': ((( 0, 0, 1), ( 1, 0, 0), ( 1, 0, 1), ( 2, 0, 0), ( 2, 0, 1),
                ( 2, 1, 0)), {}),
        'H7': ((( 0, 0, 1), ( 1, 0, 0), ( 1, 0, 1), ( 2, 0, 0), ( 1, 1, 0),
                ( 1, 1, 1)), {}),
        'G7': ((( 0, 0, 1), ( 1, 0, 0), ( 1, 0, 1), ( 2, 0, 0), ( 1, 1, 0),
                ( 0, 1, 1)), {}),
        'M7': ((( 0, 0, 1), ( 1, 0, 0), ( 1, 0, 1), ( 2, 0, 0), ( 1, 1, 0),
                ( 0, 1, 0)), {}),
        'T7': ((( 0, 0, 1), ( 1, 0, 0), ( 1, 0, 1), ( 2, 0, 0), ( 0, 1, 0),
                ( 0,-1, 1)), {}),
        'X7': ((( 0, 0, 1), ( 1, 0, 0), ( 1, 0, 1), ( 2, 0, 0), ( 0, 1, 0),
                ( 1,-1, 1)), {}),
        'Q7': ((( 0, 0, 1), ( 1, 0, 0), ( 1, 0, 1), ( 2, 0, 0), ( 0, 1, 0),
                ( 2,-1, 1)), {}),
        'R7': ((( 0, 0, 1), ( 1, 0, 0), ( 1, 0, 1), ( 2, 0, 0), ( 0,-1, 1),
                ( 0,-1, 0)), {}),
        'J7': ((( 0, 0, 1), ( 1, 0, 0), ( 1, 0, 1), ( 2, 0, 0), ( 0,-1, 1),
                ( 1,-1, 0)), {}),
        'F7': ((( 0, 0, 1), ( 1, 0, 0), ( 1, 0, 1), ( 2, 0, 0), ( 0,-1, 1),
                ( 1,-1, 1)), {}),
        'C7': ((( 0, 0, 1), ( 1, 0, 0), ( 1, 0, 1), ( 2, 0, 0), ( 0,-1, 1),
                ( 2,-1, 1)), {}),
        'Y7': ((( 0, 0, 1), ( 1, 0, 0), ( 1, 0, 1), ( 2, 0, 0), ( 1,-1, 1),
                ( 1,-1, 0)), {}),
        'Z7': ((( 0, 0, 1), ( 1, 0, 0), ( 1, 0, 1), ( 1,-1, 1), ( 2,-1, 0),
                ( 2, -1, 1)), {}),
        'B7': ((( 0, 0, 1), ( 1, 0, 0), ( 1, 0, 1), ( 0, 1, 0), ( 0, 1, 1),
                ( 1,-1, 1)), {}),
        'A7': ((( 0, 0, 1), ( 1, 0, 0), ( 1, 0, 1), ( 0,-1, 1), ( 1,-1, 1),
                ( 2,-1, 0)), {}),
        'W7': ((( 0, 0, 1), ( 1, 0, 0), ( 1, 0, 1), ( 1,-1, 1), ( 2,-1, 0),
                ( 1, 1, 0)), {}),
        'D7': ((( 0, 0, 1), ( 1, 0, 0), ( 0,-1, 1), ( 1,-1, 0), ( 1,-1, 1),
                ( 0, 1, 0)), {}),
        'U7': ((( 0, 0, 1), ( 1, 0, 0), ( 1, 0, 1), ( 1, 1, 0), ( 1, 1, 1),
                ( 0, 1, 0)), {}),
        'V7': ((( 0, 0, 1), ( 1, 0, 0), ( 1, 0, 1), ( 1, 1, 0), ( 0, 1, 1),
                ( 0, 2, 0)), {}),
        'N7': ((( 0, 0, 1), ( 1, 0, 0), ( 1, 0, 1), ( 0,-1, 1), ( 1, 1, 0),
                ( 1, 1, 1)), {}),
        'S7': ((( 0, 0, 1), ( 1, 0, 0), ( 1, 0, 1), ( 0,-1, 1), ( 1, 1, 0),
                ( 0, 1, 1)), {}),}
    """(0,0,0) is implied."""

    symmetric_pieces = 'C7 D7 I7 M7 V7'.split()
    """Pieces with reflexive symmetry, identical to their mirror images."""

    asymmetric_pieces = (
        'A7 B7 E7 F7 G7 H7 J7 L7 N7 P7 Q7 R7 S7 T7 U7 W7 X7 Y7 Z7').split()
    """Pieces without reflexive symmetry, different from their mirror images."""

    piece_colors = {
        'I7': 'blue',
        'M7': 'red',
        'D7': 'green',
        'C7': 'lime',
        'V7': 'gold',
        'S7': 'navy',
        'P7': 'magenta',
        'E7': 'darkorange',
        'H7': 'turquoise',
        'W7': 'blueviolet',
        'G7': 'maroon',
        'F7': 'darkseagreen',
        'A7': 'peru',
        'B7': 'plum',
        'J7': 'yellowgreen',
        'L7': 'steelblue',
        'N7': 'gray',
        'Q7': 'lightcoral',
        'R7': 'olive',
        'T7': 'teal',
        'U7': 'tan',
        'X7': 'indigo',
        'Y7': 'yellow',
        'Z7': 'orangered',
        '0': 'gray'}


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
                        yield coordsys.Triangular3D((x, y, z))

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
                    coord = coordsys.Triangular3D((x, y, z))
                    if x + y + z < 20 and not coord in holes:
                        coords.add(coord)
                        yield coord
        for y in range(12):
            for x in range(12):
                for z in range(self.depth):
                    coord = coordsys.Triangular3D((x, y, z))
                    if ( x + y + z > 11 and not coord in holes
                         and coord not in coords):
                        coords.add(coord)
                        yield coordsys.Triangular3D((x, y, z))

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
                        yield coordsys.Triangular3D((x, y, z))

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
                        yield coordsys.Triangular3D((x, y, z))

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
     solutions

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
                        coord = coordsys.Triangular3D((x, y, z))
                        coords.add(coord)
                        yield coord
            for y in range(12):
                for x in range(12):
                    total = x + y + z
                    if total >= 12 and not (5 < x < 10 and 5 < y < 10
                                            and 13 < total < 18):
                        coord = coordsys.Triangular3D((x, y, z))
                        if coord not in coords:
                            coords.add(coord)
                            yield coord

    def customize_piece_data(self):
        self.piece_data['P7'][-1]['flips'] = None
        self.piece_data['P7'][-1]['rotations'] = None


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
                        hole.add(coordsys.Triangular3D((x, y, z)))
        for y in range(2, 8):
            for x in range(2, 8):
                for z in range(self.depth):
                    if x + y + z > 9:
                        hole.add(coordsys.Triangular3D((x, y, z)))
        for y in range(self.height):
            for x in range(self.width):
                for z in range(self.depth):
                    total = x + y + z
                    coord = coordsys.Triangular3D((x, y, z))
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
                        hole.add(coordsys.Triangular3D((x, y, z)))
        for y in range(6, 10):
            for x in range(3, 7):
                for z in range(self.depth):
                    if 10 < x + y + z < 15:
                        hole.add(coordsys.Triangular3D((x, y, z)))
        for y in range(self.height):
            for x in range(self.width):
                for z in range(self.depth):
                    coord = coordsys.Triangular3D((x, y, z))
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
                        hole.add(coordsys.Triangular3D((x, y, z)))
            for x in range(6, 10):
                for z in range(self.depth):
                    if 11 < x + y + z < 16:
                        hole.add(coordsys.Triangular3D((x, y, z)))
        for y in range(self.height):
            for x in range(self.width):
                for z in range(self.depth):
                    coord = coordsys.Triangular3D((x, y, z))
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
                        hole.add(coordsys.Triangular3D((x, y, z)))
            for x in range(7, 11):
                for z in range(self.depth):
                    if 12 < x + y + z < 17:
                        hole.add(coordsys.Triangular3D((x, y, z)))
        for y in range(self.height):
            for x in range(self.width):
                for z in range(self.depth):
                    coord = coordsys.Triangular3D((x, y, z))
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
                        hole.add(coordsys.Triangular3D((x, y, z)))
            for x in range(8, 12):
                for z in range(self.depth):
                    if 13 < x + y + z < 18:
                        hole.add(coordsys.Triangular3D((x, y, z)))
        for y in range(self.height):
            for x in range(self.width):
                for z in range(self.depth):
                    coord = coordsys.Triangular3D((x, y, z))
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
                        hole.add(coordsys.Triangular3D((x, y, z)))
        for coord in ((4,4,1), (7,3,0), (8,4,1), (3,7,0), (4,8,1), (7,7,0)):
            hole.remove(coord)
        for y in range(self.height):
            for x in range(self.width):
                for z in range(self.depth):
                    coord = coordsys.Triangular3D((x, y, z))
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
                        hole.add(coordsys.Triangular3D((x, y, z)))
        for coord in ((5,3,1), (6,3,0), (8,5,1), (8,6,0), (3,8,0), (3,8,1)):
            hole.remove(coord)
        for y in range(self.height):
            for x in range(self.width):
                for z in range(self.depth):
                    coord = coordsys.Triangular3D((x, y, z))
                    if 5 < x + y + z < 18 and coord not in hole:
                        yield coord

    def customize_piece_data(self):
        self.piece_data['P7'][-1]['flips'] = None


class HeptiamondsDiamondRing(Heptiamonds):

    """
     solutions

    10-unit diamond with central 4-unit diamond hole
    """

    height = 10
    width = 10

    duplicate_conditions = ({'rotate_180': True},)

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.height):
                    if x < 3 or x > 6 or y < 3 or y > 6:
                        yield coordsys.Triangular3D((x, y, z))

    def customize_piece_data(self):
        self.piece_data['W7'][-1]['flips'] = None


if __name__ == '__main__':
    p = Pentominoes6x10()
    print 'matrix length =', len(p.matrix)
    print 'first 20 rows:'
    pprint(p.matrix[:20], width=720)
