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
import collections

from puzzler import coordsys
from puzzler.puzzles import Puzzle2D, OneSidedLowercaseMixin


class Polyhexes(Puzzle2D):

    """
    The shape of the matrix is defined by the `coordinates` generator method.
    The `width` and `height` attributes define the maximum bounds only.
    """

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
    def coordinates_staggered_rectangle(cls, width, height, offset=None):
        for x in range(width):
            y_offset = int((width - x - 1) / 2)
            for y in range(height):
                yield cls.coordinate_offset(x, y + y_offset, offset)

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
    def coordinates_semiregular_hexagon(cls, base_length, side_length,
                                        offset=None):
        bound =  base_length + side_length - 1
        min_xy = side_length - 1
        max_xy = base_length + 2 * side_length - 3
        for coord in cls.coordinates_parallelogram(bound, bound):
            x, y = coord
            if min_xy <= (x + y) <= max_xy:
                yield cls.coordinate_offset(x, y, offset)

    # old name:
    coordinates_semi_regular_hexagon = coordinates_semiregular_hexagon

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
    def coordinates_inverted_triangle(cls, side_length, offset=None):
        coords = set(cls.coordinates_parallelogram(
            side_length + 1, side_length, offset=offset))
        coords -= set(cls.coordinates_triangle(side_length, offset=offset))
        return sorted(coords)

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
            if (xy >= min_xy or y >= min_y) and (xy <= max_xy or y <= max_y):
                yield cls.coordinate_offset(x, y, offset)

    def make_aspects(self, units, flips=(False, True),
                     rotations=(0, 1, 2, 3, 4, 5), implied_0=True):
        aspects = set()
        if implied_0:
            coord_list = ((0, 0),) + units
        else:
            coord_list = tuple(units)
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

    def build_svg_shape(self, s_matrix, x, y):
        """
        Return an SVG shape definition for the shape at (x,y), and erase the
        shape from s_matrix.
        """
        name = s_matrix[y][x]
        color = self.piece_colors[name]
        cells = self.get_piece_cells(s_matrix, x, y)
        path_points = self.get_path_points(cells)
        # Erase cells of this piece:
        for x, y in cells:
            s_matrix[y][x] = self.empty_cell
        path_strings = [
            ('M %.3f,%.3f %s Z'
             % (points[0][0], points[0][1],
                ' '.join(('L %.3f,%.3f' % coord) for coord in points[1:])))
            for points in path_points]
        return self.svg_path % {
            'color': color,
            'stroke': self.svg_stroke,
            'stroke_width': self.svg_stroke_width,
            'path_data': ' '.join(path_strings),
            'name': name}

    _sqrt3 = math.sqrt(3)
    corner_offsets = {0: (0.0, 1 / _sqrt3),
                      1: (0.0, 0.0),
                      2: (0.5, -_sqrt3 / 6),
                      3: (1.0, 0.0),
                      4: (1.0, 1 / _sqrt3),
                      5: (0.5, _sqrt3 / 2)}
    """Offset of corners from the lower left-hand corner of hexagon."""

    def get_path_points(self, cells):
        """
        Return a list of paths, each a list of closed path points.

        The first path is the main shape outline, and subsequent subpaths (if
        any) are holes.
        """
        # This version allows for shapes with holes.  It works for polyhexes,
        # but doesn't take into account multiple path choices that would occur
        # for polyiamonds and polyominoes (e.g.  heptomino with a hole).
        segments = set()
        segment_starts = collections.defaultdict(set)
        for cell in cells:
            for segment in self.get_path_segments(cell):
                start, end = segment
                reverse = (end, start)
                if reverse in segments:
                    # two cells are adjacent; segments cancel each other out
                    segments.remove(reverse)
                    segment_starts[end].remove(start)
                else:
                    segments.add(segment)
                    segment_starts[start].add(end)
        # Join the remaining segments into (potentially multiple) paths.
        paths = []
        while segments:
            # arbitrary starting point, should be outermost path:
            segment = min(segments)
            segments.remove(segment)
            start, end = segment
            path = [start, end]
            # keep track of start point, to know when to stop:
            first = start
            while True:
                start = end
                # not true for polyominoes & polyiamonds with holes at edge:
                assert len(segment_starts[start]) == 1
                end = segment_starts[start].pop()
                segment = (start, end)
                segments.remove(segment)
                if end == first:
                    break
                else:
                    path.append(end)
            paths.append(path)
        return paths

    def get_path_segments(self, cell):
        """
        Return a list of (start,end) pairs of coordinate tuples for edge
        segments of the cell at (x,y), counterclockwise.
        """
        x, y = cell
        unit = self.svg_unit_length
        yunit = self.svg_unit_height
        height = (self.height + 2) * yunit
        base_x = (x + (y - 1) / 2.0) * unit
        base_y = height - y * yunit
        corners = len(self.corner_offsets)
        segments = []
        start = None
        for i in range(corners + 1):
            end = (
                round(base_x + self.corner_offsets[i % corners][0] * unit, 6),
                round(base_y - self.corner_offsets[i % corners][1] * unit, 6))
            if start:
                segments.append((start, end))
            start = end
        return segments


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

    symmetric_pieces = (
        Trihexes.symmetric_pieces + Tetrahexes.symmetric_pieces)

    asymmetric_pieces = (
        Trihexes.asymmetric_pieces + Tetrahexes.asymmetric_pieces)

    piece_colors = copy.deepcopy(Tetrahexes.piece_colors)
    piece_colors.update(Trihexes.piece_colors)


class OneSidedPolyhexes34(OneSidedLowercaseMixin, Polyhexes34):

    pass


class Polyhexes1234(Polyhexes34):

    piece_data = copy.deepcopy(Polyhexes34.piece_data)
    piece_data.update(copy.deepcopy(Monohex.piece_data))
    piece_data.update(copy.deepcopy(Dihex.piece_data))

    symmetric_pieces = (
        Monohex.symmetric_pieces + Dihex.symmetric_pieces
        + Polyhexes34.symmetric_pieces)

    asymmetric_pieces = (
        Monohex.asymmetric_pieces + Dihex.asymmetric_pieces
        + Polyhexes34.asymmetric_pieces)

    piece_colors = copy.deepcopy(Polyhexes34.piece_colors)
    piece_colors.update(Monohex.piece_colors)
    piece_colors.update(Dihex.piece_colors)


class OneSidedPolyhexes1234(OneSidedLowercaseMixin, Polyhexes1234):

    pass


class Pentahexes(Polyhexes):

    piece_data = {
        'A5': ((( 1, 0), ( 2, 0), ( 1, 1), ( 2,-1)), {}),
        'B5': ((( 1, 0), ( 2, 0), ( 1, 1), ( 2, 1)), {}),
        'C5': ((( 1, 0), ( 2, 0), ( 2, 1), (-1, 1)), {}),
        'D5': ((( 1, 0), ( 2, 0), ( 0, 1), ( 1, 1)), {}),
        'E5': ((( 1, 0), ( 1, 1), ( 2, 0), ( 3, 0)), {}),
        'F5': ((( 1, 0), ( 2, 0), ( 0, 1), ( 2, 1)), {}),
        'G5': ((( 1, 0), ( 1, 1), ( 2, 1), ( 3, 0)), {}),
        'H5': ((( 1, 0), ( 1, 1), ( 0, 2), ( 2, 1)), {}),
        'I5': ((( 1, 0), ( 2, 0), ( 3, 0), ( 4, 0)), {}),
        'J5': ((( 1, 0), ( 2, 0), ( 3, 0), ( 3, 1)), {}),
        'L5': ((( 1, 0), ( 2, 0), ( 2, 1), ( 2, 2)), {}),
        'N5': ((( 1, 0), ( 2, 0), ( 2, 1), ( 3, 1)), {}),
        'P5': ((( 1, 0), ( 2, 0), ( 2, 1), ( 3, 0)), {}),
        'Q5': ((( 1, 0), ( 2, 0), ( 2, 1), ( 1,-1)), {}),
        'R5': ((( 1, 0), ( 2, 0), ( 2, 1), ( 1, 2)), {}),
        'S5': ((( 1, 0), ( 2, 0), ( 2, 1), ( 0,-1)), {}),
        'T5': ((( 1, 0), ( 2, 0), ( 2, 1), ( 2,-1)), {}),
        'U5': ((( 1, 0), ( 1, 1), (-1, 1), (-1, 2)), {}),
        'V5': ((( 1, 0), ( 2, 0), ( 0, 1), ( 0, 2)), {}),
        'W5': ((( 1, 0), ( 1, 1), ( 2, 1), ( 2, 2)), {}),
        'X5': ((( 1, 0), ( 2, 0), ( 0, 1), ( 2,-1)), {}),
        'Y5': ((( 1, 0), ( 2, 0), ( 2, 1), ( 3,-1)), {}),}
    """(0,0) is implied."""

    symmetric_pieces = 'I5 E5 L5 C5 Y5 D5 X5 A5 V5 U5 W5'.split()
    """Pieces with reflexive symmetry, identical to their mirror images."""

    asymmetric_pieces = 'J5 P5 N5 R5 B5 F5 S5 Q5 T5 H5 G5'.split()
    """Pieces without reflexive symmetry, different from their mirror images."""

    piece_colors = {
        'A5': 'maroon',
        'B5': 'steelblue',
        'C5': 'lime',
        'D5': 'green',
        'E5': 'magenta',
        'F5': 'lightcoral',
        'G5': 'indigo',
        'H5': 'tan',
        'I5': 'blue',
        'J5': 'darkseagreen',
        'L5': 'darkorange',
        'N5': 'plum',
        'P5': 'peru',
        'Q5': 'olive',
        'R5': 'yellow',
        'S5': 'gray',
        'T5': 'teal',
        'U5': 'navy',
        'V5': 'blueviolet',
        'W5': 'gold',
        'X5': 'red',
        'Y5': 'turquoise',
        '0': 'gray',
        '1': 'black'}


class OneSidedPentahexes(OneSidedLowercaseMixin, Pentahexes):

    pass


class Polyhexes12345(Polyhexes1234, Pentahexes):

    piece_data = copy.deepcopy(Pentahexes.piece_data)
    piece_data.update(copy.deepcopy(Polyhexes1234.piece_data))

    symmetric_pieces = (
        Polyhexes1234.symmetric_pieces + Pentahexes.symmetric_pieces)

    asymmetric_pieces = (
        Polyhexes1234.asymmetric_pieces + Pentahexes.asymmetric_pieces)

    piece_colors = copy.deepcopy(Pentahexes.piece_colors)
    piece_colors.update(Polyhexes1234.piece_colors)


class OneSidedPolyhexes12345(OneSidedLowercaseMixin, Polyhexes12345):

    pass


class Hexahexes(Polyhexes):

    implied_0 = False

    piece_data = {
        'A06': (((0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (2, 0)), {}),
        'A16': (((0, 0), (0, 1), (0, 2), (1, 1), (1, 2), (2, 0)), {}),
        'A26': (((0, 0), (0, 1), (0, 2), (1, 1), (2, 0), (2, 1)), {}),
        'C06': (((0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0)), {}),
        'C16': (((0, 0), (0, 1), (1, 1), (2, 1), (3, 1), (4, 0)), {}),
        'C26': (((0, 1), (0, 2), (0, 3), (1, 0), (1, 3), (2, 0)), {}),
        'C36': (((0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 1)), {}),
        'C46': (((0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0)), {}),
        'C56': (((0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (1, 3)), {}),
        'C66': (((0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (3, 1)), {}),
        'C76': (((0, 1), (0, 2), (1, 0), (1, 2), (1, 3), (2, 0)), {}),
        'E06': (((0, 0), (0, 1), (0, 2), (1, 1), (1, 2), (2, 2)), {}),
        'F06': (((0, 0), (0, 1), (0, 2), (0, 3), (1, 1), (1, 3)), {}),
        'F16': (((0, 0), (0, 1), (1, 1), (1, 2), (2, 1), (3, 1)), {}),
        'H06': (((0, 0), (0, 1), (0, 2), (0, 3), (1, 2), (2, 2)), {}),
        'H16': (((0, 0), (0, 1), (1, 1), (1, 2), (1, 3), (2, 0)), {}),
        'H26': (((0, 0), (0, 1), (1, 1), (1, 2), (1, 3), (2, 1)), {}),
        'I06': (((0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5)), {}),
        'J06': (((0, 0), (0, 1), (0, 2), (0, 3), (1, 3), (2, 2)), {}),
        'J16': (((0, 0), (0, 1), (0, 2), (1, 2), (2, 0), (2, 1)), {}),
        'J26': (((0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 2)), {}),
        'J36': (((0, 0), (0, 1), (1, 1), (1, 3), (2, 1), (2, 2)), {}),
        'J46': (((0, 1), (0, 2), (0, 3), (1, 0), (1, 2), (2, 2)), {}),
        'K06': (((0, 1), (0, 2), (1, 1), (2, 1), (2, 2), (3, 0)), {}),
        'L06': (((0, 0), (0, 1), (0, 2), (0, 3), (1, 3), (2, 3)), {}),
        'L16': (((0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 4)), {}),
        'L26': (((0, 0), (0, 1), (0, 2), (1, 2), (2, 1), (3, 1)), {}),
        'L36': (((0, 0), (0, 1), (0, 2), (1, 1), (2, 1), (3, 0)), {}),
        'M06': (((0, 0), (0, 1), (1, 1), (1, 2), (1, 3), (2, 2)), {}),
        'M16': (((0, 0), (0, 1), (0, 3), (1, 1), (1, 2), (2, 2)), {}),
        'M26': (((0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (2, 1)), {}),
        'M36': (((0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)), {}),
        'M46': (((0, 0), (0, 1), (1, 1), (1, 2), (2, 2), (2, 3)), {}),
        'N06': (((0, 0), (0, 1), (0, 2), (1, 2), (1, 3), (1, 4)), {}),
        'N16': (((0, 0), (0, 1), (0, 2), (0, 3), (1, 3), (1, 4)), {}),
        'O06': (((0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1)), {}),
        'P06': (((0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (1, 1)), {}),
        'P16': (((0, 0), (0, 1), (0, 2), (0, 4), (1, 2), (1, 3)), {}),
        'P26': (((0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 0)), {}),
        'P36': (((0, 0), (0, 1), (0, 4), (1, 1), (1, 2), (1, 3)), {}),
        'P46': (((0, 0), (0, 1), (0, 2), (1, 1), (2, 0), (3, 0)), {}),
        'P56': (((0, 0), (0, 1), (0, 2), (0, 3), (1, 2), (1, 3)), {}),
        'P66': (((0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 1)), {}),
        'P76': (((0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (1, 3)), {}),
        'Q06': (((0, 0), (0, 1), (1, 1), (2, 1), (2, 2), (3, 1)), {}),
        'Q16': (((0, 0), (0, 1), (0, 2), (1, 2), (1, 3), (2, 2)), {}),
        'Q26': (((0, 1), (0, 2), (1, 0), (1, 2), (1, 3), (2, 2)), {}),
        'Q36': (((0, 0), (0, 1), (1, 0), (1, 1), (1, 2), (2, 2)), {}),
        'R06': (((0, 0), (0, 1), (0, 3), (1, 1), (1, 2), (2, 0)), {}),
        'R16': (((0, 1), (0, 2), (1, 0), (1, 2), (1, 3), (2, 1)), {}),
        'S06': (((0, 0), (0, 1), (1, 1), (2, 0), (3, 0), (3, 1)), {}),
        'S16': (((0, 0), (0, 1), (1, 1), (2, 1), (3, 1), (3, 2)), {}),
        'S26': (((0, 0), (0, 1), (0, 2), (1, 1), (1, 2), (1, 3)), {}),
        'S36': (((0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (2, 3)), {}),
        'T06': (((0, 0), (0, 1), (1, 1), (1, 2), (2, 0), (2, 2)), {}),
        'T16': (((0, 1), (0, 2), (1, 0), (1, 1), (2, 1), (3, 1)), {}),
        'T26': (((0, 1), (0, 2), (1, 2), (1, 3), (2, 1), (3, 0)), {}),
        'T36': (((0, 0), (0, 1), (0, 3), (1, 0), (1, 1), (1, 2)), {}),
        'T46': (((0, 0), (0, 1), (0, 2), (1, 1), (2, 1), (3, 1)), {}),
        'T56': (((0, 0), (0, 1), (1, 0), (1, 1), (1, 2), (2, 1)), {}),
        'T66': (((0, 0), (0, 1), (1, 1), (1, 2), (2, 0), (2, 1)), {}),
        'T76': (((0, 1), (0, 2), (1, 1), (1, 2), (1, 3), (2, 0)), {}),
        'U06': (((0, 0), (0, 1), (0, 3), (0, 4), (1, 1), (1, 2)), {}),
        'U16': (((0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (1, 2)), {}),
        'U26': (((0, 0), (0, 1), (0, 2), (1, 1), (2, 1), (2, 2)), {}),
        'V06': (((0, 0), (0, 1), (0, 2), (1, 2), (2, 1), (3, 0)), {}),
        'V16': (((0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (2, 0)), {}),
        'W06': (((0, 0), (0, 1), (1, 1), (1, 2), (2, 2), (3, 1)), {}),
        'W16': (((0, 0), (0, 1), (0, 2), (1, 2), (1, 3), (2, 3)), {}),
        'W26': (((0, 0), (0, 1), (0, 2), (1, 1), (1, 2), (2, 1)), {}),
        'W36': (((0, 0), (0, 1), (1, 1), (1, 2), (1, 3), (2, 3)), {}),
        'X06': (((0, 1), (0, 3), (1, 1), (1, 2), (2, 0), (2, 2)), {}),
        'X16': (((0, 1), (1, 1), (1, 2), (2, 0), (2, 1), (3, 1)), {}),
        'X26': (((0, 1), (0, 2), (1, 1), (2, 0), (2, 1), (3, 1)), {}),
        'Y06': (((0, 1), (0, 2), (1, 2), (1, 3), (2, 0), (2, 1)), {}),
        'Y16': (((0, 1), (1, 1), (2, 1), (2, 2), (2, 3), (3, 0)), {}),
        'Y26': (((0, 1), (1, 1), (1, 2), (1, 3), (1, 4), (2, 0)), {}),
        'Y36': (((0, 0), (0, 1), (0, 2), (0, 3), (1, 1), (2, 0)), {}),
        'Y46': (((0, 0), (0, 1), (1, 1), (2, 1), (2, 2), (3, 0)), {}),
        'Y56': (((0, 0), (0, 1), (0, 2), (1, 2), (1, 3), (2, 1)), {}),
        'Y66': (((0, 1), (1, 1), (1, 2), (1, 3), (2, 1), (3, 0)), {}),
        'Z06': (((0, 1), (0, 2), (1, 1), (2, 1), (3, 0), (3, 1)), {}),
        }
    """(0,0) is NOT implied."""
    for _name in list(piece_data):
        piece_data[_name][-1]['implied_0'] = False
    del _name

    symmetric_pieces = (
        'A06 C06 C16 E06 I06 O06 T06 T16 T56 U06 U16 V06 X06 X16 Y06 Y16 Y26'
        .split())
    """Pieces with reflexive symmetry, identical to their mirror images."""

    asymmetric_pieces = (
        'A16 A26 C26 C36 C46 C56 C66 C76 F06 F16 H06 H16 H26 J06 J16 J26 '
        'J36 J46 K06 L06 L16 L26 L36 M06 M16 M26 M36 M46 N06 N16 P06 P16 '
        'P26 P36 P46 P56 P66 P76 Q06 Q16 Q26 Q36 R06 R16 S06 S16 S26 S36 '
        'T26 T36 T46 T66 T76 U26 V16 W06 W16 W26 W36 X26 Y36 Y46 Y56 Y66 Z06'
        .split())
    """Pieces without reflexive symmetry, different from their mirror images."""

    piece_colors = {
        # a selection of colors, repeating:
        'A06': 'maroon',
        'A16': 'steelblue',
        'A26': 'lime',
        'C06': 'green',
        'C16': 'magenta',
        'C26': 'indigo',
        'C36': 'blue',
        'C46': 'darkseagreen',
        'C56': 'darkorange',
        'C66': 'plum',
        'C76': 'peru',
        'E06': 'olive',
        'F06': 'teal',
        'F16': 'navy',
        'H06': 'blueviolet',
        'H16': 'red',
        'H26': 'turquoise',
        'I06': 'maroon',
        'J06': 'steelblue',
        'J16': 'lime',
        'J26': 'green',
        'J36': 'magenta',
        'J46': 'indigo',
        'K06': 'blue',
        'L06': 'darkseagreen',
        'L16': 'darkorange',
        'L26': 'plum',
        'L36': 'peru',
        'M06': 'olive',
        'M16': 'teal',
        'M26': 'navy',
        'M36': 'blueviolet',
        'M46': 'red',
        'N06': 'turquoise',
        'N16': 'maroon',
        'O06': 'steelblue',
        'P06': 'lime',
        'P16': 'green',
        'P26': 'magenta',
        'P36': 'indigo',
        'P46': 'blue',
        'P56': 'darkseagreen',
        'P66': 'darkorange',
        'P76': 'plum',
        'Q06': 'peru',
        'Q16': 'olive',
        'Q26': 'teal',
        'Q36': 'navy',
        'R06': 'blueviolet',
        'R16': 'red',
        'S06': 'turquoise',
        'S16': 'maroon',
        'S26': 'steelblue',
        'S36': 'lime',
        'T06': 'green',
        'T16': 'magenta',
        'T26': 'indigo',
        'T36': 'blue',
        'T46': 'darkseagreen',
        'T56': 'darkorange',
        'T66': 'plum',
        'T76': 'peru',
        'U06': 'olive',
        'U16': 'teal',
        'U26': 'navy',
        'V06': 'blueviolet',
        'V16': 'red',
        'W06': 'turquoise',
        'W16': 'maroon',
        'W26': 'steelblue',
        'W36': 'lime',
        'X06': 'green',
        'X16': 'magenta',
        'X26': 'indigo',
        'Y06': 'blue',
        'Y16': 'darkseagreen',
        'Y26': 'darkorange',
        'Y36': 'plum',
        'Y46': 'peru',
        'Y56': 'olive',
        'Y66': 'teal',
        'Z06': 'navy',}


class OneSidedHexahexes(OneSidedLowercaseMixin, Hexahexes):

    pass


class Polyhexes123456(Polyhexes12345, Hexahexes):

    piece_data = copy.deepcopy(Hexahexes.piece_data)
    piece_data.update(copy.deepcopy(Polyhexes12345.piece_data))

    symmetric_pieces = (
        Polyhexes12345.symmetric_pieces + Hexahexes.symmetric_pieces)

    asymmetric_pieces = (
        Polyhexes12345.asymmetric_pieces + Hexahexes.asymmetric_pieces)

    piece_colors = copy.deepcopy(Hexahexes.piece_colors)
    piece_colors.update(Polyhexes12345.piece_colors)


class OneSidedPolyhexes123456(OneSidedLowercaseMixin, Polyhexes123456):

    pass
