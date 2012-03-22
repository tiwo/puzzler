#!/usr/bin/env python
# $Id$

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2012 by David J. Goodger
# License: GPL 2 (see __init__.py)

"""
Polyiamond puzzle base classes.
"""

import math
import copy

from puzzler import coordsys
from puzzler.puzzles import (
    Puzzle, Puzzle3D, PuzzlePseudo3D, OneSidedLowercaseMixin)


class Polyiamonds(PuzzlePseudo3D):

    """
    Polyiamonds use a pseudo-3D coordinate system: 2D + orientation.

    The shape of the matrix is defined by the `coordinates` generator method.
    The `width` and `height` attributes define the maximum bounds only.
    """

    margin = 1

    # triangle orientation (up=0, down=1):
    depth = 2

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

    @classmethod
    def coordinates_parallelogram(cls, base_length, side_length, offset=None):
        for z in range(cls.depth):
            for y in range(side_length):
                for x in range(base_length):
                    yield cls.coordinate_offset(x, y, z, offset)

    @classmethod
    def coordinate_offset(cls, x, y, z, offset):
        if offset:
            return coordsys.Triangular3D((x, y, z)) + offset
        else:
            return coordsys.Triangular3D((x, y, z))

    @classmethod
    def coordinates_hexagon(cls, side_length, offset=None):
        return cls.coordinates_semiregular_hexagon(
            side_length, side_length, offset)

    @classmethod
    def coordinates_semiregular_hexagon(cls, base_length, side_length,
                                        offset=None):
        bound = base_length + side_length
        min_total = side_length
        max_total = 2 * side_length + base_length - 1
        for coord in cls.coordinates_parallelogram(bound, bound):
            x, y, z = coord
            total = x + y + z
            if min_total <= total <= max_total:
                yield cls.coordinate_offset(x, y, z, offset)

    @classmethod
    def coordinates_elongated_hexagon(cls, base_length, side_length,
                                      offset=None):
        x_bound = base_length + side_length
        y_bound = 2 * side_length
        min_total = side_length
        max_total = 2 * side_length + base_length - 1
        for coord in cls.coordinates_parallelogram(x_bound, y_bound):
            x, y, z = coord
            total = x + y + z
            if min_total <= total <= max_total:
                yield cls.coordinate_offset(x, y, z, offset)

    @classmethod
    def coordinates_hexagram(cls, side_length, offset=None):
        max_total = side_length * 5
        min_total = side_length * 3
        for z in range(cls.depth):
            for y in range(side_length * 4):
                for x in range(side_length * 4):
                    total = x + y + z
                    if (  (x >= side_length and y >= side_length
                           and total < max_total)
                          or (total >= min_total
                              and x < min_total
                              and y < min_total)):
                        yield cls.coordinate_offset(x, y, z, offset)

    @classmethod
    def coordinates_butterfly(cls, base_length, side_length, offset=None):
        min_total = side_length * 2
        max_total = base_length + side_length
        for coord in cls.coordinates_parallelogram(base_length + side_length,
                                                   side_length * 2):
            x, y, z = coord
            total = x + y + z
            if (  (y < side_length and x < side_length)
                  or (y >= side_length and total < min_total)
                  or (x >= base_length and total >= max_total)):
                continue
            yield cls.coordinate_offset(x, y, z, offset)

    @classmethod
    def coordinates_trapezoid(cls, base_length, side_length, offset=None):
        max_total = base_length - 1
        for coord in cls.coordinates_parallelogram(base_length, side_length):
            x, y, z = coord
            total = x + y + z
            if total <= max_total:
                yield cls.coordinate_offset(x, y, z, offset)

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
        return '\n'.join(line[left_margin:] for line in output)

    def format_svg_shapes(self, s_matrix):
        polygons = []
        for y in range(1, self.height + 1):
            for x in range(1, self.width + 1):
                for z in range(self.depth):
                    if s_matrix[z][y][x] == self.empty_cell:
                        continue
                    polygons.append(self.build_polygon(s_matrix, x, y, z))
        return polygons

    def calculate_svg_dimensions(self):
        height = (self.height + 2) * self.svg_unit_height
        width = (self.width + self.height / 2.0 + 2) * self.svg_unit_width
        return height, width

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


class Moniamond(Polyiamonds):

    piece_data = {'T1': ((), {})}
    """(0,0) is implied."""

    symmetric_pieces = piece_data.keys() # all of them

    asymmetric_pieces = []

    piece_colors = {'T1': 'gray'}


class Diamond(Polyiamonds):

    piece_data = {'D2': (((0, 0, 1),), {}),}
    """(0,0) is implied."""

    symmetric_pieces = piece_data.keys() # all of them

    asymmetric_pieces = []

    piece_colors = {'D2': 'steelblue'}


class Triamond(Polyiamonds):

    piece_data = {'I3': (((0, 0, 1), (1, 0, 0)), {}),}
    """(0,0) is implied."""

    symmetric_pieces = piece_data.keys() # all of them

    asymmetric_pieces = []

    piece_colors = {'I3': 'teal'}


class Polyiamonds123(Polyiamonds):

    piece_data = copy.deepcopy(Moniamond.piece_data)
    piece_data.update(copy.deepcopy(Diamond.piece_data))
    piece_data.update(copy.deepcopy(Triamond.piece_data))
    symmetric_pieces = (
        Moniamond.symmetric_pieces + Diamond.symmetric_pieces
        + Triamond.symmetric_pieces)
    asymmetric_pieces = []
    piece_colors = copy.deepcopy(Moniamond.piece_colors)
    piece_colors.update(copy.deepcopy(Diamond.piece_colors))
    piece_colors.update(copy.deepcopy(Triamond.piece_colors))


class Tetriamonds(Polyiamonds):

    piece_data = {
        'I4': (((0, 0, 1), (1, 0, 0), (1, 0, 1)), {}),
        'C4': (((0, 0, 1), (1, 0, 0), (1,-1, 1)), {}),
        'T4': (((0, 0, 1), (1, 0, 0), (0, 1, 0)), {}),}
    """(0,0,0) is implied."""

    symmetric_pieces = ['C4', 'T4']

    asymmetric_pieces = ['I4']

    piece_colors = {
        'C4': 'brown',
        'I4': 'plum',
        'T4': 'tomato',}


class OneSidedTetriamonds(OneSidedLowercaseMixin, Tetriamonds):

    pass


class Polyiamonds1234(Polyiamonds123):

    piece_data = copy.deepcopy(Polyiamonds123.piece_data)
    piece_data.update(copy.deepcopy(Tetriamonds.piece_data))
    symmetric_pieces = (
        Polyiamonds123.symmetric_pieces + Tetriamonds.symmetric_pieces)
    asymmetric_pieces = Tetriamonds.asymmetric_pieces[:]
    piece_colors = copy.deepcopy(Polyiamonds123.piece_colors)
    piece_colors.update(Tetriamonds.piece_colors)


class OneSidedPolyiamonds1234(OneSidedLowercaseMixin, Polyiamonds1234):

    pass


class Pentiamonds(Polyiamonds):

    piece_data = {
        'I5': (((0, 0, 1), (1, 0, 0), (1, 0, 1), (2, 0, 0)), {}),
        'C5': (((0, 0, 1), (1, 0, 0), (1,-1, 1), (0,-1, 1)), {}),
        'L5': (((0, 0, 1), (1, 0, 0), (1, 0, 1), (1, 1, 0)), {}),
        'P5': (((0, 0, 1), (1, 0, 0), (1, 0, 1), (0, 1, 0)), {}),}
    """(0,0) is implied."""

    symmetric_pieces = ['C5', 'I5']

    asymmetric_pieces = ['L5', 'P5']

    piece_colors = {
        'C5': 'olive',
        'I5': 'orangered',
        'L5': 'darkseagreen',
        'P5': 'indigo',}


class OneSidedPentiamonds(OneSidedLowercaseMixin, Pentiamonds):

    pass


class Polyiamonds12345(Polyiamonds1234):

    piece_data = copy.deepcopy(Polyiamonds1234.piece_data)
    piece_data.update(copy.deepcopy(Pentiamonds.piece_data))
    symmetric_pieces = (
        Polyiamonds1234.symmetric_pieces + Pentiamonds.symmetric_pieces)
    asymmetric_pieces = (
        Polyiamonds1234.asymmetric_pieces + Pentiamonds.asymmetric_pieces)
    piece_colors = copy.deepcopy(Polyiamonds1234.piece_colors)
    piece_colors.update(Pentiamonds.piece_colors)


class OneSidedPolyiamonds12345(OneSidedLowercaseMixin, Polyiamonds12345):

    pass


class Hexiamonds(Polyiamonds):

    check_for_duplicates = True

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


class OneSidedHexiamonds(OneSidedLowercaseMixin, Hexiamonds):

    pass


class Polyiamonds123456(Polyiamonds12345):

    piece_data = copy.deepcopy(Polyiamonds12345.piece_data)
    piece_data.update(copy.deepcopy(Hexiamonds.piece_data))
    symmetric_pieces = (
        Polyiamonds12345.symmetric_pieces + Hexiamonds.symmetric_pieces)
    asymmetric_pieces = (
        Polyiamonds12345.asymmetric_pieces + Hexiamonds.asymmetric_pieces)
    piece_colors = copy.deepcopy(Polyiamonds12345.piece_colors)
    piece_colors.update(Hexiamonds.piece_colors)


class OneSidedPolyiamonds123456(OneSidedLowercaseMixin, Polyiamonds123456):

    pass


class Heptiamonds(Polyiamonds):

    check_for_duplicates = True

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


class OneSidedHeptiamonds(OneSidedLowercaseMixin, Heptiamonds):

    pass


class Polyiamonds1234567(Polyiamonds123456):

    piece_data = copy.deepcopy(Polyiamonds123456.piece_data)
    piece_data.update(copy.deepcopy(Heptiamonds.piece_data))
    symmetric_pieces = (
        Polyiamonds123456.symmetric_pieces + Heptiamonds.symmetric_pieces)
    asymmetric_pieces = (
        Polyiamonds123456.asymmetric_pieces + Heptiamonds.asymmetric_pieces)
    piece_colors = copy.deepcopy(Polyiamonds123456.piece_colors)
    piece_colors.update(Heptiamonds.piece_colors)


class OneSidedPolyiamonds1234567(OneSidedLowercaseMixin, Polyiamonds1234567):

    pass
