#!/usr/bin/env python
# $Id$

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2012 by David J. Goodger
# License: GPL 2 (see __init__.py)

"""
Polycube puzzle base classes.
"""

import copy

from puzzler.puzzles import Puzzle3D
from puzzler.puzzles.polyominoes import Pentominoes


class Polycubes(Puzzle3D):

    pass


class Monocube(Polycubes):

    piece_data = {'M': ((), {}),}
    """(0,0,0) is implied."""

    piece_colors = {
        'M': 'black',
        '0': 'gray',
        '1': 'black'}


class Dicube(Polycubes):

    piece_data = {'D': (((1, 0, 0),), {}),}
    """(0,0,0) is implied."""

    piece_colors = {
        'D': 'gray',
        '0': 'gray',
        '1': 'black'}


class Tricubes(Polycubes):

    piece_data = {
        'I3': (((1, 0, 0), (2, 0, 0)), {}),
        'V3': (((1, 0, 0), (0, 1, 0)), {}),}
    """(0,0,0) is implied."""

    piece_colors = {
        'I3': 'darkblue',
        'V3': 'darkred',
        '0': 'gray',
        '1': 'black'}

    # for format_solution:
    piece_width = 3


class Tetracubes(Polycubes):

    piece_data = {
        'I4': ((( 1, 0, 0), (2, 0, 0), (3, 0, 0)), {}),
        'L4': (((-1, 0, 0), (1, 0, 0), (1, 1, 0)), {}),
        'T4': ((( 1, 0, 0), (2, 0, 0), (1, 1, 0)), {}),
        'S4': (((-1, 0, 0), (0, 1, 0), (1, 1, 0)), {}),
        'O4': ((( 1, 0, 0), (0, 1, 0), (1, 1, 0)), {}),
        'B4': ((( 0, 1, 0), (1, 0, 0), (0, 1, 1)), {}),
        'P4': ((( 0, 1, 0), (1, 0, 0), (0, 0, 1)), {}),
        'A4': ((( 0, 1, 0), (1, 0, 0), (1, 0, 1)), {}),}
    """(0,0,0) is implied.  The names are based on Kadon's 'Poly-4 Supplement'
    naming and the names of the Soma Cubes.  See
    http://www.gamepuzzles.com/poly4.htm."""

    piece_colors = {
        'I4': 'blue',
        'O4': 'magenta',
        'T4': 'green',
        'S4': 'lime',
        'L4': 'blueviolet',
        'B4': 'gold',
        'P4': 'red',
        'A4': 'navy',
        '0': 'gray',
        '1': 'black'}

    # for format_solution:
    piece_width = 3


class SomaCubes(Polycubes):

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


class SolidPentominoes(Polycubes, Pentominoes):

    def make_aspects(self, units,
                     flips=(0, 1), axes=(0, 1, 2), rotations=(0, 1, 2, 3)):
        units = tuple((x, y, 0) for (x, y) in units) # convert to 3D
        return Polycubes.make_aspects(self, units, flips, axes, rotations)


class Pentacubes(Polycubes):

    piece_data = {
        'L15': (((-1,  0,  0), ( 1,  0,  0), ( 1,  1,  0), (-1,  0,  1)), {}),
        'L25': (((-1,  0,  0), ( 1,  0,  0), ( 1,  1,  0), ( 0,  0,  1)), {}),
        'L35': (((-1,  0,  0), ( 1,  0,  0), ( 1,  1,  0), ( 1,  0,  1)), {}),
        'L45': (((-1,  0,  0), ( 1,  0,  0), ( 1,  1,  0), ( 1,  1,  1)), {}),
        'J15': (((-1,  0,  0), ( 1,  0,  0), ( 1,  1,  0), (-1,  0, -1)), {}),
        'J25': (((-1,  0,  0), ( 1,  0,  0), ( 1,  1,  0), ( 0,  0, -1)), {}),
        'J45': (((-1,  0,  0), ( 1,  0,  0), ( 1,  1,  0), ( 1,  1, -1)), {}),
        'N15': (((-1,  0,  0), ( 0,  1,  0), ( 1,  1,  0), (-1,  0, -1)), {}),
        'N25': (((-1,  0,  0), ( 0,  1,  0), ( 1,  1,  0), ( 0,  0, -1)), {}),
        'S15': (((-1,  0,  0), ( 0,  1,  0), ( 1,  1,  0), (-1,  0,  1)), {}),
        'S25': (((-1,  0,  0), ( 0,  1,  0), ( 1,  1,  0), ( 0,  0,  1)), {}),
        'T15': (((-1, -1,  0), (-1,  0,  0), (-1,  1,  0), (-1,  0,  1)), {}),
        'T25': (((-1, -1,  0), (-1,  0,  0), (-1,  1,  0), ( 0,  0,  1)), {}),
        'V15': (((-1,  0,  0), ( 0,  1,  0), (-1,  0,  1), (-1, -1,  1)), {}),
        'V25': (((-1,  0,  0), ( 0,  1,  0), ( 0,  1,  1), ( 1,  1,  1)), {}),
        'Q5':  ((( 1,  0,  0), ( 0,  1,  0), ( 1,  1,  0), ( 0,  0,  1)), {}),
        'A5':  ((( 1,  0,  0), ( 1,  1,  0), ( 0,  0,  1), ( 1,  1,  1)), {}),}
    """(0,0,0) is implied.  The names are based on Kadon's 'Superquints' names.
    Kadon's 'J3' piece is a duplicate of the 'L3' piece.
    See http://www.gamepuzzles.com/sqnames.htm."""

    piece_colors = {
        'L15': 'darkseagreen',
        'L25': 'peru',
        'L35': 'rosybrown',
        'L45': 'yellowgreen',
        'J15': 'steelblue',
        'J25': 'darkviolet',
        'J45': 'lightcoral',
        'N15': 'olive',
        'N25': 'teal',
        'S15': 'tan',
        'S25': 'indigo',
        'T15': 'darkkhaki',
        'T25': 'orangered',
        'V15': 'darkorchid',
        'V25': 'tomato',
        'Q5':  'thistle',
        'A5':  'cadetblue',
        '0':  'gray',
        '1':  'black'}

    for _name, (_data, _kwargs) in SolidPentominoes.piece_data.items():
        piece_data[_name + '5'] = (tuple((_x, _y, 0) for (_x, _y) in _data), {})
        piece_colors[_name + '5'] = SolidPentominoes.piece_colors[_name]
    del _name, _data, _kwargs

    # for format_solution:
    piece_width = 4


class PentacubesPlus(Pentacubes):

    """
    Also known as 'Super Deluxe Quintillions', these are the pentacubes with a
    second L3 piece (a.k.a. J3), allowing the construction of box shapes.  See
    http://www.gamepuzzles.com/polycube.htm#SQd.
    """

    def customize_piece_data(self):
        """Add J35, a copy of L35."""
        Pentacubes.customize_piece_data(self)
        self.piece_data['J35'] = copy.deepcopy(self.piece_data['L35'])
        self.piece_colors['J35'] = self.piece_colors['L35']

    def format_solution(self, solution, normalized=True,
                        x_reversed=False, y_reversed=False, z_reversed=False):
        """
        Consider J35 and L35 as the same piece for solution counting purposes.
        """
        formatted = Pentacubes.format_solution(
            self, solution, normalized, x_reversed=x_reversed,
            y_reversed=y_reversed, z_reversed=z_reversed)
        if normalized:
            return formatted.replace('J35', 'L35')
        else:
            return formatted


class NonConvexPentacubes(Pentacubes):

    """
    These are the regular pentacubes less the I piece, the only convex piece.
    """

    def customize_piece_data(self):
        """Remove I."""
        Pentacubes.customize_piece_data(self)
        del self.piece_data['I5']


class Polycubes12(Polycubes):

    piece_data = copy.deepcopy(Monocube.piece_data)
    piece_data.update(copy.deepcopy(Dicube.piece_data))
    piece_colors = copy.deepcopy(Monocube.piece_colors)
    piece_colors.update(Dicube.piece_colors)


class Polycubes123(Polycubes12):

    piece_data = copy.deepcopy(Polycubes12.piece_data)
    piece_data.update(copy.deepcopy(Tricubes.piece_data))
    piece_colors = copy.deepcopy(Polycubes12.piece_colors)
    piece_colors.update(Tricubes.piece_colors)

    # for format_solution:
    piece_width = 3


class Polycubes1234(Polycubes123):

    piece_data = copy.deepcopy(Polycubes123.piece_data)
    piece_data.update(copy.deepcopy(Tetracubes.piece_data))
    piece_colors = copy.deepcopy(Polycubes123.piece_colors)
    piece_colors.update(Tetracubes.piece_colors)


class Polycubes234(Polycubes1234):

    piece_data = copy.deepcopy(Polycubes1234.piece_data)
    del piece_data['M']
    piece_colors = copy.deepcopy(Polycubes1234.piece_colors)
    del piece_colors['M']


class Polycubes12345(Polycubes1234):

    piece_data = copy.deepcopy(Polycubes1234.piece_data)
    piece_data.update(copy.deepcopy(Pentacubes.piece_data))
    piece_colors = copy.deepcopy(Polycubes1234.piece_colors)
    piece_colors.update(Pentacubes.piece_colors)

    # for format_solution:
    piece_width = 4


class Polycubes2345(Polycubes12345):

    piece_data = copy.deepcopy(Polycubes12345.piece_data)
    del piece_data['M']
    piece_colors = copy.deepcopy(Polycubes12345.piece_colors)
    del piece_colors['M']
