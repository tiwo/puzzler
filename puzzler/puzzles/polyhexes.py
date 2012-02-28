#!/usr/bin/env python
# $Id$

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2012 by David J. Goodger
# License: GPL 2 (see __init__.py)

"""
Polyhex puzzle base classes.
"""

import copy
import math

from puzzler import coordsys
from puzzler.puzzles import Puzzle2D, OneSidedLowercaseMixin


class Polyhexes(Puzzle2D):

    """
    The shape of the matrix is defined by the `coordinates` generator method.
    The `width` and `height` attributes define the maximum bounds only.
    """

    check_for_duplicates = True

    duplicate_conditions = ()

    svg_unit_height = Puzzle2D.svg_unit_length * math.sqrt(3) / 2

    coord_class = coordsys.Hexagonal2D

    def coordinates(self):
        return self.coordinates_parallelogram(self.width, self.height)

    @classmethod
    def coordinates_parallelogram(cls, width, height, offset=None):
        for y in range(height):
            for x in range(width):
                yield cls.coordinate_offset(x, y, offset)

    @classmethod
    def coordinate_offset(cls, x, y, offset):
        if offset:
            return coordsys.Hexagonal2D((x, y)) + offset
        else:
            return coordsys.Hexagonal2D((x, y))

    @classmethod
    def coordinates_hexagon(cls, side_length, offset=None):
        bound = side_length * 2 - 1
        min_xy = side_length - 1
        max_xy = 3 * side_length - 3
        for coord in cls.coordinates_parallelogram(bound, bound):
            x, y = coord
            if min_xy <= (x + y) <= max_xy:
                yield cls.coordinate_offset(x, y, offset)

    @classmethod
    def coordinates_elongated_hexagon(cls, base_length, side_length,
                                      offset=None):
        x_bound = side_length + base_length - 1
        y_bound = 2 * side_length - 1
        min_xy = side_length - 1
        max_xy = base_length + 2 * side_length - 3
        for coord in cls.coordinates_parallelogram(x_bound, y_bound):
            x, y = coord
            if min_xy <= (x + y) <= max_xy:
                yield cls.coordinate_offset(x, y, offset)

    @classmethod
    def coordinates_hexagram(cls, side_length, offset=None):
        bound = (side_length - 1) * 4 + 1
        min_x = min_y = side_length - 1
        max_x = max_y = (side_length - 1) * 3
        min_xy = (side_length - 1) * 3
        max_xy = (side_length - 1) * 5
        for coord in cls.coordinates_parallelogram(bound, bound):
            x, y = coord
            xy = x + y
            if (  (min_xy <= xy and y <= max_y and x <= max_x)
                  or (xy <= max_xy and y >= min_y and x >= min_x)):
                yield cls.coordinate_offset(x, y, offset)

    @classmethod
    def coordinates_trapezoid(cls, base_length, side_length, offset=None):
        max_xy = base_length - 1
        for coord in cls.coordinates_parallelogram(base_length, side_length):
            x, y = coord
            if (x + y) <= max_xy:
                yield cls.coordinate_offset(x, y, offset)

    @classmethod
    def coordinates_triangle(cls, side_length, offset=None):
        return cls.coordinates_trapezoid(side_length, side_length, offset)

    @classmethod
    def coordinates_butterfly(cls, base_length, side_length, offset=None):
        """
        The base_length is actually the figure height (vertical length), and
        the side_length is the length of the four angled sides.
        """
        x_bound = side_length * 2 - 1
        y_bound = base_length + side_length - 1
        min_y = side_length - 1
        max_y = base_length - 1
        min_xy = x_bound - 1
        max_xy = y_bound - 1
        for coord in cls.coordinates_parallelogram(x_bound, y_bound):
            x, y = coord
            xy = x + y
            if ((xy >= min_xy) or (y >= min_y)) and ((xy <= max_xy) or (y <= max_y)):
                yield cls.coordinate_offset(x, y, offset)

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

    def calculate_svg_dimensions(self):
        height = (self.height + 2) * self.svg_unit_height
        width = (self.width + self.height / 2.0 + 2) * self.svg_unit_width
        return height, width

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


class Monohex(Polyhexes):

    piece_data = {'H1': ((), {})}
    """(0,0) is implied."""

    symmetric_pieces = piece_data.keys() # all of them

    asymmetric_pieces = []

    piece_colors = {'H1': 'gray'}


class Dihex(Polyhexes):

    piece_data = {'I2': ((( 1, 0),), {})}
    """(0,0) is implied."""

    symmetric_pieces = piece_data.keys() # all of them

    asymmetric_pieces = []

    piece_colors = {'I2': 'steelblue'}


class Trihexes(Polyhexes):

    piece_data = {
        'I3': ((( 1, 0), ( 2, 0)), {}),
        'V3': ((( 1, 0), ( 1, 1)), {}),
        'A3': ((( 1, 0), ( 0, 1)), {}),}
    """(0,0) is implied."""

    symmetric_pieces = piece_data.keys() # all of them

    asymmetric_pieces = []

    piece_colors = {
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


class Polyhexes34(Tetrahexes):

    piece_data = copy.deepcopy(Tetrahexes.piece_data)
    piece_data.update(copy.deepcopy(Trihexes.piece_data))

    symmetric_pieces = (Trihexes.symmetric_pieces
                        + Tetrahexes.symmetric_pieces)

    asymmetric_pieces = (Trihexes.asymmetric_pieces
                         + Tetrahexes.asymmetric_pieces)

    piece_colors = copy.deepcopy(Tetrahexes.piece_colors)
    piece_colors.update(Trihexes.piece_colors)

    check_for_duplicates = False


class Polyhex1234(Polyhexes34):

    piece_data = copy.deepcopy(Polyhexes34.piece_data)
    piece_data.update(copy.deepcopy(Monohex.piece_data))
    piece_data.update(copy.deepcopy(Dihex.piece_data))

    symmetric_pieces = (Monohex.symmetric_pieces + Dihex.symmetric_pieces
                        + Polyhexes34.symmetric_pieces)

    asymmetric_pieces = (Monohex.asymmetric_pieces + Dihex.asymmetric_pieces
                         + Polyhexes34.asymmetric_pieces)

    piece_colors = copy.deepcopy(Polyhexes34.piece_colors)
    piece_colors.update(Monohex.piece_colors)
    piece_colors.update(Dihex.piece_colors)

    check_for_duplicates = False


class OneSidedPolyhexes1234(OneSidedLowercaseMixin, Polyhex1234):

    pass


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

    piece_data = copy.deepcopy(Pentahexes.piece_data)
    piece_data.update(copy.deepcopy(Polyhex1234.piece_data))

    symmetric_pieces = (Polyhex1234.symmetric_pieces
                        + Pentahexes.symmetric_pieces)

    asymmetric_pieces = (Polyhex1234.asymmetric_pieces
                         + Pentahexes.asymmetric_pieces)

    piece_colors = copy.deepcopy(Pentahexes.piece_colors)
    piece_colors.update(Polyhex1234.piece_colors)
