#!/usr/bin/env python
# -*- coding: utf-8 -*-
# $Id$

"""
Polytrig puzzle base classes.
"""

import copy
import math
import collections

from puzzler import coordsys
from puzzler.puzzles import OneSidedLowercaseMixin
from puzzler.puzzles.polysticks import Polysticks


class Polytrigs(Polysticks):

    """
    'Polytrigs' == triangular-grid polysticks ('trig' = TRIangular Grid).
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
            for ((x0, y0), (x1, y1), r) in curves.get(name, []):
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
