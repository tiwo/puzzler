#!/usr/bin/env python
# -*- coding: utf-8 -*-
# $Id$

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2015 by David J. Goodger
# License: GPL 2 (see __init__.py)

"""
Polytwig puzzle base classes.
"""

import copy
import math
import collections

from puzzler import coordsys
from puzzler.puzzles import OneSidedLowercaseMixin, PuzzlePseudo3D
from puzzler.puzzles.polytrigs import Polytrigs


class Polytwigs(Polytrigs):

    """
    'Polytwigs' == hexagonal-grid polysticks, because they look like twigs.
    """

    # line segment orientation (horizontal/right=0, 120deg=1, 240deg=2):
    depth = 3

    # most puzzles are slanted 30°ccw and require correction;
    # those that aren't will specify 0°
    svg_rotation = 30

    svg_stroke_width = '2'
    """Width of line segments."""

    svg_line_deltas = (
        # z == 0:
        (Polytrigs.svg_unit_length, 0),
        # z == 1:
        (-Polytrigs.svg_unit_length / 2.0,
         -Polytrigs.svg_unit_length * math.sqrt(3) / 2.0),
        # z == 2:
        (-Polytrigs.svg_unit_length / 2.0,
         Polytrigs.svg_unit_length * math.sqrt(3) / 2.0))

    svg_unit_width = Polytrigs.svg_unit_length * 1.5

    svg_unit_height = Polytrigs.svg_unit_length * math.sqrt(3)

    def coordinates(self):
        """
        Return coordinates for a typical parallelogram polytwig puzzle.
        """
        return self.coordinates_bordered(self.width - 1, self.height - 1)

    @classmethod
    def coordinate_offset(cls, x, y, z, offset):
        if offset:
            return coordsys.HexagonalGrid3D((x, y, z)) + offset
        else:
            return coordsys.HexagonalGrid3D((x, y, z))

    @classmethod
    def coordinates_bordered(cls, m, n, offset=None):
        """
        Bordered parallelogram polytwig grid of side length M & N hexagons.

        **NOTE:** Puzzle length & width must include edges, typically M+1 x
        N+1.
        """
        last_x = m
        last_y = n
        for y in range(n + 1):
            for x in range(m + 1):
                for z in range(cls.depth):
                    if z == 2 and y == 0 and x == 0:
                        continue
                    if (z == 1 and y == last_y) or (z == 0 and x == last_x):
                        continue
                    if x == last_x and y == last_y:
                        continue
                    yield cls.coordinate_offset(x, y, z, offset)

    @classmethod
    def coordinates_unbordered(cls, m, n, offset=None):
        """
        Unbordered parallelogram polytwig grid of side length M & N hexagons.
        """
        for coord in cls.coordinates_bordered(m, n):
            x, y, z = coord
            if (y == 0 and z != 1) or (x == 0 and z != 0) or y == n or x == m:
                continue
            yield cls.coordinate_offset(x, y, z, offset)

    @classmethod
    def coordinates_hexagon(cls, side_length, offset=None):
        """Hexagonal bordered polytwig grid."""
        min_xy = side_length - 1
        max_xy = 3 * side_length - 2
        bound = 2 * side_length - 1
        for coord in cls.coordinates_bordered(bound, bound):
            x, y, z = coord
            xy = x + y
            if (xy < min_xy) or ((xy == min_xy) and (z == 2)) or (xy > max_xy):
                continue
            yield cls.coordinate_offset(x, y, z, offset)

    @classmethod
    def coordinates_hexagon_unbordered(cls, side_length, offset=None):
        min_xy = side_length - 1
        max_xy = 3 * side_length - 2
        bound = 2 * side_length - 1
        for coord in cls.coordinates_unbordered(bound, bound):
            x, y, z = coord
            xy = x + y
            if (xy <= min_xy) or (xy == max_xy and z != 2) or (xy > max_xy):
                continue
            yield cls.coordinate_offset(x, y, z, offset)

    @classmethod
    def coordinates_elongated_hexagon(cls, base_length, side_length,
                                      offset=None):
        x_bound = side_length + base_length - 1
        y_bound = side_length * 2 - 1
        min_xy = side_length - 1
        max_xy = base_length + 2 * side_length - 2
        for coord in cls.coordinates_bordered(x_bound, y_bound):
            x, y, z = coord
            xy = x + y
            if (xy < min_xy) or ((xy == min_xy) and (z == 2)) or (xy > max_xy):
                continue
            yield cls.coordinate_offset(x, y, z, offset)

    @classmethod
    def coordinates_elongated_hexagon_unbordered(
            cls, base_length, side_length, offset=None):
        x_bound = side_length + base_length - 1
        y_bound = side_length * 2 - 1
        min_xy = side_length - 1
        max_xy = base_length + 2 * side_length - 2
        for coord in cls.coordinates_unbordered(x_bound, y_bound):
            x, y, z = coord
            xy = x + y
            if (xy <= min_xy) or (xy > max_xy) or ((xy == max_xy) and (z != 2)):
                continue
            yield cls.coordinate_offset(x, y, z, offset)

    @classmethod
    def coordinates_semiregular_hexagon(cls, base_length, side_length,
                                        offset=None):
        x_bound = y_bound = side_length + base_length - 1
        min_xy = side_length - 1
        max_xy = base_length + 2 * side_length - 2
        for coord in cls.coordinates_bordered(x_bound, y_bound):
            x, y, z = coord
            xy = x + y
            if (xy < min_xy) or ((xy == min_xy) and (z == 2)) or (xy > max_xy):
                continue
            yield cls.coordinate_offset(x, y, z, offset)

    @classmethod
    def coordinates_trapezoid(cls, m, n, offset=None):
        """
        Trapezoidal bordered polytwig grid of base length M & height N hexagons.
        """
        max_xy = m
        for coord in cls.coordinates_bordered(m, n):
            x, y, z = coord
            xy = x + y
            if xy > max_xy:
                continue
            yield cls.coordinate_offset(x, y, z, offset)

    @classmethod
    def coordinates_trapezoid_unbordered(cls, m, n, offset=None):
        """
        Trapezoidal unbordered polytwig grid of base length M & height N
        hexagons.
        """
        max_xy = m
        for coord in cls.coordinates_unbordered(m, n):
            x, y, z = coord
            xy = x + y
            if (xy > max_xy) or (xy == max_xy and z != 2):
                continue
            yield cls.coordinate_offset(x, y, z, offset)

    @classmethod
    def coordinates_inverted_trapezoid_unbordered(cls, m, n, offset=None):
        """
        Inverted trapezoidal unbordered polytwig grid of base length M &
        height N hexagons.
        """
        min_xy = n
        for coord in cls.coordinates_unbordered(m, n):
            x, y, z = coord
            xy = x + y
            if (xy < min_xy):
                continue
            yield cls.coordinate_offset(x, y, z, offset)

    @classmethod
    def coordinates_triangle(cls, m, offset=None):
        """
        Triangular bordered polytwig grid of side length M hexagons.
        """
        return cls.coordinates_trapezoid(m, m, offset)

    @classmethod
    def coordinates_triangle_unbordered(cls, m, offset=None):
        """
        Triangular unbordered polytwig grid of side length M hexagons.
        """
        return cls.coordinates_trapezoid_unbordered(m, m, offset)

    @classmethod
    def coordinates_inverted_triangle(cls, m, offset=None):
        """
        Inverted (down-pointing) triangular bordered polytwig grid of side
        length M hexagons.
        """
        min_xy = m - 1
        for coord in cls.coordinates_bordered(m, m):
            x, y, z = coord
            xy = x + y
            if xy > min_xy or (xy == min_xy and z != 2):
                yield cls.coordinate_offset(x, y, z, offset)

    @classmethod
    def coordinates_inverted_triangle_unbordered(cls, m, offset=None):
        """
        Inverted (down-pointing) triangular unbordered polytwig grid of side
        length M hexagons.
        """
        min_xy = m
        for coord in cls.coordinates_unbordered(m, m):
            x, y, z = coord
            xy = x + y
            if xy >= min_xy:
                yield cls.coordinate_offset(x, y, z, offset)

    @classmethod
    def coordinates_hexagram(cls, side_length, offset=None):
        """Hexagram bordered polytwig grid."""
        s = side_length
        if not offset:
            offset = (0, 0, 0)
        x, y, z = offset
        offset1 = (x + s - 1, y + s - 1, z)
        coords = (
            list(set(cls.coordinates_triangle(s * 3 - 2, offset=offset1)))
            + list(set(cls.coordinates_inverted_triangle(s * 3 - 2, offset))))
        return sorted(coords)

    @classmethod
    def coordinates_chevron(cls, base, side, offset=None):
        """
        Chevron-shaped bordered polytwig grid, (base, side) length in hexagons.
        """
        min_xy = side - 1
        max_xy = base + side - 1
        last_y = side * 2 - 1
        for coord in cls.coordinates_bordered(max_xy, last_y):
            x, y, z = coord
            xy = x + y
            if (xy < min_xy) or ((xy == min_xy) and (z == 2)):
                continue
            if (y < side) and (xy > max_xy):
                continue
            if (y >= side) and ((x > base) or ((x == base) and (z == 0))):
                continue
            if y == last_y and x == base and z == 2:
                continue
            yield cls.coordinate_offset(x, y, z, offset)

    @classmethod
    def coordinates_butterfly(cls, base, side, offset=None):
        """
        Butterfly-shaped bordered polytwig grid, (base, side) length in
        hexagons.
        """
        min_xy = (side - 1) * 2
        max_xy = base + side - 1
        last_y = side * 2 - 1
        first_x = side - 1
        for coord in cls.coordinates_bordered(max_xy, last_y):
            x, y, z = coord
            xy = x + y
            if (y >= side) and (((xy < min_xy) or ((xy == min_xy) and (z == 2)))
                                or ((x > base) or ((x == base) and (z == 0)))):
                continue
            if (y < side) and ((xy > max_xy) or (x < first_x) or
                               (x == first_x and y == 0 and z == 2)):
                continue
            if y == last_y and x == base and z == 2:
                continue
            yield cls.coordinate_offset(x, y, z, offset)

    @classmethod
    def coordinates_butterfly_unbordered(cls, base, side, offset=None):
        """
        Butterfly-shaped unbordered polytwig grid, (base, side) length in
        hexagons.
        """
        bite = coordsys.HexagonalGrid3DCoordSet(
            cls.coordinates_elongated_hexagon(1, side - 1))
        coords = coordsys.HexagonalGrid3DCoordSet(
            set(cls.coordinates_elongated_hexagon_unbordered(base, side))
            - bite.translate((0, 1, 0))
            - bite.translate((base, 1, 0)))
        if offset:
            coords = coords.translate(offset)
        return sorted(coords)

    @classmethod
    def coordinates_vertically_staggered_rectangle(cls, m, n, offset=None):
        last_x = m
        last_y = n
        min_x2y = int((m - 1) / 2) * 2
        max_x2y = min_x2y + 2 * n + 1
        for coord in cls.coordinates_bordered(m, n + int((m - 1) / 2)):
            x, y, z = coord
            x2y = x + 2 * y
            if (  (x2y < min_x2y) or (x2y == min_x2y and not (x % 2) and z == 2)
                  or (x2y > max_x2y) or (x2y == max_x2y and (x % 2) and z == 1)
                  or (x == last_x and y == last_y and z == 2)):
                continue
            yield cls.coordinate_offset(x, y, z, offset)

    @classmethod
    def coordinates_inset_rectangle(cls, m, n, offset=None):
        last_x = m
        last_y = n - 1
        min_x2y = int((m - 1) / 2) * 2
        max_x2y = min_x2y + 2 * n
        for coord in cls.coordinates_bordered(m, n + int((m - 1) / 2)):
            x, y, z = coord
            x2y = x + 2 * y
            if (  (x2y < min_x2y) or (x2y == min_x2y and not (x % 2) and z == 2)
                  or (x2y > max_x2y)
                  or (x2y == max_x2y and not (x % 2) and z == 1)
                  or (x == last_x and not (x % 2) and y == last_y and z == 2)):
                continue
            yield cls.coordinate_offset(x, y, z, offset)

    @classmethod
    def coordinates_rounded_rectangle(cls, m, n, offset=None):
        last_x = m
        last_y = n - 1
        min_x2y = m - 1 - (m % 2)
        max_x2y = min_x2y + 2 * n
        for coord in cls.coordinates_bordered(m, n + int((m - 1) / 2)):
            x, y, z = coord
            x2y = x + 2 * y
            x2y_a = x2y - (x + 1) % 2
            x2y_b = x2y + (x + 1) % 2
            if (min_x2y <= x2y <= max_x2y and
                not ((x2y_a == min_x2y and z == 2 and (x == 0 or x % 2))
                     or (x2y_b == max_x2y and z == 1 and (x == 0 or x % 2))
                     or (x == last_x and y == last_y and z == 2 and x % 2))):
                yield cls.coordinate_offset(x, y, z, offset)

    def make_aspects(self, units, flips=(0, 1), rotations=(0, 1, 2, 3, 4, 5)):
        aspects = set()
        for flip in flips or (0,):
            for rotation in rotations or (0,):
                aspect = coordsys.HexagonalGrid3DView(
                    units, rotation, 0, flip) # 0 is axis, ignored
                aspects.add(aspect)
        return aspects

    build_matrix_header = PuzzlePseudo3D.build_matrix_header

    build_matrix_row = PuzzlePseudo3D.build_matrix_row

    def format_solution(self, solution, normalized=True, rotate_180=False):
        s_matrix = self.build_solution_matrix(solution)
        if rotate_180:                  # !!! ???
            s_matrix = [[list(reversed(s_matrix[z][y]))
                         for y in reversed(range(self.height))]
                        for z in reversed(range(self.depth))]
        return self.format_hexagonal_grid(s_matrix)

    _hexgrid_parts = (
        # z == 0:
        (('', '_%-3s'),                 # occupied cell, lines[0..1]
         ('', '    ')),                 # empty cell
        # z == 1:
        (('%-3s   ', ' \\'),            # occupied cell
         ('      ',  '  ')),            # empty cell
        # z == 2:
        ((' %-3s  ', '/     '),         # occupied cell
         ('      ',  '      ')))        # empty cell

    def format_hexagonal_grid(self, s_matrix):
        """
        In order to have enough space for two or three characters per segment,
        the solutions will have to be formatted at least this big::

                              ____
                             /    \
                        _R05/      \
                       R05  R05    /
                  _I1_/      \_R05/
                 L2   C3     R05  W4
                /      \_S3_/      \
                L2     C3   S3     W4
                 \_C3_/      \_S3_/
                 P4   Y3     /    W4
                /      \_Y3_/      \
                P4     Y3   Y4     W4
                 \_P4_/      \_Y4_/
                 C4   P4     Y4
                /      \_Y4_/
                C4     C4
                 \_C4_/

        3 sections for each intersection:

        * z==0::

            _I1_

        * z==1::

             I04
              \

        * z==2::

             I04
            /

        For 3 characters per segment, a larger representation would be better.
        For or 4 or even 5, it would be needed::

                            _C002_
                           /      \
                          C002     S05
                   _S05__/          \_Q05__
                  /      \          /      \
                 S05      S05      S05      Q06
                /          \_S05__/          \
                \          /      \          /
                 T05      T05      Q06      Q06
                  \_T05__/          \_Q06__/
                         \          /
                          T05      Q06
                           \_T05__/
        """
        width = len(s_matrix[0][0])
        height = len(s_matrix[0])
        output = [[''] * width
                  for _ in range(height * 4 + (width - 1) * 2)]
        offsets = [2, 2, 0]
        for x in range(width):
            for y in range(height):
                y_offset = y * 4 + x * 2
                for z in reversed(range(self.depth)):
                    cell = s_matrix[z][y][x]
                    parts = self._hexgrid_parts[z][cell == self.empty_cell]
                    for i, part in enumerate(parts):
                        if '%' in part:
                            part = part % (cell or '_\\/'[z])
                        if '_' in part:
                            part = part.replace(' ', '_')
                        output[y_offset + offsets[z] + 1 - i][x] += part
        lines = [''.join((part or '      ') for part in row) for row in output]
        min_padding = width * 6
        for i, row in enumerate(output):
            line = ''.join((part or '      ') for part in row)
            min_padding = min(min_padding, len(line) - len(line.lstrip()))
            output[i] = line.rstrip()
        while not output[0].strip():
            del output[0]
        while not output[-1].strip():
            del output[-1]
        if min_padding:
            for i, line in enumerate(output):
                output[i] = line[min_padding:]
        return '\n'.join(reversed(output))

    def format_coords(self):
        s_matrix = self.empty_solution_matrix()
        for x, y, z in self.solution_coords:
            s_matrix[z][y][x] = ''
        return self.format_hexagonal_grid(s_matrix)

    def calculate_svg_dimensions(self):
        height = (self.height + self.width/2.0) * self.svg_unit_height
        width = (self.width + 1) * self.svg_unit_width
        return height, width

    def svg_path_data(self, s_matrix):
        s_coords = sorted(self.solution_coords)
        lines = collections.defaultdict(dict)
        curves = {}
        margin = self.margin
        for coord in s_coords:
            (x, y, z) = coord
            name = s_matrix[z][y + margin][x + margin]
            if name == self.empty_cell:
                continue
            # initial line segment end coordinates; will be adjusted below:
            lines[name][coord] = self.svg_line_coords(coord)
            curves[name] = []
            neighbors = coord.neighbors()
            start_join = False
            for (xn, yn, zn) in neighbors[:2]:
                start_join = (
                    start_join or (s_matrix[zn][yn + margin][xn + margin]
                                   == name))
            lines[name][coord][0] += self.svg_deltas[start_join][z]
            end_join = False
            for (xn, yn, zn) in neighbors[2:]:
                end_join = (
                    end_join
                    or (s_matrix[zn][yn + margin][xn + margin] == name))
            lines[name][coord][1] -= self.svg_deltas[end_join][z]
        for coord in s_coords:
            (x, y, z) = coord
            name = s_matrix[z][y + margin][x + margin]
            if name == self.empty_cell:
                continue
            neighbors = coord.neighbors()
            # Each segment checks for the next neighbor counter-clockwise,
            # at each end (0 == coordinate intersection, 2 == off-coordinate):
            for (neighbor, end) in ((0, 0), (2, 1)):
                (xn, yn, zn) = neighbors[neighbor]
                if s_matrix[zn][yn + margin][xn + margin] == name:
                    start = lines[name][coord][end]
                    end = lines[name][neighbors[neighbor]][end]
                    curves[name].append((start, end, self.svg_radii[1]))
        return lines, curves

    def svg_line_coords(self, coord):
        """
        Return the (x,y) coordinates of the start- and end-points of the
        full-length hexgrid line segment (x,y,z), as a list.
        """
        x, y, z = coord
        start_coord = self.svg_coord(coord)
        end_coord = start_coord + self.svg_line_deltas[z]
        return [start_coord, end_coord]

    def svg_coord(self, coord):
        """
        Return the SVG (x,y) coordinates of the start-point of the hexgrid
        coordinate.
        """
        x, y, z = coord
        yunit = self.svg_unit_height
        height = (self.height + self.width/2.0 - 1) * yunit
        return coordsys.Cartesian2D(
            ((x + 1) * self.svg_unit_width, height - (y + x * 0.5) * yunit))

    def calculate_svg_details(self):
        # called from __init__
        """
        For 120° angle, line thickness "t", line end must be >= (1 +
        sqrt(3)/2)t short (~= 1.866t; for t=16, short 29.85).

        Curve end-points (relative to intersection point)::

               (-dx1, +dy1).
                            \
                             \____.(+dx0, 0)
                             /
                            /
               (-dx1, -dy1).

        For unit length = 100, line thickness = 16:

        ===  =======  =========  ==========
        var  formula  stub/end   120°
        ===  =======  =========  ==========
        dx0           14         32
        dx1  =dx0/2   7          16
        dy1  =dx1*√3  ?????????  27.7128129
        r    =dx0*√3  n/a        55.4256258
        ===  =======  =========  ==========
        """
        unit_length = self.svg_unit_length
        sqrt3 = 3 ** .5
        dx0 = (unit_length * .14,       # stub/end
               unit_length * .32)       # 120°
        dx1 = tuple(val / 2 for val in dx0)
        dy1 = tuple(val * sqrt3 for val in dx1)
        svg_deltas = [
            ((+dx0[i], 0),
             (-dx1[i], -dy1[i]),
             (-dx1[i], +dy1[i])) for i in range(2)]
        svg_radii = (None, dx0[1] * sqrt3)
        return svg_deltas, svg_radii


class MonotwigsData(object):

    piece_data = {
        'I1': (((0,0,0),), {}),}

    symmetric_pieces = ['I1']
    """Pieces with reflexive symmetry, identical to their mirror images."""

    asymmetric_pieces = []
    """Pieces without reflexive symmetry, different from their mirror images."""

    piece_colors = {
        'I1': 'steelblue',}


class DitwigsData(object):

    piece_data = {
        'L2': (((0,0,0), (0,0,1)), {}),}

    symmetric_pieces = ['L2']
    """Pieces with reflexive symmetry, identical to their mirror images."""

    asymmetric_pieces = []
    """Pieces without reflexive symmetry, different from their mirror images."""

    piece_colors = {
        'L2': 'khaki',}


class TritwigsData(object):

    piece_data = {
        'Y3': (((0, 0, 0), (0, 0, 1), (0, 0, 2)), {}),
        'S3': (((0, 1, 0), (1, 0, 0), (1, 0, 1)), {}),
        'C3': (((0, 0, 0), (0, 0, 1), (0, 1, 2)), {}),}

    symmetric_pieces = ['C3', 'Y3']
    """Pieces with reflexive symmetry, identical to their mirror images."""

    asymmetric_pieces = ['S3']
    """Pieces without reflexive symmetry, different from their mirror images."""

    piece_colors = {
        'Y3': 'lime',
        'S3': 'magenta',
        'C3': 'cyan',
        '0': 'gray',
        '1': 'black'}


class TetratwigsData(object):

    piece_data = {
        'Y4': (((0, 1, 0), (1, 0, 0), (1, 0, 1), (1, 0, 2)), {}),
        'W4': (((0, 1, 0), (0, 1, 1), (1, 0, 0), (1, 0, 1)), {}),
        'P4': (((0, 1, 0), (0, 1, 1), (1, 0, 1), (1, 0, 2)), {}),
        'C4': (((0, 0, 0), (0, 0, 1), (0, 1, 2), (1, 0, 2)), {}),}

    symmetric_pieces = ['C4', 'W4']
    """Pieces with reflexive symmetry, identical to their mirror images."""

    asymmetric_pieces = ['P4', 'Y4']
    """Pieces without reflexive symmetry, different from their mirror images."""

    piece_colors = {
        'C4': 'darkorange',
        'P4': 'blueviolet',
        'Y4': 'darkgreen',
        'W4': 'teal',
        '0': 'gray',
        '1': 'black'}


class PentatwigsData(object):

    piece_data = {
        'C5': (((0, 0, 0), (0, 0, 1), (0, 1, 2), (1, 0, 1), (1, 0, 2)), {}),
        'H5': (((0, 1, 0), (0, 1, 1), (0, 1, 2), (0, 2, 2), (1, 0, 1)), {}),
        'I5': (((0, 2, 0), (0, 2, 1), (1, 1, 0), (1, 1, 1), (2, 0, 1)), {}),
        'L5': (((0, 1, 0), (0, 1, 1), (0, 1, 2), (1, 0, 0), (1, 0, 1)), {}),
        'P5': (((0, 0, 1), (0, 1, 0), (0, 1, 2), (1, 0, 0), (1, 0, 1)), {}),
        'R5': (((0, 1, 0), (0, 1, 1), (0, 1, 2), (1, 0, 1), (1, 0, 2)), {}),
        'S5': (((0, 1, 0), (0, 1, 2), (1, 0, 0), (1, 0, 1), (2, 0, 2)), {}),
        'T5': (((0, 2, 0), (1, 1, 0), (1, 1, 1), (1, 1, 2), (2, 0, 1)), {}),
        'U5': (((0, 1, 0), (1, 1, 0), (1, 1, 2), (2, 0, 0), (2, 0, 1)), {}),
        'W5': (((0, 1, 0), (0, 1, 1), (1, 0, 0), (1, 0, 1), (2, 0, 2)), {}),
        'X5': (((0, 1, 0), (0, 1, 1), (0, 1, 2), (1, 0, 1), (1, 1, 2)), {}),
        'Y5': (((0, 0, 1), (0, 1, 0), (0, 1, 1), (0, 1, 2), (1, 0, 1)), {}),}

    symmetric_pieces = 'C5 T5 U5 X5 Y5'.split()
    """Pieces with reflexive symmetry, identical to their mirror images."""

    asymmetric_pieces = 'H5 I5 L5 P5 R5 S5 W5'.split()
    """Pieces without reflexive symmetry, different from their mirror images."""

    piece_colors = {
        'C5': 'blue',
        'H5': 'red',
        'I5': 'lightcoral',
        'L5': 'peru',
        'P5': 'green',
        'R5': 'navy',
        'S5': 'turquoise',
        'U5': 'maroon',
        'T5': 'brown',
        'W5': 'plum',
        'X5': 'indigo',
        'Y5': 'olive',
        '0': 'gray',
        '1': 'black'}


class HexatwigsData(object):

    piece_data = {
        'C06': (((0, 1, 0), (1, 1, 0), (1, 1, 2),
                 (2, 0, 0), (2, 0, 1), (2, 0, 2)), {}),
        'F06': (((0, 2, 0), (0, 2, 2), (1, 1, 0),
                 (1, 1, 1), (1, 1, 2), (2, 0, 1)), {}),
        'H06': (((0, 2, 0), (0, 2, 1), (1, 0, 1),
                 (1, 1, 0), (1, 1, 1), (1, 1, 2)), {}),
        'H16': (((0, 2, 0), (0, 2, 1), (1, 1, 0),
                 (1, 1, 1), (1, 1, 2), (2, 0, 1)), {}),
        'I06': (((0, 3, 0), (1, 2, 0), (1, 2, 1),
                 (2, 1, 0), (2, 1, 1), (3, 0, 1)), {}),
        'J06': (((0, 1, 0), (0, 1, 1), (0, 2, 0),
                 (0, 2, 2), (1, 0, 0), (1, 0, 1)), {}),
        'L06': (((0, 2, 0), (0, 2, 1), (0, 3, 2),
                 (1, 1, 0), (1, 1, 1), (2, 0, 1)), {}),
        'L16': (((0, 2, 0), (1, 1, 0), (1, 1, 1),
                 (2, 0, 0), (2, 0, 1), (2, 0, 2)), {}),
        'L26': (((0, 1, 0), (0, 1, 1), (1, 0, 0),
                 (1, 0, 1), (1, 0, 2), (2, 0, 2)), {}),
        'M06': (((0, 1, 0), (0, 1, 1), (0, 2, 2),
                 (1, 0, 0), (1, 0, 1), (2, 0, 2)), {}),
        'O06': (((0, 0, 0), (0, 0, 1), (0, 1, 0),
                 (0, 1, 2), (1, 0, 1), (1, 0, 2)), {}),
        'Q06': (((0, 0, 0), (0, 0, 1), (0, 1, 0),
                 (0, 1, 1), (1, 0, 1), (1, 0, 2)), {}),
        'Q16': (((0, 0, 1), (0, 1, 0), (0, 1, 2),
                 (1, 0, 0), (1, 0, 1), (1, 0, 2)), {}),
        'Q26': (((0, 0, 0), (0, 1, 0), (0, 1, 2),
                 (1, 0, 0), (1, 0, 1), (1, 0, 2)), {}),
        'R06': (((0, 2, 0), (0, 2, 2), (1, 0, 1),
                 (1, 1, 0), (1, 1, 1), (1, 1, 2)), {}),
        'R16': (((0, 1, 0), (0, 1, 2), (1, 0, 0),
                 (1, 0, 1), (1, 0, 2), (2, 0, 2)), {}),
        'S06': (((0, 0, 0), (0, 1, 0), (0, 1, 1),
                 (0, 2, 2), (1, 0, 1), (1, 0, 2)), {}),
        'S16': (((0, 2, 0), (0, 2, 1), (0, 3, 2),
                 (1, 0, 1), (1, 1, 1), (1, 1, 2)), {}),
        'S26': (((0, 1, 0), (0, 1, 1), (0, 2, 2),
                 (1, 0, 0), (1, 0, 1), (1, 0, 2)), {}),
        'U06': (((0, 1, 0), (0, 1, 1), (0, 1, 2),
                 (1, 0, 0), (1, 0, 1), (1, 0, 2)), {}),
        'V06': (((0, 0, 0), (0, 0, 2), (0, 1, 0),
                 (0, 1, 1), (1, 0, 1), (1, 0, 2)), {}),
        'W06': (((0, 1, 0), (0, 1, 1), (0, 2, 1),
                 (0, 2, 2), (1, 0, 0), (1, 0, 1)), {}),
        'X06': (((0, 1, 0), (0, 1, 1), (1, 0, 0),
                 (1, 0, 1), (1, 0, 2), (1, 1, 2)), {}),
        'X16': (((0, 1, 0), (0, 1, 2), (1, 0, 0),
                 (1, 0, 1), (1, 0, 2), (1, 1, 2)), {}),
        'Y06': (((0, 2, 0), (1, 0, 1), (1, 1, 0),
                 (1, 1, 1), (1, 1, 2), (2, 1, 2)), {}),
        'Y16': (((0, 2, 0), (1, 0, 1), (1, 1, 0),
                 (1, 1, 1), (1, 1, 2), (2, 0, 1)), {}),
        'Y26': (((0, 0, 0), (0, 1, 0), (0, 1, 1),
                 (1, 0, 0), (1, 0, 1), (1, 0, 2)), {}),}

    symmetric_pieces = 'I06 M06 O06 U06 V06'.split()
    """Pieces with reflexive symmetry, identical to their mirror images."""

    asymmetric_pieces = (
        'C06 F06 H06 H16 J06 L06 L16 L26 Q06 Q16 Q26 R06 R16 '
        'S06 S16 S26 W06 X06 X16 Y06 Y16 Y26').split()
    """Pieces without reflexive symmetry, different from their mirror images."""

    piece_colors = {
        'C06': 'tan',
        'F06': 'slateblue',
        'H06': 'aquamarine',
        'H16': 'cadetblue',
        'I06': 'burlywood',
        'J06': 'crimson',
        'L06': 'darkgoldenrod',
        'L16': 'deepskyblue',
        'L26': 'peachpuff',
        'M06': 'darkkhaki',
        'O06': 'darkseagreen',
        'Q06': 'deeppink',
        'Q16': 'greenyellow',
        'Q26': 'hotpink',
        'R06': 'indianred',
        'R16': 'olivedrab',
        'S06': 'limegreen',
        'S16': 'mediumpurple',
        'S26': 'orange',
        'U06': 'palegreen',
        'V06': 'paleturquoise',
        'W06': 'darkorchid',
        'X06': 'silver',
        'X16': 'thistle',
        'Y06': 'tomato',
        'Y16': 'violet',
        'Y26': 'darkmagenta',
        '0': 'gray',
        '1': 'black'}


class Polytwigs12(Polytwigs):

    piece_data = copy.deepcopy(MonotwigsData.piece_data)
    piece_data.update(copy.deepcopy(DitwigsData.piece_data))
    symmetric_pieces = (
        MonotwigsData.symmetric_pieces + DitwigsData.symmetric_pieces)
    asymmetric_pieces = []
    piece_colors = copy.deepcopy(MonotwigsData.piece_colors)
    piece_colors.update(DitwigsData.piece_colors)


class Polytwigs123(Polytwigs12):

    piece_data = copy.deepcopy(Polytwigs12.piece_data)
    piece_data.update(copy.deepcopy(TritwigsData.piece_data))
    symmetric_pieces = (
        Polytwigs12.symmetric_pieces + TritwigsData.symmetric_pieces)
    asymmetric_pieces = TritwigsData.asymmetric_pieces[:]
    piece_colors = copy.deepcopy(Polytwigs12.piece_colors)
    piece_colors.update(TritwigsData.piece_colors)


class OneSidedPolytwigs123(OneSidedLowercaseMixin, Polytwigs123):

    pass


class Tetratwigs(TetratwigsData, Polytwigs):

    pass


class OneSidedTetratwigs(OneSidedLowercaseMixin, Tetratwigs):

    pass


class Polytwigs1234(Polytwigs123):

    piece_data = copy.deepcopy(Polytwigs123.piece_data)
    piece_data.update(copy.deepcopy(TetratwigsData.piece_data))
    symmetric_pieces = (
        Polytwigs123.symmetric_pieces + TetratwigsData.symmetric_pieces)
    asymmetric_pieces = (
        Polytwigs123.asymmetric_pieces + TetratwigsData.asymmetric_pieces)
    piece_colors = copy.deepcopy(Polytwigs123.piece_colors)
    piece_colors.update(TetratwigsData.piece_colors)


class OneSidedPolytwigs1234(OneSidedLowercaseMixin, Polytwigs1234):

    pass


class Pentatwigs(PentatwigsData, Polytwigs):

    pass


class OneSidedPentatwigs(OneSidedLowercaseMixin, Pentatwigs):

    pass


class Polytwigs45(Pentatwigs):

    piece_data = copy.deepcopy(Pentatwigs.piece_data)
    piece_data.update(copy.deepcopy(TetratwigsData.piece_data))
    symmetric_pieces = (
        Tetratwigs.symmetric_pieces + PentatwigsData.symmetric_pieces)
    asymmetric_pieces = (
        Tetratwigs.asymmetric_pieces + PentatwigsData.asymmetric_pieces)
    piece_colors = copy.deepcopy(TetratwigsData.piece_colors)
    piece_colors.update(PentatwigsData.piece_colors)


class OneSidedPolytwigs45(OneSidedLowercaseMixin, Polytwigs45):

    pass


class Polytwigs12345(Polytwigs1234):

    piece_data = copy.deepcopy(Polytwigs1234.piece_data)
    piece_data.update(copy.deepcopy(PentatwigsData.piece_data))
    symmetric_pieces = (
        Polytwigs1234.symmetric_pieces + PentatwigsData.symmetric_pieces)
    asymmetric_pieces = (
        Polytwigs1234.asymmetric_pieces + PentatwigsData.asymmetric_pieces)
    piece_colors = copy.deepcopy(Polytwigs1234.piece_colors)
    piece_colors.update(PentatwigsData.piece_colors)


class OneSidedPolytwigs12345(OneSidedLowercaseMixin, Polytwigs12345):

    pass


class Hexatwigs(HexatwigsData, Polytwigs):

    pass


class OneSidedHexatwigs(OneSidedLowercaseMixin, Hexatwigs):

    pass


class Polytwigs123456(Polytwigs12345):

    piece_data = copy.deepcopy(Polytwigs12345.piece_data)
    piece_data.update(copy.deepcopy(HexatwigsData.piece_data))
    symmetric_pieces = (
        Polytwigs12345.symmetric_pieces + HexatwigsData.symmetric_pieces)
    asymmetric_pieces = (
        Polytwigs12345.asymmetric_pieces + HexatwigsData.asymmetric_pieces)
    piece_colors = copy.deepcopy(Polytwigs12345.piece_colors)
    piece_colors.update(HexatwigsData.piece_colors)


class OneSidedPolytwigs123456(OneSidedLowercaseMixin, Polytwigs123456):

    pass


class QuasiDitwigsData(object):

    piece_data = {
        'L2': (((0,0,0), (0,0,1)), {}),
        'S2': (((0,0,0), (1,0,0)), {}),
        'C2': (((0,0,0), (1,0,1)), {}),}

    symmetric_pieces = ['L2', 'C2']
    """Pieces with reflexive symmetry, identical to their mirror images."""

    asymmetric_pieces = ['S2']
    """Pieces without reflexive symmetry, different from their mirror images."""

    piece_colors = {
        'L2': 'khaki',
        'C2': 'darkblue',
        'S2': 'darkred',}


class QuasiTritwigsData(object):

    piece_data = {
        'C03': (((0, 0, 0), (0, 0, 1), (0, 1, 2)), {}),
        'S03': (((0, 1, 0), (1, 0, 0), (1, 0, 1)), {}),
        'Y03': (((0, 0, 0), (0, 0, 1), (0, 0, 2)), {}),
        'C13': (((0, 0, 0), (0, 0, 1), (0, 1, 0)), {}),
        'C23': (((0, 0, 0), (0, 1, 2), (1, 0, 1)), {}),
        'H13': (((0, 0, 0), (1, 0, 0), (1, 1, 2)), {}),
        'I13': (((0, 2, 0), (1, 1, 0), (2, 0, 0)), {}),
        'P13': (((0, 1, 2), (1, 0, 0), (1, 0, 1)), {}),
        'P23': (((0, 0, 0), (0, 0, 1), (0, 1, 1)), {}),
        'P33': (((0, 0, 0), (0, 1, 2), (1, 0, 0)), {}),
        'S13': (((0, 1, 0), (0, 2, 2), (1, 0, 2)), {}),
        'T13': (((0, 0, 1), (0, 1, 0), (0, 2, 2)), {}),
        'U13': (((0, 1, 0), (1, 0, 0), (2, 0, 0)), {}),
        'W13': (((0, 1, 1), (1, 0, 0), (1, 0, 1)), {}),
        'W23': (((0, 1, 0), (0, 2, 2), (1, 0, 0)), {}),
        'Y13': (((0, 0, 1), (0, 1, 0), (0, 1, 1)), {}),
        'Y23': (((0, 0, 0), (0, 1, 0), (1, 0, 0)), {}),}

    symmetric_pieces = ['C03', 'C23', 'T13', 'U13', 'Y03', 'Y23']
    """Pieces with reflexive symmetry, identical to their mirror images."""

    asymmetric_pieces = [
        'C13', 'H13', 'I13', 'P13', 'P23', 'P33', 'S03', 'S13', 'Y13',
        'W13', 'W23']
    """Pieces without reflexive symmetry, different from their mirror images."""

    piece_colors = {
        'C03': 'cyan',
        'S03': 'magenta',
        'Y03': 'lime',
        'C13': 'darkorange',
        'C23': 'blue',
        'H13': 'red',
        'I13': 'green',
        'P13': 'blueviolet',
        'P23': 'peru',
        'P33': 'navy',
        'S13': 'turquoise',
        'T13': 'brown',
        'U13': 'cadetblue',
        'W13': 'teal',
        'W23': 'plum',
        'Y13': 'darkgreen',
        'Y23': 'olive',
        '0': 'gray',
        '1': 'black'}


class QuasiTritwigs(QuasiTritwigsData, Polytwigs):

    pass


class OneSidedQuasiTritwigs(OneSidedLowercaseMixin, QuasiTritwigs):

    pass


class QuasiPolytwigs123(Polytwigs):

    piece_data = copy.deepcopy(MonotwigsData.piece_data)
    piece_data.update(copy.deepcopy(QuasiDitwigsData.piece_data))
    piece_data.update(copy.deepcopy(QuasiTritwigsData.piece_data))
    symmetric_pieces = (
        MonotwigsData.symmetric_pieces + QuasiDitwigsData.symmetric_pieces
        + QuasiTritwigsData.symmetric_pieces)
    asymmetric_pieces = (
        MonotwigsData.asymmetric_pieces + QuasiDitwigsData.asymmetric_pieces
        + QuasiTritwigsData.asymmetric_pieces)
    piece_colors = copy.deepcopy(MonotwigsData.piece_colors)
    piece_colors.update(QuasiDitwigsData.piece_colors)
    piece_colors.update(QuasiTritwigsData.piece_colors)


class OneSidedQuasiPolytwigs123(OneSidedLowercaseMixin, QuasiPolytwigs123):

    pass
