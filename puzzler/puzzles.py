#!/usr/bin/env python
# -*- coding: utf-8 -*-
# $Id$

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2011 by David J. Goodger
# License: GPL 2 (see __init__.py)

import sys
import copy
import datetime
import math
import re
import collections
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
        """A list of lists; see the ExactCover.load_matrix() method of
        puzzler.exact_cover_dlx or puzzler.exact_cover_x2."""

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
        formatted = self.format_solution(solution, normalized=True)
        if self.check_for_duplicates:
            if self.store_solutions(solution, formatted):
                return
        if dated:
            print >>stream, 'at %s,' % datetime.datetime.now(),
        print >>stream, solver.format_solution()
        print >>stream
        print >>stream, self.format_solution(solution, normalized=False)
        print >>stream
        stream.flush()

    def record_dated_solution(self, solution, solver, stream=sys.stdout):
        """A dated variant of `self.record_solution`."""
        self.record_solution(solution, solver, stream=stream, dated=True)

    def format_solution(self, solution, normalized=True):
        """
        Return a puzzle-specific formatting of a solution.

        Implement in subclasses.

        * `solution` is a list of pieces.  Each piece is a list of column
          names from the exact cover matrix: cooridinates and the piece name.

        * `normalized` is a flag; if set, the solution is formatted in a way
          that allows for easy duplicate detection (such as renaming identical
          pieces).
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
                if hasattr(output_path, 'write'):
                    svg_file = output_path
                else:
                    svg_file = open(output_path, 'w')
                svg_file.write(svg)
            finally:
                if not hasattr(output_path, 'write'):
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
        elif hasattr(input_path, 'readline'):
            input_file = input_path
        else:
            input_file = open(input_path, 'r')
        try:
            for line in input_file:
                match = self.solution_header.match(line)
                if match:
                    #number = int(match.group(1))
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
        Return True if the solution is a duplicate, false if unique.

        Store the formatted solution along with puzzle-specific variants
        (reflections, rotations) in `self.solutions`, to check for duplicates.
        """
        if formatted in self.solutions:
            return True
        self.solutions.add(formatted)
        # keep track of formatted variants of *this* solution, to
        # differentiate from previous solutions:
        solutions = set([formatted])
        for conditions in self.duplicate_conditions:
            formatted = self.format_solution(solution, **conditions)
            if formatted in self.solutions:
                # applying duplicate conditions may result in variant
                # solutions identical to `formatted`
                if formatted not in solutions:
                    return True
            else:
                self.solutions.add(formatted)
                solutions.add(formatted)
        return False


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
                aspect = coordsys.Cartesian2DView(coord_list, rotation, flip)
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

    def format_solution(self, solution, normalized=True,
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

    def format_coords_svg(self, piece_name='0'):
        s_matrix = self.empty_solution_matrix(margin=self.margin)
        for x, y in self.solution_coords:
            s_matrix[y + self.margin][x + self.margin] = piece_name
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
            coord_set = coordsys.Cartesian3DView(coord_list)
            if axis != 2:
                coord_set = coord_set.rotate0(1, (1 - axis) % 3)
            coords = tuple(coord_set)
            for flip in flips or (0,):
                for rotation in rotations or (0,):
                    aspect = coordsys.Cartesian3DView(
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

    def format_solution(self, solution, normalized=True,
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

    def format_coords_svg(self, piece_name='0'):
        s_matrix = self.empty_solution_matrix(margin=self.margin)
        for x, y, z in self.solution_coords:
            s_matrix[z + self.margin][y + self.margin][
                x + self.margin] = piece_name
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

    def format_coords_svg(self, piece_name='0'):
        s_matrix = self.empty_solution_matrix(margin=self.margin)
        for x, y, z in self.solution_coords:
            s_matrix[z][y + self.margin][x + self.margin] = piece_name
        return self.format_svg(s_matrix=s_matrix)

    def format_x3d(self, solution=None, s_matrix=None):
        raise NotImplementedError


class OneSidedLowercaseMixin(object):

    """
    Must be the first base class listed in client subclass definitions for
    MRO (method resolution order) to work.
    """

    def customize_piece_data(self):
        """
        Disable flips on all pieces, and add flipped versions of asymmetric
        pieces with lowercase names.
        """
        self.piece_colors = copy.deepcopy(self.piece_colors)
        for key in self.piece_data.keys():
            self.piece_data[key][-1]['flips'] = None
        for key in self.asymmetric_pieces:
            new_key = key.lower()
            self.piece_data[new_key] = copy.deepcopy(self.piece_data[key])
            self.piece_data[new_key][-1]['flips'] = (1,)
            self.piece_colors[new_key] = self.piece_colors[key]


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
        '0': 'gray',
        '1': 'black'}


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


class Pentominoes8x8WithoutCorners(Pentominoes):

    """2170 solutions"""

    height = 8
    width = 8

    def customize_piece_data(self):
        self.piece_data['P'][-1]['flips'] = None
        self.piece_data['P'][-1]['rotations'] = None

    def coordinates(self):
        for y in range(self.height):
            for x in range(self.width):
                if (x == 0 or x == 7) and (y == 0 or y == 7):
                    continue
                yield coordsys.Cartesian2D((x, y))


class OneSidedPentominoes(OneSidedLowercaseMixin, Pentominoes):

    def format_solution(self, solution,  normalized=True, **kwargs):
        """Convert solutions to uppercase to avoid duplicates."""
        formatted = Pentominoes.format_solution(
            self, solution, normalized, **kwargs)
        if normalized:
            return formatted.upper()
        else:
            return formatted


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
                        yield coordsys.Cartesian3D((x, y, z))


class SolidPentominoes6x6x6Crystal1(SolidPentominoes):

    """2 solutions"""

    width = 6
    height = 6
    depth = 6

    def customize_piece_data(self):
        self.piece_data['P'][-1]['flips'] = None
        self.piece_data['P'][-1]['axes'] = None

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if x + y + z < 6:
                        yield coordsys.Cartesian3D((x, y, z))
        for x, y, z in ((1,1,4), (1,4,1), (4,1,1), (2,2,2)):
            yield coordsys.Cartesian3D((x, y, z))


class SolidPentominoes6x6x6Crystal2(SolidPentominoes):

    """1 solution"""

    width = 6
    height = 6
    depth = 6

    def customize_piece_data(self):
        self.piece_data['P'][-1]['flips'] = None

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if x + y + z < 6:
                        yield coordsys.Cartesian3D((x, y, z))
        for x, y, z in ((1,2,3), (2,2,2), (3,2,1), (1,4,1)):
            yield coordsys.Cartesian3D((x, y, z))


class SolidPentominoes6x6x6Crystal3(SolidPentominoes):

    """9 solutions"""

    width = 6
    height = 6
    depth = 6

    def customize_piece_data(self):
        self.piece_data['P'][-1]['axes'] = None

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if x + y + z < 6:
                        yield coordsys.Cartesian3D((x, y, z))
        for x, y, z in ((1,2,3), (3,1,2), (2,3,1), (2,2,2)):
            yield coordsys.Cartesian3D((x, y, z))


class SolidPentominoes6x6x6CrystalX1(SolidPentominoes):

    """0 solutions"""

    width = 6
    height = 6
    depth = 6

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if x + y + z < 6:
                        yield coordsys.Cartesian3D((x, y, z))
        for x, y, z in ((1,1,4), (2,1,3), (3,1,2), (4,1,1)):
            yield coordsys.Cartesian3D((x, y, z))


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
                        yield coordsys.Cartesian3D((x, y, z))
        for x, y, z in ((0,0,6), (0,6,0), (6,0,0), (2,2,2)):
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
        '0': 'gray',
        '1': 'black'}


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
        '0':  'gray',
        '1':  'black'}

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
                        yield coordsys.Cartesian3D((x, y, z))

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
                        yield coordsys.Cartesian3D((x, y, z))


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
                    coords.add(coordsys.Cartesian3D((i, j, 4)))
                    coords.add(coordsys.Cartesian3D((i, 4, j)))
                    coords.add(coordsys.Cartesian3D((4, i, j)))
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
                        yield coordsys.Cartesian3D((x, y, z))


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
            yield coordsys.Cartesian3D(coord)

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
                        yield coordsys.Cartesian3D((x, y, z))


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
                        yield coordsys.Cartesian3D((x, y, z))


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
                        yield coordsys.Cartesian3D((x, y, z))

    transform_solution_matrix = Puzzle3D.swap_yz_transform


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

    def format_solution(self, solution, normalized=True,
                        x_reversed=False, y_reversed=False, z_reversed=False):
        """
        Consider J3 and L3 as the same piece for solution counting purposes.
        """
        formatted = Pentacubes.format_solution(
            self, solution, normalized, x_reversed=x_reversed,
            y_reversed=y_reversed, z_reversed=z_reversed)
        if normalized:
            return formatted.replace('J3', 'L3')
        else:
            return formatted


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
                    coords.add(coordsys.Cartesian3D((i, j, 5)))
                    coords.add(coordsys.Cartesian3D((i, 5, j)))
                    coords.add(coordsys.Cartesian3D((5, i, j)))
        return sorted(coords)


class NonConvexPentacubes(Pentacubes):

    """
    These are the regular pentacubes less the I piece, the only convex piece.
    """

    def customize_piece_data(self):
        """Remove I."""
        Pentacubes.customize_piece_data(self)
        del self.piece_data['I']


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
                        yield coordsys.Cartesian3D((x, y, z))

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
                        yield coordsys.Cartesian3D((x, y, z))

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
                        yield coordsys.Cartesian3D((x, y, z))

    transform_solution_matrix = Puzzle3D.cycle_xyz_transform


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
        '0': 'gray',
        '1': 'black'}

    check_for_duplicates = False

    def format_solution(self, solution, normalized=True,
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


class SomaTunnel(SomaCubes):

    """26 solutions."""

    height = 3
    width = 5
    depth = 3

    check_for_duplicates = True
    duplicate_conditions = ({'x_reversed': True, 'z_reversed': True},)

    def coordinates(self):
        for (x, y) in ((0,0), (1,0), (1,1), (1,2), (2,2),
                       (3,2), (3,1), (3,0), (4,0)):
            for z in range(self.depth):
                yield coordsys.Cartesian3D((x, y, z))


class SomaScrew(SomaCubes):

    """14 solutions."""

    height = 5
    width = 3
    depth = 3

    def coordinates(self):
        holes = set(((0,0,1), (0,0,2), (1,0,2), (1,1,2), (2,1,2), (2,1,1),
                     (2,2,1), (2,2,0), (1,2,0), (1,3,0), (0,3,0), (0,3,1)))
        top = ((2,4,2), (2,4,1), (1,4,1))
        for z in range(self.depth):
            for y in range(self.height - 1):
                for x in range(self.width):
                    if (x,y,z) not in holes:
                        yield coordsys.Cartesian3D((x, y, z))
        for (x,y,z) in top:
            yield coordsys.Cartesian3D((x, y, z))


class SomaClip(SomaCubes):

    """20 solutions."""

    height = 4
    width = 4
    depth = 3

    check_for_duplicates = True
    duplicate_conditions = ({'z_reversed': True, 'xy_swapped': True},)

    def coordinates(self):
        for x in range(self.width):
            for y in range(self.height):
                if   ((y == 0) or (x == 0)
                      or (x == 3 and y == 1) or (y == 3 and x == 1)):
                    for z in range(self.depth):
                        yield coordsys.Cartesian3D((x, y, z))

    transform_solution_matrix = Puzzle3D.cycle_xyz_transform


class Polysticks(PuzzlePseudo3D):

    # line segment orientation (horizontal=0, vertical=1):
    depth = 2

    margin = 1

    svg_path = '''\
<path stroke="%(color)s" stroke-width="%(stroke_width)s" stroke-linecap="round"
      fill="none" d="%(path_data)s">
<desc>%(name)s</desc>
</path>
'''

    svg_stroke_width = '2'
    """Width of line segments."""

    svg_curve_radius = '2.5'
    svg_line = 'M %(x).3f,%(y).3f l %(dx).3f,%(dy).3f'
    svg_line_length = 6
    svg_line_end_offset = 7.5
    svg_line_start_offset = 2.5
    # difference between a terminal line segment & one with a curve attached:
    svg_line_end_delta = 0.5
    svg_ne_curve = 'M %(x).3f,%(y).3f a 2.5,2.5 0 0,0 -2.5,-2.5'
    svg_nw_curve = 'M %(x).3f,%(y).3f a 2.5,2.5 0 0,1 +2.5,-2.5'
    svg_se_curve = 'M %(x).3f,%(y).3f a 2.5,2.5 0 0,0 +2.5,-2.5'
    svg_sw_curve = 'M %(x).3f,%(y).3f a 2.5,2.5 0 0,1 -2.5,-2.5'

## initial attempt to generalize the above & format_svg:
#   svg_curve = ('M %(x).3f,%(y).3f a %(radius)s,%(radius)s 0 0,%(sweep)i'
#                ' %(x_sign)s%(radius)s,-%(radius)s')
#   svg_path_data = {
#       0: Struct(curve_neighbors={(+1, 0, 0): Struct(dx=7.5, dy=0,
#                                                     sweep=0, x_sign='+'),
#                                  (0, 0, 0): Struct(dx=2.5, dy=0,
#                                                    sweep=1, x_sign='-')},
#                 ),
#       1: Struct(curve_neighbors={(-1, +1, 0): Struct(dx=0, dy=7.5,
#                                                      sweep=0, x_sign='-'),
#                                  (0, +1, 0): Struct(dx=0, dy=7.5,
#                                                     sweep=1, x_sign='+')},
#                 start_neighbors=(Struct(dx=-1, dy=0, dlength=-.5, dstart=.5),
#                                  Struct(dx=0,  dy=0, dlength=-.5, dstart=.5)),
#                 end_neighbors=(Struct(dx=-1, dy=1, dlength=-.5),
#                                Struct(dx=0,  dy=1, dlength=-.5)))}

    def coordinates(self):
        """
        Return coordinates for a typical rectangular polystick puzzle.
        """
        return self.coordinates_bordered(self.width, self.height)

    def coordinates_bordered(self, m, n):
        """MxN bordered polystick grid."""
        last_x = m - 1
        last_y = n - 1
        for y in range(n):
            for x in range(m):
                for z in range(2):
                    if (z == 1 and y == last_y) or (z == 0 and x == last_x):
                        continue
                    yield coordsys.SquareGrid3D((x, y, z))

    def coordinates_unbordered(self, m, n):
        """MxN unbordered polystick grid."""
        for y in range(n - 1):
            for x in range(m - 1):
                for z in range(2):
                    if (z == 1 and x == 0) or (z == 0 and y == 0):
                        continue
                    yield coordsys.SquareGrid3D((x, y, z))

    def coordinates_diamond_lattice(self, m, n):
        """MxN polystick diamond lattice."""
        height = width = m + n
        sw = m - 2
        ne = m + 2 * n - 1
        nw = -m - 1
        se = m
        for y in range(height):
            for x in range(width):
                for z in range(2):
                    if nw < (x - y - z) < se and sw < (x + y) < ne:
                        yield coordsys.SquareGrid3D((x, y, z))

    def make_aspects(self, units, flips=(0, 1), rotations=(0, 1, 2, 3)):
        aspects = set()
        for flip in flips or (0,):
            for rotation in rotations or (0,):
                aspect = coordsys.SquareGrid3DView(
                    units, rotation, 0, flip) # 0 is axis, ignored
                aspects.add(aspect)
        return aspects

    def build_matrix_header(self):
        headers = []
        for i, key in enumerate(sorted(self.pieces.keys())):
            self.matrix_columns[key] = i
            headers.append(key)
        deltas = ((1,0,0), (0,1,0))
        intersections = set()
        for coord in sorted(self.solution_coords):
            (x, y, z) = coord
            header = '%0*i,%0*i,%0*i' % (
                self.x_width, x, self.y_width, y, self.z_width, z)
            self.matrix_columns[header] = len(headers)
            headers.append(header)
            next = coord + deltas[z]
            if next in self.solution_coords:
                intersections.add(next[:2])
        primary = len(headers)
        for (x, y) in sorted(intersections):
            header = '%0*i,%0*ii' % (self.x_width, x, self.y_width, y)
            self.matrix_columns[header] = len(headers)
            headers.append(header)
        self.secondary_columns = len(headers) - primary
        self.matrix.append(headers)

    def build_regular_matrix(self, keys):
        for key in keys:
            for coords, aspect in self.pieces[key]:
                for y in range(self.height - aspect.bounds[1]):
                    for x in range(self.width - aspect.bounds[0]):
                        translated = aspect.translate((x, y, 0))
                        if translated.issubset(self.solution_coords):
                            self.build_matrix_row(key, translated)

    def build_matrix_row(self, name, coords):
        row = [0] * len(self.matrix[0])
        row[self.matrix_columns[name]] = name
        for (x,y,z) in coords:
            label = '%0*i,%0*i,%0*i' % (
                self.x_width, x, self.y_width, y, self.z_width, z)
            row[self.matrix_columns[label]] = label
        for (x,y) in coords.intersections():
            label = '%0*i,%0*ii' % (self.x_width, x, self.y_width, y)
            if label in self.matrix_columns:
                row[self.matrix_columns[label]] = label
        self.matrix.append(row)

    def format_solution(self, solution, normalized=True,
                        x_reversed=False, y_reversed=False, xy_swapped=False,
                        rotation=False):
        order_functions = (lambda x: x, reversed)
        x_reversed_fn = order_functions[x_reversed]
        y_reversed_fn = order_functions[1 - y_reversed] # reversed by default
        h_matrix, v_matrix, omitted, prefix = self.build_solution_matrices(
            solution, xy_swapped, rotation)
        lines = []
        for y in range(self.height):
            h_segments = []
            # !!! [:-1] is a hack. Works for bordered grids only:
            for name in x_reversed_fn(h_matrix[y][:-1]):
                if name == ' ':
                    h_segments.append('    ')
                else:
                    h_segments.append(('-%s--' % name)[:4])
            lines.append(' ' + ' '.join(h_segments).rstrip())
            if y != self.height - 1:
                v_segments_1 = [name[0] for name in x_reversed_fn(v_matrix[y])]
                v_segments_2 = []
                for name in x_reversed_fn(v_matrix[y]):
                    if name == ' ':
                        v_segments_2.append(' ')
                    else:
                        v_segments_2.append((name + '|')[1])
                lines.append(
                    '%s\n%s'
                    % ('    '.join(v_segments_1).rstrip(),
                       '    '.join(v_segments_2).rstrip()))
        formatted = (prefix + '\n'.join(y_reversed_fn(lines)))
        if normalized:
            return formatted.upper()
        else:
            return formatted

    def build_solution_matrices(self, solution,
                                xy_swapped=False, rotation=False, margin=0):
        h_matrix = [[' '] * (self.width + 2 * margin)
                    for y in range(self.height + 2 * margin)]
        v_matrix = [[' '] * (self.width + 2 * margin)
                    for y in range(self.height + 2 * margin)]
        matrices = [h_matrix, v_matrix]
        omitted = []
        prefix = []
        for row in solution:
            name = row[-1]
            if row[0] == '!':
                omitted.append(name)
                prefix.append('(%s omitted)\n' % name)
                continue
            for segment_coords in row[:-1]:
                if segment_coords[-1] == 'i':
                    continue
                x, y, z = (int(d.strip()) for d in segment_coords.split(','))
                direction = z
                x, y, direction = self.rotate_segment(x, y, direction, rotation)
                if xy_swapped:
                    x, y = y, x
                    direction = 1 - direction
                matrices[direction][y + margin][x + margin] = name
        return h_matrix, v_matrix, omitted, '\n'.join(prefix)

    def rotate_segment(self, x, y, direction, rotation):
        quadrant = rotation % 4
        if quadrant:
            coords = (x, y)
            x = (coords[quadrant % 2] * (-2 * ((quadrant + 1) // 2 % 2) + 1)
                 + (self.width - 1) * ((quadrant + 1) // 2 % 2))
            y = (coords[(quadrant + 1) % 2] * (-2 * (quadrant // 2 % 2) + 1)
                 + (self.height - 1) * (quadrant // 2 % 2))
            if  ((direction == 1 and quadrant == 1)
                 or (direction == 0 and quadrant == 2)):
                x -= 1
            elif ((direction == 1 and quadrant == 2)
                  or (direction == 0 and quadrant == 3)):
                y -= 1
            if quadrant != 2:
                direction = 1 - direction
        return x, y, direction

    def convert_record_to_solution_matrix(self, record):
        s_matrix = self.empty_solution_matrix(self.margin)
        for row in record:
            parts = row.split()
            name = parts[-1]
            for coords in parts[:-1]:
                if coords.endswith('i') or coords == '!':
                    continue            # skip intersections
                x, y, z = (int(coord) for coord in coords.split(','))
                s_matrix[z][y + self.margin][x + self.margin] = name
        return s_matrix

    def build_solution_matrix(self, solution, margin=0):
        s_matrix = self.empty_solution_matrix(margin)
        for row in solution:
            name = row[-1]
            for cell_name in row[:-1]:
                if cell_name.endswith('i') or cell_name == '!':
                    continue
                x, y, z = [int(d.strip()) for d in cell_name.split(',')]
                s_matrix[z][y + margin][x + margin] = name
        return s_matrix

    def empty_solution_matrix(self, margin=0):
        s_matrix = [[[self.empty_cell] * (self.width + 2 * margin)
                     for y in range(self.height + 2 * margin)]
                    for z in range(self.depth)]
        return s_matrix

    def format_svg(self, solution=None, s_matrix=None):
        if s_matrix:
            assert solution is None, ('Provide only one of solution '
                                      '& s_matrix arguments, not both.')
        else:
            s_matrix = self.build_solution_matrix(solution, margin=1)
        paths = []
        for x in range(1, self.width + 1):
            for y in range(1, self.height + 1):
                for z in range(self.depth):
                    if s_matrix[z][y][x] == self.empty_cell:
                        continue
                    paths.append(self.build_path(s_matrix, x, y, z))
        header = self.svg_header % {
            'height': (self.height + 1) * self.svg_unit_height,
            'width': (self.width + 1) * self.svg_unit_width}
        return '%s%s%s%s%s' % (header, self.svg_g_start, ''.join(paths),
                               self.svg_g_end, self.svg_footer)

    def build_path(self, s_matrix, x, y, z):
        name = s_matrix[z][y][x]
        color = self.piece_colors[name]
        cells = self.get_piece_cells(s_matrix, x, y, z)
        segments = self.get_path_segments(cells, s_matrix, x, y, z)
        path_str = ' '.join(segments)
        return self.svg_path % {'color': color,
                                'stroke_width': self.svg_stroke_width,
                                'path_data': path_str,
                                'name': name}

    def get_piece_cells(self, s_matrix, x, y, z):
        cell_content = s_matrix[z][y][x]
        coord = coordsys.SquareGrid3D((x, y, z))
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

    def get_path_segments(self, cells, s_matrix, x, y, z):
        # this code is long & hairy, but the alternative may be worse ;-)
        segments = []
        unit = self.svg_unit_length
        height = (self.height + 1) * unit
        for (x,y,z) in cells:
            if z:                       # vertical
                if (x-1,y+1,0) in cells:
                    segments.append(self.svg_ne_curve % {
                        'x': x * unit,
                        'y': height - (y * unit + self.svg_line_end_offset)})
                if (x,y+1,0) in cells:
                    segments.append(self.svg_nw_curve % {
                        'x': x * unit,
                        'y': height - (y * unit + self.svg_line_end_offset)})
                if s_matrix[z][y][x] == self.empty_cell:
                    continue
                s_matrix[z][y][x] = self.empty_cell
                y_start = y
                while (x,y_start-1,z) in cells:
                    y_start -= 1
                    s_matrix[z][y_start][x] = self.empty_cell
                y_end = y
                while (x,y_end+1,z) in cells:
                    y_end += 1
                    s_matrix[z][y_end][x] = self.empty_cell
                x_from = x * unit
                dx = 0
                y_from = y_start * unit + (self.svg_line_start_offset
                                           - self.svg_line_end_delta)
                dy = self.svg_line_length + (y_end - y_start) * unit
                if (x-1,y_start,0) in cells or (x,y_start,0) in cells:
                    y_from += self.svg_line_end_delta
                    dy -= self.svg_line_end_delta
                if (x-1,y_end+1,0) in cells or (x,y_end+1,0) in cells:
                    dy -= self.svg_line_end_delta
                segments.append(self.svg_line % {
                    'x': x_from, 'dx': dx, 'y': (height - y_from), 'dy': -dy})
            else:                       # horizontal
                if (x+1,y,1) in cells:
                    segments.append(self.svg_se_curve % {
                        'x': x * unit + self.svg_line_end_offset,
                        'y': height - y * unit})
                if (x,y,1) in cells:
                    segments.append(self.svg_sw_curve % {
                        'x': x * unit + self.svg_line_start_offset,
                        'y': height - y * unit})
                if s_matrix[z][y][x] == self.empty_cell:
                    continue
                s_matrix[z][y][x] = self.empty_cell
                x_start = x
                while (x_start-1,y,z) in cells:
                    x_start -= 1
                    s_matrix[z][y][x_start] = self.empty_cell
                x_end = x
                while (x_end+1,y,z) in cells:
                    x_end += 1
                    s_matrix[z][y][x_end] = self.empty_cell
                x_from = x_start * unit + (self.svg_line_start_offset
                                           - self.svg_line_end_delta)
                dx = self.svg_line_length + (x_end - x_start) * unit
                y_from = y * unit
                dy = 0
                if (x_start,y,1) in cells or (x_start,y-1,1) in cells:
                    x_from += self.svg_line_end_delta
                    dx -= self.svg_line_end_delta
                if (x_end+1,y,1) in cells or (x_end+1,y-1,1) in cells:
                    dx -= self.svg_line_end_delta
                segments.append(self.svg_line % {
                    'x': x_from, 'dx': dx, 'y': height - y_from, 'dy': dy})
        return segments


class Tetrasticks(Polysticks):

    piece_data = {
        'I': (((0,0,0), (1,0,0), (2,0,0), (3,0,0)), {}),
        'L': (((0,0,0), (1,0,0), (2,0,0), (3,0,1)), {}),
        'Y': (((0,0,0), (1,0,0), (2,0,0), (2,0,1)), {}),
        'V': (((0,0,0), (1,0,0), (2,0,1), (2,1,1)), {}),
        'T': (((0,0,0), (1,0,0), (1,0,1), (1,1,1)), {}),
        'X': (((0,1,0), (1,1,0), (1,0,1), (1,1,1)), {}),
        'U': (((0,0,0), (1,0,0), (0,0,1), (2,0,1)), {}),
        'N': (((0,0,0), (1,0,0), (2,0,1), (2,1,0)), {}),
        'J': (((0,0,0), (1,0,0), (2,0,1), (1,1,0)), {}),
        'H': (((0,0,0), (1,0,0), (1,0,1), (1,1,0)), {}),
        'F': (((0,0,0), (1,0,0), (0,0,1), (1,0,1)), {}),
        'Z': (((0,0,1), (0,1,0), (1,1,0), (2,1,1)), {}),
        'R': (((0,0,1), (0,1,0), (1,1,0), (1,1,1)), {}),
        'W': (((0,0,0), (1,0,1), (1,1,0), (2,1,1)), {}),
        'P': (((0,0,1), (0,1,0), (1,0,1), (1,0,0)), {}),
        'O': (((0,0,0), (1,0,1), (0,1,0), (0,0,1)), {})}
    """Line segments."""

    symmetric_pieces = 'I O T U V W X'.split()
    """Pieces with reflexive symmetry, identical to their mirror images."""

    asymmetric_pieces = 'F H J L N P R Y Z'.split()
    """Pieces without reflexive symmetry, different from their mirror images."""

    welded_pieces = 'F H R T X Y'.split()
    """Pieces with junction points (where 3 or more segments join)."""

    unwelded_pieces = 'I J L N O P U V W Z'.split()
    """Pieces without junction points (max. 2 segments join)."""

    imbalance_omittable_pieces = 'H J L N Y'.split()
    """Pieces to be omitted (one at a time) to remove an overall imbalance."""

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
        'J': 'darkseagreen',
        'H': 'peru',
        'R': 'rosybrown',
        'O': 'yellowgreen',
        '0': 'gray',
        '1': 'black'}

    def build_rows_for_omitted_pieces(self):
        """
        Build matrix rows for omitted pieces to remove an overall imbalance.
        """
        for name in self.imbalance_omittable_pieces:
            row = [0] * len(self.matrix[0])
            row[self.matrix_columns['!']] = name
            row[self.matrix_columns[name]] = name
            self.matrix.append(row)

    def make_aspects(self, units, flips=(0, 1), rotations=(0, 1, 2, 3)):
        if units:
            return Polysticks.make_aspects(
                self, units, flips=flips, rotations=rotations)
        else:
            return set()


class Polysticks123Data(object):

    piece_data = {
        'I1': (((0,0,0),), {}),
        'I2': (((0,0,0), (1,0,0)), {}),
        'V2': (((0,0,0), (0,0,1)), {}),
        'I3': (((0,0,0), (1,0,0), (2,0,0)), {}),
        'L3': (((0,0,0), (1,0,0), (2,0,1)), {}),
        'T3': (((0,0,0), (1,0,0), (1,0,1)), {}),
        'Z3': (((0,1,0), (1,0,1), (1,0,0)), {}),
        'U3': (((0,0,1), (0,0,0), (1,0,1)), {}),}

    piece_colors = {
        'I1': 'steelblue',
        'I2': 'gray',
        'V2': 'lightcoral',
        'I3': 'olive',
        'L3': 'teal',
        'T3': 'tan',
        'Z3': 'indigo',
        'U3': 'orangered',
        '0': 'gray',
        '1': 'black'}


class Polysticks123(Polysticks123Data, Polysticks):

    pass


class WeldedTetrasticks5x5(Tetrasticks):

    """
    3 solutions (perfect solutions, i.e. no pieces cross).
    2 solutions are perfectly symmetrical in reflection.
    """

    width = 5
    height = 5

    check_for_duplicates = True
    duplicate_conditions = ({'rotation': 1},
                            {'rotation': 2},
                            {'rotation': 3},
                            {'x_reversed': True},
                            {'y_reversed': True},
                            {'xy_swapped': True},
                            {'x_reversed': True,
                             'rotation': 1},
                            {'y_reversed': True,
                             'rotation': 1},
                            {'xy_swapped': True,
                             'rotation': 1},
                            {'x_reversed': True,
                             'rotation': 2},
                            {'y_reversed': True,
                             'rotation': 2},
                            {'xy_swapped': True,
                             'rotation': 2},
                            {'x_reversed': True,
                             'rotation': 3},
                            {'y_reversed': True,
                             'rotation': 3},
                            {'xy_swapped': True,
                             'rotation': 3},)

    def customize_piece_data(self):
        self.piece_colors = copy.deepcopy(self.piece_colors)
        for key in self.unwelded_pieces:
            del self.piece_data[key]
        for key in self.asymmetric_pieces:
            if key not in self.piece_data:
                continue
            self.piece_data[key][-1]['flips'] = None
            new_key = key.lower()
            self.piece_data[new_key] = copy.deepcopy(self.piece_data[key])
            self.piece_data[new_key][-1]['flips'] = (1,)
            self.piece_colors[new_key] = self.piece_colors[key]


class Tetrasticks6x6(Tetrasticks):

    """
    1795 solutions total:

    * 72 solutions omitting H
    * 382 omitting J
    * 607 omitting L
    * 530 omitting N
    * 204 omitting Y

    All are perfect solutions (i.e. no pieces cross).
    """

    width = 6
    height = 6

    check_for_duplicates = True
    duplicate_conditions = ({'xy_swapped': True},)

    def customize_piece_data(self):
        self.piece_data['!'] = ((), {})

    def build_matrix(self):
        self.build_rows_for_omitted_pieces()
        x_coords, x_aspect = self.pieces['X'][0]
        self.build_matrix_row('X', x_aspect)
        for x in range(2):
            translated = x_aspect.translate((x, 1, 0))
            self.build_matrix_row('X', translated)
        keys = sorted(self.pieces.keys())
        keys.remove('X')
        self.build_regular_matrix(keys)


class Tetrasticks3x5DiamondLattice(Tetrasticks):

    """
    0 solutions
    """

    width = 8
    height = 8

    def customize_piece_data(self):
        self.piece_data['!'] = ((), {})
        self.piece_data['P'][-1]['flips'] = None
        self.piece_data['P'][-1]['rotations'] = (0,1)

    def build_matrix(self):
        self.build_rows_for_omitted_pieces()
        self.build_regular_matrix(sorted(self.pieces.keys()))

    def coordinates(self):
        return self.coordinates_diamond_lattice(5, 3)


class OneSidedTetrasticks(OneSidedLowercaseMixin, Tetrasticks):

    pass


class OneSidedTetrasticks5x5DiamondLattice(OneSidedTetrasticks):

    """
    107 solutions (see "Covering the Aztec Diamond with One-sided Tetrasticks,
    Extended Version", by `Alfred Wassermann`_).

    .. _Alfred Wassermann:
       http://did.mat.uni-bayreuth.de/~alfred/home/index.html
    """

    width = 10
    height = 10

    check_for_duplicates = False

    @classmethod
    def components(cls):
        return (OneSidedTetrasticks5x5DiamondLattice_A,
                OneSidedTetrasticks5x5DiamondLattice_B,
                OneSidedTetrasticks5x5DiamondLattice_C,
                OneSidedTetrasticks5x5DiamondLattice_D,
                OneSidedTetrasticks5x5DiamondLattice_E,
                OneSidedTetrasticks5x5DiamondLattice_F,)

    def _customize_piece_data_I(self):
        """
        Limit I piece to horizontal when X is symmetrical (on the diagonal).
        """
        OneSidedTetrasticks.customize_piece_data(self)
        self.piece_data['I'][-1]['rotations'] = None

    def coordinates(self):
        return self.coordinates_diamond_lattice(5, 5)

    def build_matrix(self):
        """"""
        keys = sorted(self.pieces.keys())
        x_coords, x_aspect = self.pieces['X'][0]
        translated = x_aspect.translate(self.X_offset)
        self.build_matrix_row('X', translated)
        keys.remove('X')
        self.build_regular_matrix(keys)


class OneSidedTetrasticks5x5DiamondLattice_A(
    OneSidedTetrasticks5x5DiamondLattice):

    """? solutions."""

    X_offset = (4,4,0)

    def customize_piece_data(self):
        self._customize_piece_data_I()


class OneSidedTetrasticks5x5DiamondLattice_B(
    OneSidedTetrasticks5x5DiamondLattice):

    """? solutions."""

    X_offset = (4,5,0)


class OneSidedTetrasticks5x5DiamondLattice_C(
    OneSidedTetrasticks5x5DiamondLattice):

    """? solutions."""

    X_offset = (5,5,0)

    def customize_piece_data(self):
        self._customize_piece_data_I()


class OneSidedTetrasticks5x5DiamondLattice_D(
    OneSidedTetrasticks5x5DiamondLattice):

    """? solutions."""

    X_offset = (4,6,0)


class OneSidedTetrasticks5x5DiamondLattice_E(
    OneSidedTetrasticks5x5DiamondLattice):

    """? solutions."""

    X_offset = (5,6,0)


class OneSidedTetrasticks5x5DiamondLattice_F(
    OneSidedTetrasticks5x5DiamondLattice):

    """? solutions."""

    X_offset = (4,7,0)


class OneSidedTetrasticks8x8CenterHole(OneSidedTetrasticks):

    """
    ? solutions
    """

    width = 8
    height = 8

    def customize_piece_data(self):
        OneSidedTetrasticks.customize_piece_data(self)
        self.piece_data['P'][-1]['rotations'] = None
        # enough for uniqueness?

    def coordinates(self):
        hole = coordsys.SquareGrid3DCoordSet(self.coordinates_unbordered(4, 4))
        hole = hole.translate((2, 2, 0))
        for coord in self.coordinates_bordered(self.width, self.height):
            if coord not in hole:
                yield coord


class OneSidedTetrasticks8x8ClippedCorners1(OneSidedTetrasticks):

    """
    ? solutions
    """

    width = 8
    height = 8

    def coordinates(self):
        hole = set(((0,5,1),(0,6,0),(0,6,1),(0,7,0),(1,6,1),(1,7,0),
                    (5,0,0),(6,0,0),(6,0,1),(6,1,0),(7,0,1),(7,1,1)))
        for coord in self.coordinates_bordered(self.width, self.height):
            if coord not in hole:
                yield coord


class OneSidedTetrasticks8x8ClippedCorners2(OneSidedTetrasticks):

    """
    ? solutions
    """

    width = 8
    height = 8

    def coordinates(self):
        hole = set(((0,5,1),(0,6,0),(0,6,1),(0,7,0),(1,6,1),(1,7,0),
                    (5,7,0),(6,6,0),(6,6,1),(6,7,0),(7,5,1),(7,6,1)))
        for coord in self.coordinates_bordered(self.width, self.height):
            if coord not in hole:
                yield coord


class OneSidedTetrasticks8x8ClippedCorner(OneSidedTetrasticks):

    """
    ? solutions
    """

    width = 8
    height = 8

    def coordinates(self):
        hole = set(((0,4,1),(0,5,0),(0,5,1),(0,6,0),(0,6,1),(0,7,0),
                    (1,5,1),(1,6,0),(1,6,1),(1,7,0),(2,6,1),(2,7,0)))
        for coord in self.coordinates_bordered(self.width, self.height):
            if coord not in hole:
                yield coord


class OneSidedTetrasticks6x10CenterHole(OneSidedTetrasticks):

    """
    ? solutions
    """

    width = 10
    height = 6

    def coordinates(self):
        hole = coordsys.SquareGrid3DCoordSet(self.coordinates_bordered(2, 2))
        hole = hole.translate((4, 2, 0))
        for coord in self.coordinates_bordered(self.width, self.height):
            if coord not in hole:
                yield coord


class OneSidedTetrasticks6x10Slot(OneSidedTetrasticks):

    """
    ? solutions
    """

    width = 10
    height = 6

    def coordinates(self):
        hole = set(((3,2,1),(4,2,1),(5,2,1),(6,2,1)))
        for coord in self.coordinates_bordered(self.width, self.height):
            if coord not in hole:
                yield coord


class OneSidedTetrasticks6x10SideHoles(OneSidedTetrasticks):

    """
    ? solutions
    """

    width = 10
    height = 6

    def coordinates(self):
        hole = set(((0,2,1),(4,0,0),(4,5,0),(9,2,1)))
        for coord in self.coordinates_bordered(self.width, self.height):
            if coord not in hole:
                yield coord


class OneSidedTetrasticks6x10ClippedCorners1(OneSidedTetrasticks):

    """
    ? solutions
    """

    width = 10
    height = 6

    def coordinates(self):
        hole = set(((0,4,1),(0,5,0),(8,0,0),(9,0,1)))
        for coord in self.coordinates_bordered(self.width, self.height):
            if coord not in hole:
                yield coord


class OneSidedTetrasticks6x10ClippedCorners2(OneSidedTetrasticks):

    """
    ? solutions
    """

    width = 10
    height = 6

    def coordinates(self):
        hole = set(((0,4,1),(0,5,0),(8,5,0),(9,4,1)))
        for coord in self.coordinates_bordered(self.width, self.height):
            if coord not in hole:
                yield coord


class OneSidedTetrasticks6x10ClippedCorners3(OneSidedTetrasticks):

    """
    ? solutions
    """

    width = 10
    height = 6

    def coordinates(self):
        hole = set(((8,0,0),(8,5,0),(9,0,1),(9,4,1)))
        for coord in self.coordinates_bordered(self.width, self.height):
            if coord not in hole:
                yield coord


class Polysticks1234(Tetrasticks, Polysticks123Data):

    piece_data = copy.deepcopy(Tetrasticks.piece_data)
    piece_data.update(copy.deepcopy(Polysticks123Data.piece_data))
    piece_colors = copy.deepcopy(Tetrasticks.piece_colors)
    piece_colors.update(Polysticks123Data.piece_colors)


class Polysticks1234_7x7(Polysticks1234):

    """
    ? solutions (very large number; over 35000 unique solutions in first
    position of X, I, & I1)
    (perfect solutions, i.e. no pieces cross).
    """

    width = 7
    height = 7

    def customize_piece_data(self):
        self.piece_data['P'][-1]['flips'] = None
        self.piece_data['P'][-1]['rotations'] = None


class Polysticks1234_3x7DiamondLattice(Polysticks1234):

    """
    ? solutions
    """

    width = 10
    height = 10

    def customize_piece_data(self):
        self.piece_data['P'][-1]['flips'] = None
        self.piece_data['P'][-1]['rotations'] = (0,1)

    def coordinates(self):
        return self.coordinates_diamond_lattice(7, 3)


class Polysticks1234_8x8Unbordered(Polysticks1234):

    """
    ? solutions
    """

    width = 8
    height = 8

    def coordinates(self):
        return self.coordinates_unbordered(self.width, self.height)


class Polysticks1234_5x5DiamondLatticeRing(Polysticks1234):

    """
    """

    width = 10
    height = 10

    def customize_piece_data(self):
        self.piece_data['P'][-1]['flips'] = None
        self.piece_data['P'][-1]['rotations'] = None

    def coordinates(self):
        hole = set((coord + (3,3,0))
                   for coord in self.coordinates_diamond_lattice(2, 2))
        return list(set(self.coordinates_diamond_lattice(5, 5)) - hole)


class Polysticks123_4x4Corners(Polysticks123):

    """
    0 solutions
    """

    width = 4
    height = 4

    def coordinates(self):
        last_x = self.width - 1
        last_y = self.height - 1
        for y in range(self.height):
            for x in range(self.width):
                for z in range(self.depth):
                    if ( (z == 1 and y == last_y)
                         or (z == 0 and x == last_x)
                         or (x,y,z) in ((1,1,0),(1,1,1),(1,2,0),(2,1,1))):
                        continue
                    yield coordsys.SquareGrid3D((x, y, z))


class Polytrigs(Polysticks):

    """
    'Polytrigs' == triangular polysticks ('trig' = TRIangular Grid).
    """

    # line segment orientation (horizontal/right=0, 60deg=1, 120deg=2):
    depth = 3

    margin = 1

    svg_stroke_width = 1.6
    """Width of line segments."""

    svg_unit_height = Polysticks.svg_unit_length * math.sqrt(3) / 2

    svg_curve = 'M %(x0).3f,%(y0).3f a %(r).3f,%(r).3f 0 0,1 %(dx).3f,%(dy).3f'

    def __init__(self, init_puzzle=True):
        Polysticks.__init__(self, init_puzzle=init_puzzle)
        self.svg_deltas, self.svg_radii = self.calculate_svg_details()

    def coordinates(self):
        """
        Return coordinates for a typical parallelogram polytrig puzzle.
        """
        return self.coordinates_bordered(self.width, self.height)

    def coordinate_offset(self, x, y, z, offset):
        if offset:
            return coordsys.TriangularGrid3D((x, y, z)) + offset
        else:
            return coordsys.TriangularGrid3D((x, y, z))

    def coordinates_bordered(self, m, n, offset=None):
        """
        Bordered parallelogram polytrig grid of side length M & N.

        **NOTE:** Puzzle length & width must include edges, typically M+1 x
        N+1.
        """
        last_x = m
        last_y = n
        for y in range(n + 1):
            for x in range(m + 1):
                for z in range(self.depth):
                    if (z != 0 and y == last_y) or (z == 0 and x == last_x):
                        continue
                    if z == 2 and x == 0:
                        continue
                    yield self.coordinate_offset(x, y, z, offset)

    def coordinates_unbordered(self, m, n, offset=None):
        """Unbordered parallelogram polytrig grid of side length M & N."""
        last_x = m
        last_y = n
        for y in range(n):
            for x in range(m + 1):
                for z in range(self.depth):
                    if (not y and z == 0) or (x == last_x and z < 2):
                        continue
                    if x == 0 and z != 0:
                        continue
                    yield self.coordinate_offset(x, y, z, offset)

    def coordinates_triangle(self, side_length, offset=None):
        """Triangular bordered polytrig grid."""
        for coord in self.coordinates_bordered(side_length, side_length):
            x, y, z = coord
            xy = x + y
            if (xy > side_length) or ((xy == side_length) and (z != 2)):
                continue
            yield self.coordinate_offset(x, y, z, offset)

    def coordinates_hexagon(self, side_length, offset=None):
        """Hexagonal bordered polytrig grid."""
        min_xy = side_length
        max_xy = 3 * side_length
        bound = 2 * side_length
        for coord in self.coordinates_bordered(bound, bound):
            x, y, z = coord
            xy = x + y
            if (xy < min_xy) or (xy > max_xy) or ((xy == max_xy) and (z != 2)):
                continue
            yield self.coordinate_offset(x, y, z, offset)

    def coordinates_hexagon_unbordered(self, side_length, offset=None):
        """Hexagonal unbordered polytrig grid."""
        min_xy = side_length
        max_xy = 3 * side_length
        bound = 2 * side_length
        for coord in self.coordinates_unbordered(bound, bound):
            x, y, z = coord
            xy = x + y
            if (xy < min_xy) or (xy == min_xy and z == 2) or (xy >= max_xy):
                continue
            yield self.coordinate_offset(x, y, z, offset)

    def coordinates_semiregular_hexagon(self, side_a, side_b, offset=None):
        """Semi-regular hexagonal bordered polytrig grid."""
        if side_a < side_b:
            side_a, side_b = side_b, side_a
        min_xy = side_b
        max_xy = side_a + 2 * side_b
        bound = side_a + side_b
        for coord in self.coordinates_bordered(bound, bound):
            x, y, z = coord
            xy = x + y
            if (xy < min_xy) or (xy > max_xy) or ((xy == max_xy) and (z != 2)):
                continue
            yield self.coordinate_offset(x, y, z, offset)

    def coordinates_elongated_hexagon(self, base_length, side_length,
                                      offset=None):
        """Elongated hexagonal bordered polytrig grid."""
        min_xy = side_length
        max_xy = base_length + side_length * 2
        x_bound = side_length + base_length
        y_bound = side_length * 2
        for coord in self.coordinates_bordered(x_bound, y_bound):
            x, y, z = coord
            xy = x + y
            if (xy < min_xy) or (xy > max_xy) or ((xy == max_xy) and (z != 2)):
                continue
            yield self.coordinate_offset(x, y, z, offset)

    def coordinates_trapezoid(self, width, height, offset=None):
        max_xy = width
        for coord in self.coordinates_bordered(width, height):
            x, y, z = coord
            xy = x + y
            if (xy < max_xy) or (xy == max_xy and z == 2):
                yield self.coordinate_offset(x, y, z, offset)

    def coordinates_butterfly(self, base_length, side_length, offset=None):
        """Butterfly-shaped bordered polytrig grid."""
        x_bound = max_xy = base_length + side_length
        y_bound = min_xy = side_length * 2
        for coord in self.coordinates_bordered(x_bound, y_bound):
            x, y, z = coord
            xy = x + y
            xz = x - z / 2
            if (  (side_length <= xz < base_length)
                  or (x == base_length and z != 0)
                  or (min_xy <= xy < max_xy)
                  or (xy == max_xy and z == 2)):
                yield self.coordinate_offset(x, y, z, offset)

    def coordinates_chevron(self, base_length, side_length, offset=None):
        x_bound = base_length + side_length
        y_bound = min_xy = side_length * 2
        max_xy = base_length + side_length * 2
        for coord in self.coordinates_bordered(x_bound, y_bound):
            x, y, z = coord
            xy = x + y
            if (  ((y < side_length)
                   and ((x > side_length) or (x == side_length and z != 2)))
                  or ((y >= side_length)
                      and ((min_xy <= xy < max_xy)
                           or (xy == max_xy and z == 2)))):
                yield self.coordinate_offset(x, y, z, offset)

    def make_aspects(self, units, flips=(0, 1), rotations=(0, 1, 2, 3, 4, 5)):
        aspects = set()
        for flip in flips or (0,):
            for rotation in rotations or (0,):
                aspect = coordsys.TriangularGrid3DView(
                    units, rotation, 0, flip) # 0 is axis, ignored
                aspects.add(aspect)
        return aspects

    def build_matrix_header(self):
        headers = []
        for i, key in enumerate(sorted(self.pieces.keys())):
            self.matrix_columns[key] = i
            headers.append(key)
        deltas = ((1,0,0), (0,1,0), (-1,1,0))
        intersections = set()
        for coord in sorted(self.solution_coords):
            (x, y, z) = coord
            header = '%0*i,%0*i,%0*i' % (
                self.x_width, x, self.y_width, y, self.z_width, z)
            self.matrix_columns[header] = len(headers)
            headers.append(header)
            intersections.update(set(coord.intersection_coordinates()))
        primary = len(headers)
        for (x, y, z) in sorted(intersections):
            header = '%0*i,%0*i,%01ii' % (self.x_width, x, self.y_width, y, z)
            self.matrix_columns[header] = len(headers)
            headers.append(header)
        self.secondary_columns = len(headers) - primary
        self.matrix.append(headers)

    def build_matrix_row(self, name, coords):
        row = [0] * len(self.matrix[0])
        row[self.matrix_columns[name]] = name
        for (x,y,z) in coords:
            label = '%0*i,%0*i,%0*i' % (
                self.x_width, x, self.y_width, y, self.z_width, z)
            row[self.matrix_columns[label]] = label
        for (x,y,z) in coords.intersections():
            label = '%0*i,%0*i,%ii' % (self.x_width, x, self.y_width, y, z)
            if label in self.matrix_columns:
                row[self.matrix_columns[label]] = label
        self.matrix.append(row)

    def format_solution(self, solution, normalized=True, rotate_180=False):
        s_matrix = self.build_solution_matrix(solution)
        if rotate_180:
            s_matrix = [[list(reversed(s_matrix[z][y]))
                         for y in reversed(range(self.height))]
                        for z in reversed(range(self.depth))]
        return self.format_triangular_grid(s_matrix)

    _trigrid_parts = (
        # z == 0:
        (('', '', '_%-3s'),            # occupied cell, lines[0..2]
         ('', '', '    ')),             # empty cell
        # z == 1:
        (('  /', '%-3s', '/'),         # occupied cell
         ('   ', '   ', ' ')),          # empty cell
        # z == 2:
        (('%-3s', ' \\ ', '\\'),       # occupied cell
         ('   ', '   ', ' ')))          # empty cell

    def format_triangular_grid(self, s_matrix):
        """
        In order to have enough space for two characters per segment, the
        solutions will have to be formatted at least this big::

                   __03__
                  /\    /\
                 I  I1 I2 I3
                /_12_\/_01_\
               /\    /\    /\
              02 Z  Z3 V  V2 01
             /_02_\/_01_\/_01_\

        3 sections to each triangle:

        * z==0::

            __12__

        * z==1::

              /
             I2
            /

        * z==2::

            \
             I3
              \

        Note: there is overlap between the far-left and -right character of
        the horizontal z==0 section and the bottom characters of the slanted
        z==1 & z==2 sections.  The slanted z==1 & z==2 sections have priority.

        For 3 characters per segment, we can get away with the same size::

                   __03x_
                  /I1x  /I3x
                III \ I2x \
                /_12x\/_01x\

        For 3 characters per segment, a larger representation would be better.
        For or 4 or even 5, it would be needed::

                   __03xx__
                  /\      /\
                 /  I1xx /  I3xx
                IIxx \  I2xx \
               /_12xx_\/_01xx_\
        """
        width = len(s_matrix[0][0])
        height = len(s_matrix[0])
        min_padding = width * 6
        output = []
        # highest y first, to render it at top:
        for y in reversed(range(height)):
            lines = [['   ' * y] for i in range(3)]
            # bottom line needs extra padding for initial z==2:
            lines[-1].append('  ')
            cell0_occupied = False
            for x in range(width):
                # left to right, top to bottom order:
                for z in reversed(range(self.depth)):
                    if z == 1:
                        # current z==2 is above previous cell0, so skip;
                        # cell0_occupied applies to current z==1 and next z==2:
                        cell0_occupied = (s_matrix[0][y][x] != self.empty_cell)
                    cell = s_matrix[z][y][x]
                    cell_type_index = (cell == self.empty_cell)
                    for i, parts in enumerate(lines):
                        part = self._trigrid_parts[z][cell_type_index][i]
                        if '%' in part:
                            part = part % cell
                        if '_' in part:
                            # no blanks in horizontal lines.
                            part = part.replace(' ', '_')
                        if part == ' ' and cell0_occupied:
                            # extend horizontal lines when there's no slant:
                            part = '_'
                        parts.append(part)
            for parts in lines:
                line = ''.join(parts)
                min_padding = min(min_padding, len(line) - len(line.lstrip()))
                output.append(line.rstrip())
        while not output[0].strip():
            del output[0]
        if min_padding:
            for i, line in enumerate(output):
                output[i] = line[min_padding:]
        return '\n'.join(output)

    def format_coords(self):
        s_matrix = self.empty_solution_matrix()
        for x, y, z in self.solution_coords:
            s_matrix[z][y][x] = ''
        return self.format_triangular_grid(s_matrix)

    def format_svg(self, solution=None, s_matrix=None):
        if s_matrix:
            assert solution is None, (
                'Provide only one of solution & s_matrix arguments, not both.')
        else:
            s_matrix = self.build_solution_matrix(solution, margin=self.margin)
        paths = self.svg_paths(s_matrix)
        header = self.svg_header % {
            'height': (self.height) * self.svg_unit_height,
            'width': (self.width + self.height/2.0 - 0.5) * self.svg_unit_width}
        return '%s%s%s%s%s' % (header, self.svg_g_start, ''.join(paths),
                               self.svg_g_end, self.svg_footer)

    def svg_paths(self, s_matrix):
        """Calculate path data and convert it into SVG paths."""
        lines, curves = self.svg_path_data(s_matrix)
        paths = []
        for name in sorted(lines):
            path_data = []
            for ((x0, y0), (x1, y1)) in lines[name].values():
                path_details = {
                    'x': x0, 'y': y0, 'dx': (x1 - x0), 'dy': (y1 - y0)}
                path_data.append(self.svg_line % path_details)
            for ((x0, y0), (x1, y1), r) in curves[name]:
                path_details = {
                    'x0': x0, 'y0': y0, 'dx': (x1 - x0), 'dy': (y1 - y0),
                    'r': r}
                path_data.append(self.svg_curve % path_details)
            path_data.sort()
            details = {
                'name': name,
                'color': self.piece_colors[name],
                'stroke_width': self.svg_stroke_width,
                'path_data': ' '.join(path_data)}
            paths.append(self.svg_path % details)
        return paths

    def svg_path_data(self, s_matrix):
        s_coords = sorted(self.solution_coords)
        xy_coords = set()
        lines = collections.defaultdict(dict)
        curves = {}
        margin = self.margin
        for coord in s_coords:
            (x, y, z) = coord
            name = s_matrix[z][y + margin][x + margin]
            if name == self.empty_cell:
                continue
            # initial line segment end coordinates; may be adjusted below:
            lines[name][coord] = self.svg_line_coords(coord)
            curves[name] = []
            xy_coords.add((x, y))
            (x, y, z) = coord.endpoint()
            xy_coords.add((x, y))
        for (x, y) in xy_coords:
            neighbors = coordsys.TriangularGrid3D.point_neighbors(x, y)
            names = [s_matrix[zn][yn + margin][xn + margin]
                     for (xn, yn, zn) in neighbors]
            for z in range(6):
                # adjust line segment ends
                line_z = neighbors[z]
                name_z = names[z]
                if name_z == self.empty_cell:
                    continue
                end_index = 0 + (z > 2)
                if names[(z + 3) % 6] == name_z:
                    # 180° line exists, no adjustment necessary
                    continue
                elif ((names[(z + 1) % 6] == name_z)
                      or (names[(z - 1) % 6] == name_z)):
                    # 60° line
                    end_type = 1
                elif ((names[(z + 2) % 6] == name_z)
                      or (names[(z - 2) % 6] == name_z)):
                    # 120° line 
                    end_type = 2
                else:
                    # stub/end line
                    end_type = 0
                lines[name_z][line_z][end_index] += self.svg_deltas[end_type][z]
            coord = self.svg_coord(neighbors[0])
            for z in range(6):
                # add curve data for joining line segments
                line_z = neighbors[z]
                name_z = names[z]
                if name_z == self.empty_cell:
                    continue
                # check next 3 neighbors, counter-clockwise:
                for n in range(z + 1, z + 3 + (z < 3)):
                    line_n = neighbors[n % 6]
                    name_n = names[n % 6]
                    if name_z != name_n:
                        continue
                    if 1 <= n - z <= 2:
                        start = coord + self.svg_deltas[n - z][z]
                        end = coord + self.svg_deltas[n - z][n % 6]
                        curves[name_n].append(
                            (start, end, self.svg_radii[n - z]))
        return lines, curves

    def svg_line_coords(self, coord):
        """
        Return the (x,y) coordinates of the start- and end-points of the
        full-length trigrid line segment (x,y,z), as a list.
        """
        return [self.svg_coord(c) for c in (coord, coord.endpoint())]

    def svg_coord(self, coord):
        """
        Return the SVG (x,y) coordinates of the start-point of the trigrid
        coordinate.
        """
        x, y, z = coord 
        yunit = self.svg_unit_height
        height = (self.height - 0.5) * yunit
        return coordsys.Cartesian2D(
            ((x + (y + 1) / 2.0) * self.svg_unit_width, height - y * yunit))
        
    def calculate_svg_details(self):
        # called from __init__
        """
        For 60° angle, line thickness "t", line end must be >= sqrt(3)t short
        (~= 1.732t; for t=16, short 27.71).

        For 120° angle, line thickness "t", line end must be >= (1 +
        sqrt(3)/2)t short (~= 1.866t; for t=16, short 29.85).

        Curve end-points (relative to intersection point)::

               (-dx1, +dy1).    .(+dx1, +dy1)
                            \  /
                (-dx0, 0).___\/___.(+dx0, 0)
                             /\
                            /  \
               (-dx1, -dy1).    .(+dx1, -dy1)

        For unit length = 100, line thickness = 16:

        ===  =======  =========  =========  ==========
        var  formula  stub/end   60°        120°
        ===  =======  =========  =========  ==========
        dx0           26         30         32
        dx1  =dx0/2   13         15         16
        dy1  =dx1*√3  22.516660  25.980762  27.7128129
        r    =dx0/√3  n/a        17.320508
        r    =dx0*√3  n/a                   55.4256258
        ===  =======  =========  =========  ==========
        """
        unit_length = self.svg_unit_length
        sqrt3 = 3 ** .5
        dx0 = (unit_length * .26,       # stub/end
               unit_length * .30,       # 60°
               unit_length * .32)       # 120°
        dx1 = tuple(val / 2 for val in dx0)
        dy1 = tuple(val * sqrt3 for val in dx1)
        svg_deltas = [
            ((+dx0[i], 0),
             (+dx1[i], -dy1[i]),
             (-dx1[i], -dy1[i]),
             (-dx0[i], 0),
             (-dx1[i], +dy1[i]),
             (+dx1[i], +dy1[i])) for i in range(3)]
        svg_radii = (None, dx0[1] / sqrt3, dx0[2] * sqrt3)
        return svg_deltas, svg_radii


class MonotrigsData(object):

    piece_data = {
        'I1': (((0,0,0),), {}),}

    symmetric_pieces = 'I1'.split()
    """Pieces with reflexive symmetry, identical to their mirror images."""

    asymmetric_pieces = []
    """Pieces without reflexive symmetry, different from their mirror images."""

    piece_colors = {
        'I1': 'steelblue',}


class DitrigsData(object):

    piece_data = {
        'I2': (((0,0,0), (1,0,0)), {}),
        'L2': (((0,0,0), (1,0,1)), {}),
        'V2': (((0,0,0), (1,0,2)), {}),}

    symmetric_pieces = 'I2 L2 V2'.split()
    """Pieces with reflexive symmetry, identical to their mirror images."""

    asymmetric_pieces = []
    """Pieces without reflexive symmetry, different from their mirror images."""

    piece_colors = {
        'I2': 'gray',
        'L2': 'teal',
        'V2': 'lightcoral',}


class Polytrigs12(Polytrigs):

    piece_data = copy.deepcopy(MonotrigsData.piece_data)
    piece_data.update(copy.deepcopy(DitrigsData.piece_data))
    symmetric_pieces = (
        MonotrigsData.symmetric_pieces + DitrigsData.symmetric_pieces)
    asymmetric_pieces = []
    piece_colors = copy.deepcopy(MonotrigsData.piece_colors)
    piece_colors.update(DitrigsData.piece_colors)


class TritrigsData(object):

    piece_data = {
        'I3': (((0,0,0), (1,0,0), (2,0,0)), {}),
        'L3': (((0,0,0), (1,0,0), (2,0,1)), {}),
        'J3': (((0,0,0), (1,0,0), (2,0,2)), {}),
        'T3': (((0,0,0), (1,0,0), (1,0,1)), {}),
        'S3': (((0,0,0), (1,0,1), (1,1,0)), {}),
        'C3': (((0,0,0), (1,0,1), (1,1,2)), {}),
        'U3': (((0,0,0), (1,0,1), (0,1,0)), {}),
        'P3': (((0,0,0), (1,0,1), (2,0,2)), {}),
        'E3': (((0,0,0), (1,0,1), (1,0,2)), {}),
        'Y3': (((0,1,0), (1,1,1), (2,0,2)), {}),
        'Z3': (((0,0,0), (1,0,2), (0,1,0)), {}),
        'O3': (((0,0,0), (1,0,2), (0,0,1)), {}),}

    symmetric_pieces = 'I3 C3 E3 Y3 O3'.split()
    """Pieces with reflexive symmetry, identical to their mirror images."""

    asymmetric_pieces = 'L3 J3 T3 S3 U3 P3 Z3'.split()
    """Pieces without reflexive symmetry, different from their mirror images."""

    piece_colors = {
        'I3': 'blue',
        'O3': 'red',
        'Y3': 'green',
        'L3': 'lime',
        'S3': 'navy',
        'P3': 'magenta',
        'T3': 'darkorange',
        'U3': 'turquoise',
        'J3': 'blueviolet',
        'E3': 'maroon',
        'C3': 'gold',
        'Z3': 'plum',
        '0': 'gray',
        '1': 'black'}


class Tritrigs(TritrigsData, Polytrigs):

    pass


class OneSidedTritrigs(OneSidedLowercaseMixin, Tritrigs):

    pass


class Polytrigs123(Polytrigs12):

    piece_data = copy.deepcopy(Polytrigs12.piece_data)
    piece_data.update(copy.deepcopy(TritrigsData.piece_data))
    symmetric_pieces = (
        Polytrigs12.symmetric_pieces + TritrigsData.symmetric_pieces)
    asymmetric_pieces = TritrigsData.asymmetric_pieces[:]
    piece_colors = copy.deepcopy(Polytrigs12.piece_colors)
    piece_colors.update(TritrigsData.piece_colors)
    

class OneSidedPolytrigs123(OneSidedLowercaseMixin, Polytrigs123):

    pass


class TetratrigsData(object):

    piece_data = {
        'B04': (((0,0,0), (1,0,1), (1,1,0), (2,0,1)), {}),
        'B14': (((0,0,0), (1,0,2), (0,1,0), (2,0,2)), {}),
        'C04': (((1,0,0), (1,0,2), (0,1,1), (0,2,0)), {}),
        'D04': (((0,0,0), (0,0,1), (0,1,0), (2,0,2)), {}),
        'D14': (((0,0,1), (0,1,0), (2,0,2), (2,0,0)), {}),
        'D24': (((0,0,1), (0,1,0), (2,0,2), (2,0,1)), {}),
        'E04': (((0,0,1), (0,1,0), (2,0,2), (1,0,2)), {}),
        'E14': (((0,1,0), (1,1,0), (1,1,1), (2,0,2)), {}),
        'E24': (((0,0,0), (1,0,1), (2,0,2), (1,1,0)), {}),
        'F04': (((0,0,0), (1,0,0), (1,0,1), (2,0,1)), {}),
        'F14': (((0,0,0), (1,0,0), (1,0,2), (2,0,2)), {}),
        'F24': (((0,0,0), (1,0,0), (1,0,2), (2,0,1)), {}),
        'H04': (((0,0,0), (1,0,0), (1,0,1), (0,1,0)), {}),
        'H14': (((0,0,0), (1,0,0), (1,0,1), (1,1,0)), {}),
        'H24': (((0,0,0), (1,0,0), (1,0,1), (1,1,2)), {}),
        'H34': (((0,0,0), (1,0,0), (2,0,2), (1,1,1)), {}),
        'H44': (((0,0,0), (1,0,1), (1,1,0), (1,1,2)), {}),
        'I04': (((0,0,0), (1,0,0), (2,0,0), (3,0,0)), {}),
        'J04': (((0,0,0), (1,0,0), (2,0,0), (3,0,2)), {}),
        'J14': (((0,0,0), (1,0,0), (2,0,1), (2,1,2)), {}),
        'J24': (((0,0,0), (1,0,0), (2,0,1), (1,1,0)), {}),
        'J34': (((0,0,0), (1,0,0), (2,0,2), (0,1,0)), {}),
        'K04': (((0,0,0), (1,0,0), (1,0,1), (1,0,2)), {}),
        'L04': (((0,0,0), (1,0,0), (2,0,0), (3,0,1)), {}),
        'M04': (((1,0,0), (1,0,1), (1,1,2), (0,2,0)), {}),
        'N04': (((0,0,0), (1,0,0), (2,0,2), (1,1,0)), {}),
        'N14': (((0,0,0), (1,0,1), (2,0,2), (2,0,1)), {}),
        'N24': (((0,0,0), (1,0,1), (2,0,2), (1,0,2)), {}),
        'O04': (((0,0,0), (1,0,1), (0,1,0), (0,0,1)), {}),
        'P04': (((0,0,0), (1,0,0), (1,0,1), (2,0,2)), {}),
        'P14': (((0,0,0), (1,0,1), (1,0,2), (0,1,0)), {}),
        'P24': (((0,0,0), (1,0,0), (2,0,1), (3,0,2)), {}),
        'Q04': (((1,0,0), (2,0,2), (0,1,0), (1,1,1)), {}),
        'Q14': (((1,1,0), (2,1,2), (0,2,0), (1,0,1)), {}),
        'Q24': (((1,0,0), (2,0,2), (0,1,0), (0,1,1)), {}),
        'Q34': (((1,0,0), (2,0,2), (0,1,0), (2,0,1)), {}),
        'R04': (((0,1,0), (1,1,0), (3,0,2), (1,1,1)), {}),
        'R14': (((0,1,0), (1,1,0), (3,0,2), (1,1,2)), {}),
        'R24': (((0,1,0), (1,1,0), (2,0,1), (1,1,2)), {}),
        'R34': (((0,1,0), (1,1,0), (2,0,1), (1,1,1)), {}),
        'S04': (((0,0,1), (0,1,0), (1,1,0), (2,1,1)), {}),
        'S14': (((0,0,0), (1,0,1), (1,1,0), (2,1,0)), {}),
        'S24': (((0,0,1), (0,1,0), (1,1,0), (2,1,2)), {}),
        'T04': (((0,0,1), (0,1,0), (1,1,0), (0,1,1)), {}),
        'T14': (((1,0,2), (0,1,0), (1,1,0), (0,1,1)), {}),
        'U04': (((0,0,1), (0,1,0), (1,1,0), (2,0,1)), {}),
        'U14': (((0,0,1), (0,1,0), (1,1,0), (3,0,2)), {}),
        'U24': (((0,0,1), (0,0,0), (1,0,0), (2,0,2)), {}),
        'V04': (((0,0,0), (1,0,0), (0,0,1), (0,1,1)), {}),
        'V14': (((0,0,0), (1,0,0), (2,0,1), (2,1,1)), {}),
        'V24': (((0,0,0), (1,0,1), (2,0,2), (2,0,0)), {}),
        'W04': (((0,0,1), (1,0,2), (1,0,1), (2,0,2)), {}),
        'W14': (((0,0,0), (1,0,1), (1,1,0), (2,1,1)), {}),
        'W24': (((0,0,0), (1,0,1), (1,1,0), (2,1,2)), {}),
        'X04': (((0,1,0), (1,1,0), (1,0,1), (1,1,1)), {}),
        'Y04': (((0,1,0), (1,1,0), (2,1,1), (3,0,2)), {}),
        'Y14': (((0,0,0), (1,0,0), (2,0,0), (2,0,1)), {}),
        'Y24': (((0,0,0), (1,0,0), (2,0,0), (2,0,2)), {}),
        'Y34': (((0,0,0), (1,0,0), (2,0,1), (2,0,2)), {}),
        'Z04': (((0,1,1), (0,1,0), (1,1,0), (2,0,1)), {}),
        }

    symmetric_pieces = (
        'C04 E14 I04 K04 M04 O04 T14 U14 U24 V04 V14 V24 W04 W14 X04 Y04'
        .split())
    """Pieces with reflexive symmetry, identical to their mirror images."""

    asymmetric_pieces = (
        'B04 B14 D04 D14 D24 E04 E24 F04 F14 F24 H04 H14 H24 H34 H44 '
        'J04 J14 J24 J34 L04 N04 N14 N24 P04 P14 P24 Q04 Q14 Q24 Q34 '
        'R04 R14 R24 R34 S04 S14 S24 T04 U04 W24 Y14 Y24 Y34 Z04').split()
    """Pieces without reflexive symmetry, different from their mirror images."""

    piece_colors = {
        'I04': 'blue',
        'O04': 'red',
        'X04': 'green',
        'C04': 'lime',
        'E14': 'navy',
        'P04': 'magenta',
        'T04': 'darkorange',
        'T14': 'turquoise',
        'K04': 'blueviolet',
        'M04': 'maroon',
        'S04': 'gold',
        'U04': 'plum',
        'U14': 'darkseagreen',
        'U24': 'peru',
        'V04': 'lightcoral',
        'V14': 'steelblue',
        'V24': 'gray',
        'W04': 'teal',
        'W14': 'olive',
        'Y04': 'yellow',
        'Z04': 'indigo',
        'B04': 'tan',
        'B14': 'cyan',
        'D04': 'aquamarine',
        'D14': 'brown',
        'D24': 'cadetblue',
        'E04': 'burlywood',
        'E24': 'crimson',
        'F04': 'darkgoldenrod',
        'F14': 'darkgreen',
        'F24': 'darkkhaki',
        'H04': 'darkseagreen',
        'H14': 'deeppink',
        'H24': 'greenyellow',
        'H34': 'hotpink',
        'H44': 'khaki',
        'J04': 'lightblue',
        'J14': 'lightseagreen',
        'J24': 'lightsteelblue',
        'J34': 'limegreen',
        'L04': 'mediumpurple',
        'N04': 'orange',
        'N14': 'palegreen',
        'N24': 'paleturquoise',
        'P14': 'palevioletred',
        'P24': 'peachpuff',
        'Q04': 'plum',
        'Q14': 'silver',
        'Q24': 'thistle',
        'Q34': 'tomato',
        'R04': 'violet',
        'R14': 'wheat',
        'R24': 'lightpink',
        'R34': 'lightslategray',
        'S14': 'darkmagenta',
        'S24': 'deepskyblue',
        'W24': 'indianred',
        'Y14': 'slateblue',
        'Y24': 'olivedrab',
        'Y34': 'darkorchid',
        '0': 'gray',
        '1': 'black'}


class Tetratrigs(TetratrigsData, Polytrigs):

    pass


class Polytrigs1234(Polytrigs123):

    piece_data = copy.deepcopy(Polytrigs123.piece_data)
    piece_data.update(copy.deepcopy(TetratrigsData.piece_data))
    symmetric_pieces = (
        Polytrigs123.symmetric_pieces + TetratrigsData.symmetric_pieces)
    asymmetric_pieces = (
        Polytrigs123.asymmetric_pieces + TetratrigsData.asymmetric_pieces)
    piece_colors = copy.deepcopy(Polytrigs123.piece_colors)
    piece_colors.update(TetratrigsData.piece_colors)


class TritrigsHex2Ring(Tritrigs):

    """0 solutions."""

    width = 5
    height = 5

    def coordinates(self):
        hole = set([(2,2,0), (2,2,1), (2,2,2), (1,2,0), (2,1,1), (3,1,2)])
        for coord in self.coordinates_hexagon(2):
            if coord not in hole:
                yield coord

    def customize_piece_data(self):
        self.piece_data['P3'][-1]['flips'] = None
        self.piece_data['P3'][-1]['rotations'] = None


class TritrigsHex3x1Ring(Tritrigs):

    """1 solution."""

    width = 5
    height = 5

    def coordinates(self):
        hole = set([(1,2,0), (2,1,1), (2,1,2)])
        for coord in self.coordinates_semiregular_hexagon(3, 1):
            if coord not in hole:
                yield coord

    def customize_piece_data(self):
        self.piece_data['Z3'][-1]['flips'] = None
        self.piece_data['Z3'][-1]['rotations'] = None


class TritrigsTrapezoid5x3Ring(Tritrigs):

    """1 solution."""

    width = 6
    height = 4

    def coordinates(self):
        hole = set([(2,1,1), (2,1,2)])
        for coord in self.coordinates_trapezoid(5, 3):
            if coord not in hole:
                yield coord

    def customize_piece_data(self):
        self.piece_data['Z3'][-1]['flips'] = None


class TritrigsStackedElongatedHexagons2x2x1(Tritrigs):

    """9 solutions."""

    width = 5
    height = 5

    def coordinates(self):
        hole = set([(1,1,2), (0,2,0), (0,2,1), (4,1,1), (3,2,0), (4,2,2)])
        for coord in self.coordinates_hexagon(2):
            if coord not in hole:
                yield coord

    def customize_piece_data(self):
        self.piece_data['P3'][-1]['flips'] = None
        self.piece_data['P3'][-1]['rotations'] = (0,1,2)


class TritrigsJaggedTrapezoid5x3(Tritrigs):

    """1 solution."""

    width = 6
    height = 4

    def coordinates(self):
        for coord in self.coordinates_trapezoid(5, 3):
            x, y, z = coord
            if y != 3:
                yield coord

    def customize_piece_data(self):
        self.piece_data['Z3'][-1]['flips'] = None


class TritrigsSpikedTriangle1(Tritrigs):

    """6 solutions."""

    width = 6
    height = 6

    def coordinates(self):
        for coord in self.coordinates_triangle(4, (1,1,0)):
            yield coord
        for coord in ((0,5,0), (1,4,2), (2,0,1), (2,0,2), (4,2,0), (5,1,1)):
            yield coordsys.TriangularGrid3D(coord)

    def customize_piece_data(self):
        self.piece_data['I3'][-1]['rotations'] = None
        self.piece_data['I3'][-1]['flips'] = None


class TritrigsSpikedTriangle2(TritrigsSpikedTriangle1):

    """0 solutions."""

    width = 6
    height = 6

    def coordinates(self):
        for coord in self.coordinates_triangle(4, (1,1,0)):
            yield coord
        for coord in ((0,4,0), (1,3,2), (3,0,1), (3,0,2), (3,3,0), (4,2,1)):
            yield coordsys.TriangularGrid3D(coord)


class TritrigsParallelogram5x2(Tritrigs):

    """9 solutions."""

    width = 6
    height = 3

    def coordinates(self):
        for coord in self.coordinates_bordered(5, 2):
            if coord != (2,1,0):
                yield coord

    def customize_piece_data(self):
        self.piece_data['P3'][-1]['rotations'] = (0,1,2)
    

class TritrigsTrapezoid6x2(Tritrigs):

    """8 solutions."""

    width = 7
    height = 3

    def coordinates(self):
        for coord in self.coordinates_trapezoid(6, 2):
            if coord != (2,1,0):
                yield coord

    def customize_piece_data(self):
        self.piece_data['P3'][-1]['flips'] = None
    

class TritrigsTrefoil1(Tritrigs):

    """0 solutions."""

    width = 5
    height = 5

    def coordinates(self):
        holes = set([(1,0,2), (4,0,1), (0,4,0)])
        for coord in self.coordinates_semiregular_hexagon(3, 1):
            if coord not in holes:
                yield coord

#     def customize_piece_data(self):
#         self.piece_data['Z3'][-1]['flips'] = None
#         self.piece_data['Z3'][-1]['rotations'] = None


class TritrigsTrefoil2(Tritrigs):

    """0 solutions."""

    width = 5
    height = 5

    def coordinates(self):
        holes = set([(2,0,0), (0,2,1), (3,2,2)])
        for coord in self.coordinates_semiregular_hexagon(3, 1):
            if coord not in holes:
                yield coord

#     def customize_piece_data(self):
#         self.piece_data['Z3'][-1]['flips'] = None
#         self.piece_data['Z3'][-1]['rotations'] = None


class TritrigsWhorl(Tritrigs):

    """0 solutions."""

    width = 5
    height = 5

    def coordinates(self):
        holes = set([(1,0,0), (0,3,1), (4,1,2)])
        for coord in self.coordinates_semiregular_hexagon(3, 1):
            if coord not in holes:
                yield coord

#     def customize_piece_data(self):
#         self.piece_data['Z3'][-1]['flips'] = None
#         self.piece_data['Z3'][-1]['rotations'] = None


class TritrigsTriangle5(Tritrigs):

    """0 solutions."""

    width = 6
    height = 5

    def coordinates(self):
        hole = set(self.coordinates_triangle(2, offset=(1, 1, 0)))
        for coord in self.coordinates_triangle(5):
            if coord not in hole:
                yield coord


class OneSidedTritrigsSemiRegularHexagon4x1(OneSidedTritrigs):

    """many solutions."""

    width = 6
    height = 6

    def coordinates(self):
        for coord in self.coordinates_semiregular_hexagon(4,1):
            yield coord

    def customize_piece_data(self):
        """Limit I3 piece to one aspect."""
        OneSidedTritrigs.customize_piece_data(self)
        self.piece_data['I3'][-1]['rotations'] = None
        self.piece_data['I3'][-1]['flips'] = None


class OneSidedTritrigsTriangle6(OneSidedTritrigs):

    """many solutions."""

    width = 7
    height = 6

    def coordinates(self):
        hole = set(self.coordinates_hexagon_unbordered(1, offset=(1, 1, 0)))
        for coord in self.coordinates_triangle(6):
            if coord not in hole:
                yield coord

    def customize_piece_data(self):
        """Limit I3 piece to one aspect."""
        OneSidedTritrigs.customize_piece_data(self)
        self.piece_data['I3'][-1]['rotations'] = None
        self.piece_data['I3'][-1]['flips'] = None


class OneSidedTritrigsButterfly5x2(OneSidedTritrigs):

    """many solutions."""

    width = 8
    height = 5

    def coordinates(self):
        return self.coordinates_butterfly(5, 2)

    #def customize_piece_data(self):
    #    OneSidedTritrigs.customize_piece_data(self)


class OneSidedTritrigsChevron3x3(OneSidedTritrigs):

    """many solutions."""

    width = 7
    height = 7

    def coordinates(self):
        hole = set(self.coordinates_hexagon_unbordered(1, offset=(3, 2, 0)))
        for coord in self.coordinates_chevron(3, 3):
            if coord not in hole:
                yield coord

    #def customize_piece_data(self):
    #    OneSidedTritrigs.customize_piece_data(self)


class OneSidedTritrigsChevron2x4_1(OneSidedTritrigs):

    """many solutions."""

    width = 7
    height = 9

    hole = set([(4,4,0)])

    def coordinates(self):
        for coord in self.coordinates_chevron(2, 4):
            if coord not in self.hole:
                yield coord


class OneSidedTritrigsChevron2x4_2(OneSidedTritrigsChevron2x4_1):

    """many solutions."""

    hole = set([(5,4,0)])


class OneSidedTritrigsChevron8x1(OneSidedTritrigs):

    """many solutions."""

    width = 10
    height = 3

    hole = set([(8,1,0)])

    def coordinates(self):
        for coord in self.coordinates_chevron(8, 1):
            if coord not in self.hole:
                yield coord


class OneSidedTritrigsTrapezoid7x3_1(OneSidedTritrigs):

    """many solutions."""

    width = 8
    height = 4

    hole = set([(2,2,0)])

    def coordinates(self):
        for coord in self.coordinates_trapezoid(self.width - 1,
                                                self.height - 1):
            if coord not in self.hole:
                yield coord


class OneSidedTritrigsTrapezoid7x3_2(OneSidedTritrigsTrapezoid7x3_1):

    """many solutions."""

    hole = set([(3,0,0)])


class OneSidedTritrigsTrapezoid9x2_1(OneSidedTritrigsTrapezoid7x3_1):

    """many solutions."""

    width = 10
    height = 3

    hole = set([(4,0,0)])


class OneSidedTritrigsTrapezoid9x2_2(OneSidedTritrigsTrapezoid9x2_1):

    """many solutions."""

    hole = set([(3,2,0)])


class Polytrigs123_4x3(Polytrigs123):

    """many solutions."""

    width = 5
    height = 4

    def coordinates(self):
        return self.coordinates_bordered(4, 3)

    def customize_piece_data(self):
        self.piece_data['P3'][-1]['rotations'] = (0,1,2)


class Polytrigs123Trapezoid5x4(Polytrigs123):

    """many solutions."""

    width = 6
    height = 5

    def coordinates(self):
        return self.coordinates_trapezoid(5, 4)

    def customize_piece_data(self):
        self.piece_data['P3'][-1]['flips'] = None


class Polytrigs123Chevron3x2(Polytrigs123):

    """many solutions."""

    width = 6
    height = 5

    def coordinates(self):
        return self.coordinates_chevron(3, 2)


class Polytrigs123Butterfly4x2(Polytrigs123):

    """many solutions."""

    width = 7
    height = 5

    def coordinates(self):
        for coord in self.coordinates_butterfly(4, 2):
            if coord != (2, 3, 0):
                yield coord


class Polytrigs123Trapezoid7x2_1(Polytrigs123):

    """many solutions."""

    width = 8
    height = 3

    hole = set([(2,2,0)])

    def coordinates(self):
        for coord in self.coordinates_trapezoid(7, 2):
            if coord not in self.hole:
                yield coord


class Polytrigs123Trapezoid7x2_2(Polytrigs123Trapezoid7x2_1):

    """many solutions."""

    hole = set([(3,0,0)])


class Polytrigs123Triangle5_1(Polytrigs123):

    """many solutions."""

    width = 6
    height = 5

    hole = set([(2,1,1), (2,1,2)])

    def coordinates(self):
        for coord in self.coordinates_triangle(5):
            if coord not in self.hole:
                yield coord


class Polytrigs123Triangle5_2(Polytrigs123Triangle5_1):

    """many solutions."""

    hole = set([(1,1,0), (2,1,0)])


class Polytrigs123Triangle5_3(Polytrigs123Triangle5_1):

    """many solutions."""

    hole = set([(1,2,0), (0,4,0)])


class Polytrigs123Triangle5_4(Polytrigs123Triangle5_1):

    """many solutions."""

    hole = set([(0,1,0), (3,1,0)])


class Polytrigs123Triangle5_5(Polytrigs123Triangle5_1):

    """many solutions."""

    hole = set([(0,2,0), (2,2,0)])


class Polytrigs123Triangle5_6(Polytrigs123Triangle5_1):

    """many solutions."""

    hole = set([(0,3,0), (1,3,0)])


class Polytrigs123Triangle5_7(Polytrigs123Triangle5_1):

    """many solutions."""

    hole = set([(1,0,0), (3,0,0)])


class Polytrigs123Triangle5_8(Polytrigs123Triangle5_1):

    """many solutions."""

    hole = set([(2,0,0), (1,2,0)])


class OneSidedPolytrigs123Trapezoid10x2(OneSidedPolytrigs123):

    """many solutions."""

    width = 11
    height = 3

    def coordinates(self):
        for coord in self.coordinates_trapezoid(10, 2):
            if coord != (4, 1, 0):
                yield coord

    def customize_piece_data(self):
        OneSidedPolytrigs123.customize_piece_data(self)
        self.piece_data['P3'][-1]['flips'] = None


class OneSidedPolytrigs123Trapezoid7x4(OneSidedPolytrigs123):

    """many solutions."""

    width = 8
    height = 5

    def coordinates(self):
        hole = set([(3,1,1), (3,1,2), (2,2,0), (2,2,1), (3,2,2)])
        for coord in self.coordinates_trapezoid(7, 4):
            if coord not in hole:
                yield coord

    def customize_piece_data(self):
        OneSidedPolytrigs123.customize_piece_data(self)
        #self.piece_data['P3'][-1]['flips'] = None


class OneSidedPolytrigs123Parallelogram9x2(OneSidedPolytrigs123):

    """many solutions."""

    width = 10
    height = 3

    def coordinates(self):
        for coord in self.coordinates_bordered(9, 2):
            if coord != (4, 1, 0):
                yield coord

    def customize_piece_data(self):
        OneSidedPolytrigs123.customize_piece_data(self)
        self.piece_data['P3'][-1]['rotations'] = (0,1,2)


class OneSidedPolytrigs123Parallelogram5x4(OneSidedPolytrigs123):

    """many solutions."""

    width = 6
    height = 5

    def coordinates(self):
        hole = set([(3,1,1), (3,1,2), (2,2,0), (2,2,1), (3,2,2)])
        for coord in self.coordinates_bordered(5, 4):
            if coord not in hole:
                yield coord

    def customize_piece_data(self):
        OneSidedPolytrigs123.customize_piece_data(self)
        #self.piece_data['P3'][-1]['rotations'] = (0,1,2)


class OneSidedPolytrigs123Butterfly6x2(OneSidedPolytrigs123):

    """many solutions."""

    width = 9
    height = 5

    def coordinates(self):
        hole = set(self.coordinates_hexagon_unbordered(1, offset=(3,1,0)))
        for coord in self.coordinates_butterfly(6, 2):
            if coord not in hole:
                yield coord

    def customize_piece_data(self):
        OneSidedPolytrigs123.customize_piece_data(self)
        self.piece_data['P3'][-1]['rotations'] = (0,1,2)
        self.piece_data['P3'][-1]['flips'] = None


class OneSidedPolytrigs123ElongatedHex4x2_1(OneSidedPolytrigs123):

    """many solutions."""

    width = 7
    height = 5

    hole = set([(1,2,0), (2,2,0), (3,2,0), (4,2,0)])

    def coordinates(self):
        for coord in self.coordinates_elongated_hexagon(4, 2):
            if coord not in self.hole:
                yield coord


class OneSidedPolytrigs123ElongatedHex4x2_2(
    OneSidedPolytrigs123ElongatedHex4x2_1):

    """many solutions."""

    hole = set([(2,3,1), (3,3,2), (1,4,0), (2,4,0)])


class OneSidedPolytrigs123ElongatedHex4x2_3(
    OneSidedPolytrigs123ElongatedHex4x2_1):

    """many solutions."""

    hole = set([(3,0,0), (4,0,0), (1,4,0), (2,4,0)])


class OneSidedPolytrigs123ElongatedHex4x2_4(
    OneSidedPolytrigs123ElongatedHex4x2_1):

    """many solutions."""

    hole = set([(0,4,0), (1,4,0), (2,4,0), (3,4,0)])


class OneSidedPolytrigs123ElongatedHex4x2_5(
    OneSidedPolytrigs123ElongatedHex4x2_1):

    """many solutions."""

    hole = set([(3,1,0), (2,2,0), (3,2,0), (2,3,0)])


class OneSidedPolytrigs123ElongatedHex4x2_6(
    OneSidedPolytrigs123ElongatedHex4x2_1):

    """many solutions."""

    hole = set([(2,2,0), (3,2,0), (3,2,1), (3,2,2)])


class OneSidedPolytrigs123ElongatedHex4x2_7(
    OneSidedPolytrigs123ElongatedHex4x2_1):

    """many solutions."""

    hole = set([(2,0,2), (6,0,1), (0,3,1), (5,3,2)])


class OneSidedPolytrigs123ElongatedHex4x2_8(
    OneSidedPolytrigs123ElongatedHex4x2_1):

    """many solutions."""

    hole = set([(2,0,2), (1,1,2), (6,0,1), (6,1,1)])


class OneSidedPolytrigs123ElongatedHex4x2_9(
    OneSidedPolytrigs123ElongatedHex4x2_1):

    """many solutions."""

    hole = set([(3,1,0), (1,2,0), (4,2,0), (2,3,0)])


class OneSidedPolytrigs123ElongatedHex4x2_10(
    OneSidedPolytrigs123ElongatedHex4x2_1):

    """many solutions."""

    hole = set([(3,1,2), (3,1,1), (4,1,2), (4,1,1)])


class OneSidedPolytrigs123ElongatedHex4x2_11(
    OneSidedPolytrigs123ElongatedHex4x2_1):

    """many solutions."""

    hole = set([(3,1,1), (4,1,2), (3,2,1), (3,2,2)])


class OneSidedPolytrigs123Trapezoid8x3_1(OneSidedPolytrigs123):

    """many solutions."""

    width = 9
    height = 4

    hole = set([(3,1,1), (3,1,2), (4,1,1), (4,1,2)])

    def coordinates(self):
        for coord in self.coordinates_trapezoid(8, 3):
            if coord not in self.hole:
                yield coord


class OneSidedPolytrigs123Trapezoid8x3_2(OneSidedPolytrigs123Trapezoid8x3_1):

    """many solutions."""

    hole = set([(2,1,1), (2,1,2), (5,1,1), (5,1,2)])


class OneSidedPolytrigs123Trapezoid8x3_3(OneSidedPolytrigs123Trapezoid8x3_1):

    """many solutions."""

    hole = set([(2,1,1), (3,1,2), (4,1,1), (5,1,2)])


class OneSidedPolytrigs123Trapezoid8x3_4(OneSidedPolytrigs123Trapezoid8x3_1):

    """many solutions."""

    hole = set([(1,1,1), (3,1,2), (4,1,1), (6,1,2)])


class OneSidedPolytrigs123Chevron9x1(OneSidedPolytrigs123):

    """many solutions."""

    width = 11
    height = 3

    hole = set([(9,1,0)])

    def coordinates(self):
        for coord in self.coordinates_chevron(9, 1):
            if coord not in self.hole:
                yield coord


class TetratrigsElongatedHex11x3(Tetratrigs):

    """ solutions."""

    width = 15
    height = 7

    def coordinates(self):
        holes = set([(6, 4, 0), (7, 2, 0)])
        for coord in self.coordinates_elongated_hexagon(11, 3):
            if coord not in holes:
                yield coord

    def customize_piece_data(self):
        self.piece_data['P04'][-1]['flips'] = None
        self.piece_data['O04'][-1]['flips'] = None
        self.piece_data['O04'][-1]['rotations'] = (1,)

    def build_matrix(self):
        """"""
        keys = sorted(self.pieces.keys())
        o_coords, o_aspect = self.pieces['O04'][0]
        translated = o_aspect.translate((6, 3, 0))
        self.build_matrix_row('O04', translated)
        keys.remove('O04')
        self.build_regular_matrix(keys)


class Polytrigs1234Trapezoid15x8(Polytrigs1234):

    """ solutions."""

    width = 16
    height = 9

    # create multiple sub-puzzles, each with O04 & I1 placed

    def coordinates(self):
        return self.coordinates_trapezoid(15, 8)

    def customize_piece_data(self):
        self.piece_data['P3'][-1]['flips'] = None


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
                aspect = coordsys.Hexagonal2DView(coord_list, rotation, flip)
                aspects.add(aspect)
        return aspects

    def format_solution(self, solution, normalized=True,
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
        '0': 'gray',
        '1': 'black'}


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
        '0': 'gray',
        '1': 'black'}


class Polyhex1234(Polyhexes123Data, Tetrahexes):

    symmetric_pieces = (Polyhexes123Data.symmetric_pieces
                        + Tetrahexes.symmetric_pieces)

    asymmetric_pieces = (Polyhexes123Data.asymmetric_pieces
                         + Tetrahexes.asymmetric_pieces)

    def customize_piece_data(self):
        self.piece_data = copy.deepcopy(Tetrahexes.piece_data)
        self.piece_data.update(copy.deepcopy(Polyhexes123Data.piece_data))
        self.piece_colors = copy.deepcopy(Tetrahexes.piece_colors)
        self.piece_colors.update(Polyhexes123Data.piece_colors)


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
        '0': 'gray',
        '1': 'black'}


class Polyhex12345(Polyhex1234, Pentahexes):

    symmetric_pieces = (Polyhex1234.symmetric_pieces
                        + Pentahexes.symmetric_pieces)

    asymmetric_pieces = (Polyhex1234.asymmetric_pieces
                         + Pentahexes.asymmetric_pieces)

    def customize_piece_data(self):
        Polyhex1234.customize_piece_data(self)
        self.piece_data.update(copy.deepcopy(Pentahexes.piece_data))
        self.piece_colors.update(Pentahexes.piece_colors)


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


class Polyhex12345_3x50(Polyhex12345):

    """0 solutions?"""

    height = 3
    width = 50

    duplicate_conditions = ({'rotate_180': True},)


class Polyhex12345_5x30(Polyhex12345):

    """? solutions"""

    height = 5
    width = 30

    duplicate_conditions = ({'rotate_180': True},)


class Polyhex12345_6x25(Polyhex12345):

    """? solutions"""

    height = 6
    width = 25

    duplicate_conditions = ({'rotate_180': True},)


class Polyhex12345_10x15(Polyhex12345):

    """? solutions"""

    height = 10
    width = 15

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
        return self.coordinates_parallelogram(self.width, self.height)

    def coordinates_parallelogram(self, base_length, side_length, offset=None):
        for z in range(self.depth):
            for y in range(side_length):
                for x in range(base_length):
                    yield self.coordinate_offset(x, y, z, offset)

    def coordinate_offset(self, x, y, z, offset):
        if offset:
            return coordsys.TriangularGrid3D((x, y, z)) + offset
        else:
            return coordsys.TriangularGrid3D((x, y, z))

    def coordinates_hexagram(self, side_length, offset=None):
        max_total = side_length * 5
        min_total = side_length * 3
        for z in range(self.depth):
            for y in range(side_length * 4):
                for x in range(side_length * 4):
                    total = x + y + z
                    if (  (x >= side_length and y >= side_length
                           and total < max_total)
                          or (total >= min_total
                              and x < min_total
                              and y < min_total)):
                        yield self.coordinate_offset(x, y, z, offset)

    def coordinates_butterfly(self, base_length, side_length, offset=None):
        for coord in self.coordinates_parallelogram(base_length + side_length,
                                                    side_length * 2):
            x, y, z = coord
            total = x + y + z
            min_total = side_length * 2
            max_total = base_length + side_length
            if (  (y < side_length and x < side_length)
                  or (y >= side_length and total < min_total)
                  or (x >= base_length and total >= max_total)):
                continue
            yield self.coordinate_offset(x, y, z, offset)

    def make_aspects(self, units, flips=(False, True),
                     rotations=(0, 1, 2, 3, 4, 5)):
        aspects = set()
        coord_list = ((0, 0, 0),) + units
        for flip in flips or (0,):
            for rotation in rotations or (0,):
                aspect = coordsys.Triangular3DView(
                    coord_list, rotation, 0, flip) # 0 is axis, ignored
                aspects.add(aspect)
        return aspects

    def format_solution(self, solution, normalized=True,
                        rotate_180=False, row_reversed=False, xy_swapped=False,
                        standardize=False):
        s_matrix = self.build_solution_matrix(solution)
        if rotate_180:
            s_matrix = [[list(reversed(s_matrix[z][y]))
                         for y in reversed(range(self.height))]
                        for z in reversed(range(self.depth))]
        # row_reversed doesn't work for triangular coordinates:
        if row_reversed:
            out = [[], []]
            trim = (self.height - 1) // 2
            for y in range(self.height):
                index = self.height - 1 - y
                for z in range(self.depth):
                    out[z].append(([self.empty_cell] * index
                                   + s_matrix[z][index]
                                   + [self.empty_cell] * y)[trim:-trim])
            s_matrix = out
        if xy_swapped:
            assert self.height == self.width, (
                'Unable to swap x & y: dimensions not equal!')
            s_matrix = [[[s_matrix[z][x][y]
                          for x in range(self.height)]
                         for y in range(self.width)]
                        for z in range(self.depth)]
        if standardize:
            s_matrix = self.standardize_solution_matrix(
                solution, s_matrix, piece_name=standardize)
        return self.format_triangular_grid(s_matrix)

    def standardize_solution_matrix(self, solution, s_matrix, piece_name):
        """
        Format the solution by rotating the puzzle so the named piece is in a
        standard position, for easy comparison.  In one-sided puzzles if the
        named piece is flipped (i.e. has a lowercase names), the puzzle is
        flipped first.
        """
        pieces = dict(
            (piece[-1], [tuple(int(d) for d in coord.split(','))
                         for coord in piece[:-1]])
            for piece in solution)
        coords = set(pieces[piece_name])
        target = set(self.pieces[piece_name.upper()][0][1])
        flip = piece_name != piece_name.upper()
        for rotation in range(6):
            new = coordsys.Triangular3DView(coords, rotation, flip=flip)
            if set(new) == target:
                break
        else:
            raise Exception(
                'unable to match rotation (%s, flip=%s)' % (piece_name, flip))
        if not rotation and not flip:
            return s_matrix
        for piece_name, coords in pieces.items():
            coord_set = coordsys.Triangular3DCoordSet(coords)
            if flip:
                coord_set = coord_set.flip0()
            coord_set = coord_set.rotate0(rotation)
            pieces[piece_name] = coord_set
        min_x = min(coord[0]
                    for piece_coords in pieces.values()
                    for coord in piece_coords)
        min_y = min(coord[1]
                    for piece_coords in pieces.values()
                    for coord in piece_coords)
        offset = coordsys.Triangular3D((-min_x, -min_y, 0))
        for piece_name, coords in pieces.items():
            pieces[piece_name] = coords.translate(offset)
        new_solution = [sorted(','.join(str(d) for d in coord)
                               for coord in pieces[piece[-1]]) + [piece[-1]]
                        for piece in solution]
        new_matrix = self.build_solution_matrix(new_solution)
        return new_matrix

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
        for the piece at (x,y,z).
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

    symmetric_pieces = 'E6 V6 X6 C6 O6'.split()
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
        '0': 'gray',
        '1': 'black'}


class Hexiamonds3x12(Hexiamonds):

    """0 solutions"""

    height = 3
    width = 12

    duplicate_conditions = ({'rotate_180': True},)


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


class Hexiamonds5x8StackedLongHexagons(Hexiamonds):

    """378 solutions"""

    height = 8
    width = 8

    duplicate_conditions = ({'rotate_180': True},)

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if 7 <= (2 * x + y + z) <= 15:
                        yield coordsys.Triangular3D((x, y, z))

    def customize_piece_data(self):
        self.piece_data['I6'][-1]['flips'] = None


class Hexiamonds4x12StackedHexagons(Hexiamonds):

    """51 solutions"""

    height = 12
    width = 8

    duplicate_conditions = ({'rotate_180': True},)

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    total = x + y + z
                    if (  (y < 4 and 4 <= x < 8 and 6 <= total < 10)
                          or (4 <= y < 8 and 2 <= x < 6 and 8 <= total < 12)
                          or (8 <= y and x < 4 and 10 <= total < 14)):
                        yield coordsys.Triangular3D((x, y, z))

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
                        yield coordsys.Triangular3D((x, y, z))


class Hexiamonds5x8StackedLongButterflies(Hexiamonds):

    """290 solutions"""

    height = 8
    width = 9

    duplicate_conditions = ({'rotate_180': True},)

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if 8 <= (2 * x + y + z) <= 16:
                        yield coordsys.Triangular3D((x, y, z))

    def customize_piece_data(self):
        self.piece_data['I6'][-1]['flips'] = None


class Hexiamonds4x12StackedButterflies(Hexiamonds):

    """26 solutions"""

    height = 12
    width = 10

    duplicate_conditions = ({'rotate_180': True},)

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    total = x + y + z
                    if (  (y < 2 and 6 <= x and total < 10)
                          or (2 <= y < 6 and 4 <= x < 8 and 8 <= total < 12)
                          or (6 <= y < 10 and 2 <= x < 6 and 10 <= total < 14)
                          or (10 <= y and x < 4 and 12 <= total)):
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


class HexiamondsIrregularHexagon7x8(Hexiamonds):

    """
    5885 solutions.

    Suggested by Dan Klarskov, Denmark, under the name 'hexui'.
    """

    height = 8
    width = 7

    check_for_duplicates = False

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if 1 < x + y + z < 9:
                        yield coordsys.Triangular3D((x, y, z))

    def customize_piece_data(self):
        self.piece_data['I6'][-1]['flips'] = None


class HexiamondsStackedChevrons_6x6(Hexiamonds):

    """
    933 solutions.

    Suggested by Dan Klarskov, Denmark, under the name 'polyam2'.
    """

    height = 6
    width = 9

    check_for_duplicates = False

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if self.height <= (2 * x + y + z) < (self.width * 2):
                        yield coordsys.Triangular3D((x, y, z))

    def customize_piece_data(self):
        self.piece_data['I6'][-1]['flips'] = None


class HexiamondsStackedChevrons_12x3_1(Hexiamonds):

    """269 solutions."""

    height = 12
    width = 9

    check_for_duplicates = False

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if 11 <= (2 * x + y + z) < 17:
                        yield coordsys.Triangular3D((x, y, z))

    def customize_piece_data(self):
        self.piece_data['I6'][-1]['flips'] = None


class HexiamondsStackedChevrons_12x3_2(Hexiamonds):

    """114 solutions."""

    height = 12
    width = 9

    check_for_duplicates = False

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
                        yield coordsys.Triangular3D((x, y, z))

    def customize_piece_data(self):
        self.piece_data['I6'][-1]['flips'] = None


class HexiamondsStackedChevrons_12x3_3(Hexiamonds):

    """46 solutions."""

    height = 12
    width = 9

    check_for_duplicates = False

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    total = x + y + z
                    if (  (y < 3 and 6 <= total < 9)
                          or (3 <= y < 6 and 3 <= x < 6)
                          or (6 <= y < 9 and 9 <= total < 12)
                          or (y >= 9 and x < 3)):
                        yield coordsys.Triangular3D((x, y, z))

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
                            yield coordsys.Triangular3D((x, y, z))
                    elif (self.height / 2 - 1) < (x + y + z) < self.width:
                        # bottom half
                        yield coordsys.Triangular3D((x, y, z))

    def customize_piece_data(self):
        self.piece_data['I6'][-1]['flips'] = None


class HexiamondsChevron_4x9(HexiamondsChevron):

    """142 solutions."""

    height = 4
    width = 11

    check_for_duplicates = False


class HexiamondsChevron_6x6(HexiamondsChevron):

    """1004 solutions."""

    height = 6
    width = 9

    check_for_duplicates = False


class HexiamondsChevron_12x3(HexiamondsChevron):

    """29 solutions."""

    height = 12
    width = 9

    check_for_duplicates = False


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
                        yield coordsys.Triangular3D((x, y, z))


class HexiamondsTenyo(Hexiamonds):

    """
     solutions.

    This is the puzzle that is sold by Tenyo Inc., Japan, in their `"PlaPuzzle"
    line`__ (`details`__).

    __ http://www.tenyo.co.jp/pp/
    __ http://www.tenyo.co.jp/pp/pz04/index.html
    """

    height = 8
    width = 7

    check_for_duplicates = False

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    xyz = x + y + z
                    if (  ((xyz > 4) or (x > 0 and xyz > 3))
                          and ((xyz < 9) or (x < 6 and xyz < 10)
                               or (x < 5 and xyz < 11))):
                        yield coordsys.Triangular3D((x, y, z))

    def customize_piece_data(self):
        self.piece_data['I6'][-1]['flips'] = None


class OneSidedHexiamonds(OneSidedLowercaseMixin, Hexiamonds):

    pass


class OneSidedHexiamondsOBeirnesHexagon(OneSidedHexiamonds):

    """
    124,519 solutions, agrees with Knuth.

    Split into 7 sub-puzzles by the distance of the small-hexagon piece (O6)
    from the center of the puzzle.

    O'Beirne's Hexagon consists of 19 small 6-triangle hexagons, arranged in a
    hexagon like a honeycomb (12 small hexagons around 6 around 1).
    """

    height = 10
    width = 10

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
                        yield coordsys.Triangular3D((x, y, z))

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
                        yield coordsys.Triangular3D((x, y, z))

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
                        yield coordsys.Triangular3D((x, y, z))


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
        '0': 'gray',
        '1': 'black'}


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
                        hole.add(coordsys.Triangular3D((x, y, z)))
        for coord in ((5,3,1), (8,3,0), (8,5,1), (6,8,0), (3,6,0), (3,8,1)):
            hole.remove(coord)
        for y in range(self.height):
            for x in range(self.width):
                for z in range(self.depth):
                    coord = coordsys.Triangular3D((x, y, z))
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
                    coord = coordsys.Triangular3D((x, y, z))
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
                    coord = coordsys.Triangular3D((x, y, z))
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
                    coord = coordsys.Triangular3D((x, y, z))
                    if 5 < x + y + z < 18 and coord not in hole:
                        yield coord


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
                for x in range(self.width):
                    if x < 3 or x > 6 or y < 3 or y > 6:
                        yield coordsys.Triangular3D((x, y, z))

    def customize_piece_data(self):
        self.piece_data['W7'][-1]['flips'] = None


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
                        yield coordsys.Triangular3D((x, y, z))

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
                            yield coordsys.Triangular3D((x, y, z))
                    elif (self.height / 2 - 1) < (x + y + z) < self.width:
                        # bottom half
                        yield coordsys.Triangular3D((x, y, z))

    def customize_piece_data(self):
        self.piece_data['W7'][-1]['flips'] = None


class Heptiamonds4x21Chevron(HeptiamondsChevron):

    """ solutions."""

    height = 4
    width = 23


class Heptiamonds6x14Chevron(HeptiamondsChevron):

    """ solutions."""

    height = 6
    width = 17


class Heptiamonds12x7Chevron(HeptiamondsChevron):

    """ solutions."""

    height = 12
    width = 13


class Heptiamonds14x6Chevron(HeptiamondsChevron):

    """ solutions."""

    height = 14
    width = 13


class Heptiamonds28x3Chevron(HeptiamondsChevron):

    """ solutions."""

    height = 28
    width = 17


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
                        yield coordsys.Triangular3D((x, y, z))

    def customize_piece_data(self):
        self.piece_data['W7'][-1]['flips'] = None


class Heptiamonds11x8Stack(HeptiamondsStack):

    height = 8
    width = 14


class Heptiamonds4x24Stack(HeptiamondsStack):

    height = 24
    width = 15


class HeptiamondsHexedTriangle(Heptiamonds):

    """many solutions"""

    height = 14
    width = 14

    check_for_duplicates = False

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if ( (x + 2 * y + z >= 13)
                         and (y - x <= 7)
                         and (2 * x + y + z <= 27)):
                        yield coordsys.Triangular3D((x, y, z))


class HeptiamondsShortHexRing(Heptiamonds):

    """
    many solutions.

    2x8 short hexagon with central 2-unit hexagon hole.
    """

    height = 10
    width = 10

    duplicate_conditions = ({'rotate_180': True},)

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    total = x + y + z
                    if (  (1 < total < 18)
                          and (total < 8 or total > 11
                               or x < 3 or x > 6 or y < 3 or y > 6)):
                        yield coordsys.Triangular3D((x, y, z))


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
                        yield coordsys.Triangular3D((x, y, z))


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
                        yield coordsys.Triangular3D((x, y, z))


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
                        yield coordsys.Triangular3D((x, y, z))


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

     solutions.
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
                    yield coordsys.Triangular3D((x, y, z))


if __name__ == '__main__':
    p = Pentominoes6x10()
    print 'matrix length =', len(p.matrix)
    print 'first 20 rows:'
    pprint(p.matrix[:20], width=720)
