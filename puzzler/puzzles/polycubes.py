#!/usr/bin/env python
# $Id$

"""
Polycube puzzle base classes.
"""

import copy

from puzzler.puzzles import Puzzle3D
from puzzler.puzzles.polyominoes import Pentominoes


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


class SolidPentominoes(Puzzle3D, Pentominoes):

    def make_aspects(self, units,
                     flips=(0, 1), axes=(0, 1, 2), rotations=(0, 1, 2, 3)):
        units = tuple((x, y, 0) for (x, y) in units) # convert to 3D
        return Puzzle3D.make_aspects(self, units, flips, axes, rotations)


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


class NonConvexPentacubes(Pentacubes):

    """
    These are the regular pentacubes less the I piece, the only convex piece.
    """

    def customize_piece_data(self):
        """Remove I."""
        Pentacubes.customize_piece_data(self)
        del self.piece_data['I']
