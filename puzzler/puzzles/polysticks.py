#!/usr/bin/env python
# $Id$

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2012 by David J. Goodger
# License: GPL 2 (see __init__.py)

"""
Polystick puzzle base classes.
"""

import copy

from puzzler import coordsys
from puzzler.puzzles import PuzzlePseudo3D, OneSidedLowercaseMixin


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

    def format_svg_shapes(self, s_matrix):
        paths = []
        for x in range(1, self.width + 1):
            for y in range(1, self.height + 1):
                for z in range(self.depth):
                    if s_matrix[z][y][x] == self.empty_cell:
                        continue
                    paths.append(self.build_path(s_matrix, x, y, z))
        return paths

    def calculate_svg_dimensions(self):
        height = (self.height + 1) * self.svg_unit_height
        width = (self.width + 1) * self.svg_unit_width
        return height, width

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


class OneSidedTetrasticks(OneSidedLowercaseMixin, Tetrasticks):

    pass


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


class Polysticks1234(Tetrasticks, Polysticks123Data):

    piece_data = copy.deepcopy(Tetrasticks.piece_data)
    piece_data.update(copy.deepcopy(Polysticks123Data.piece_data))
    piece_colors = copy.deepcopy(Tetrasticks.piece_colors)
    piece_colors.update(Polysticks123Data.piece_colors)
