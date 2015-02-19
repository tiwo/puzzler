#!/usr/bin/env python
# $Id$

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2014 by David J. Goodger
# License: GPL 2 (see __init__.py)

"""
Polycube puzzle base classes.
"""

import copy

from puzzler.puzzles import Puzzle3D
from puzzler.puzzles.polyominoes import Pentominoes, Hexominoes


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


class SolidPentominoes(Polycubes):

    piece_colors = copy.deepcopy(Pentominoes.piece_colors)
    piece_data = {}
    for _name, (_data, _kwargs) in Pentominoes.piece_data.items():
        piece_data[_name] = (tuple((_x, _y, 0) for (_x, _y) in _data), {})
    del _name, _data, _kwargs


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
        piece_data[_name + '5'] = (_data, _kwargs)
        piece_colors[_name + '5'] = SolidPentominoes.piece_colors[_name]
    del _name, _data, _kwargs

    # for format_solution:
    piece_width = 4


class PentacubesPlus(Pentacubes):

    """
    Also known as Kadon's 'Super Deluxe Quintillions', these are the
    pentacubes with a second L3 piece (a.k.a. J3), total 30 pieces, allowing
    the construction of box shapes.  See
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


class Pentacubes3x3x3(Pentacubes):

    """
    The 25 regular pentacubes that fit in a 3x3x3 box. The I, L, N, and Y
    pieces are omitted.
    """

    omitted_pieces = ('I5', 'L5', 'N5', 'Y5')

    def customize_piece_data(self):
        """Remove pieces with any dimension measuring > 3."""
        Pentacubes.customize_piece_data(self)
        for name in self.omitted_pieces:
            del self.piece_data[name]


class SolidHexominoes(Polycubes):

    piece_colors = copy.deepcopy(Hexominoes.piece_colors)
    piece_data = {}
    for _name, (_data, _kwargs) in Hexominoes.piece_data.items():
        piece_data[_name] = (tuple((_x, _y, 0) for (_x, _y) in _data), {})
    del _name, _data, _kwargs

    # for format_solution:
    piece_width = 4


class SolidHexominoesPlus(SolidHexominoes):

    piece_data = copy.deepcopy(SolidHexominoes.piece_data)
    piece_data['S16'] = copy.deepcopy(piece_data['N06'])
    piece_colors = copy.deepcopy(SolidHexominoes.piece_colors)
    piece_colors['S16'] = piece_colors['N06']


class Hexacubes(Polycubes):

    piece_data = {
        # tromino V plus another out of plane:
        'Aa6': ((( 0,  1,  0), ( 1,  1,  0),
                 ( 0,  1,  1), ( 1,  1,  1), ( 0,  0,  1)), {}),# Kadon's Fat A
        'Ba6': ((( 0,  1,  0), ( 1,  1,  0),
                 ( 1,  1,  1), ( 1,  0,  1), ( 0,  0,  1)), {}),        # B
        # pentomino F plus one cube out of plane:
        'Fa6': ((( 1,  2,  0), ( 0,  2,  0), ( 0,  1,  0), (-1,  1,  0),
                 ( 1,  2,  1)), {}),                                    # F1
        'Fb6': ((( 1,  2,  0), ( 0,  2,  0), ( 0,  1,  0), (-1,  1,  0),
                 ( 0,  2,  1)), {}),                                    # F2
        'Fc6': ((( 1,  2,  0), ( 0,  2,  0), ( 0,  1,  0), (-1,  1,  0),
                 ( 0,  1,  1)), {}),                                    # F3
        'Fd6': ((( 1,  2,  0), ( 0,  2,  0), ( 0,  1,  0), (-1,  1,  0),
                 (-1,  1,  1)), {}),                                    # F4
        'Fe6': ((( 1,  2,  0), ( 0,  2,  0), ( 0,  1,  0), (-1,  1,  0),
                 ( 0,  0,  1)), {}),                                    # F5
        'Ff6': ((( 1,  2,  0), ( 0,  2,  0), ( 0,  1,  0), (-1,  1,  0),
                 ( 1,  2, -1)), {}),                                    # Fb1
        'Fg6': ((( 1,  2,  0), ( 0,  2,  0), ( 0,  1,  0), (-1,  1,  0),
                 ( 0,  2, -1)), {}),                                    # Fb2
        'Fh6': ((( 1,  2,  0), ( 0,  2,  0), ( 0,  1,  0), (-1,  1,  0),
                 ( 0,  1, -1)), {}),                                    # Fb3
        'Fi6': ((( 1,  2,  0), ( 0,  2,  0), ( 0,  1,  0), (-1,  1,  0),
                 (-1,  1, -1)), {}),                                    # Fb4
        'Fj6': ((( 1,  2,  0), ( 0,  2,  0), ( 0,  1,  0), (-1,  1,  0),
                 ( 0,  0, -1)), {}),                                    # Fb5
        # tetromino J plus two cubes out of plane:
        'Ja6': ((( 0,  2,  0), ( 0,  1,  0), (-1,  0,  0),
                 ( 0,  2,  1), (-1,  2,  1)), {}),                      # J1l
        'Jb6': ((( 0,  2,  0), ( 0,  1,  0), (-1,  0,  0),
                 ( 0,  2,  1), ( 1,  2,  1)), {}),                      # J1r
        'Jc6': ((( 0,  2,  0), ( 0,  1,  0), (-1,  0,  0),
                 ( 0,  1,  1), (-1,  1,  1)), {}),                      # J2l
        'Jd6': ((( 0,  2,  0), ( 0,  1,  0), (-1,  0,  0),
                 ( 0,  1,  1), ( 1,  1,  1)), {}),                      # J2r
        'Je6': ((( 0,  2,  0), ( 0,  1,  0), (-1,  0,  0),
                 ( 0,  0,  1), ( 1,  0,  1)), {}),                      # J3r
        'Jf6': ((( 0,  2,  0), ( 0,  1,  0), (-1,  0,  0),
                 (-1,  0,  1), (-2,  0,  1)), {}),                      # J4l
        'Jg6': ((( 0,  2,  0), ( 0,  1,  0), (-1,  0,  0),
                 (-1,  0,  1), (-1,  1,  1)), {}),                      # J4u
        'Jh6': ((( 0,  2,  0), ( 0,  1,  0), (-1,  0,  0),
                 (-1,  0,  1), (-1, -1,  1)), {}),                      # J4d
        'Ji6': ((( 0,  2,  0), ( 0,  1,  0), (-1,  0,  0),
                 (-1,  0,  1), (-1,  0,  2)), {}),                      # J4v
        # pentomino L plus one cube out of plane:
        'La6': ((( 0,  3,  0), ( 0,  2,  0), ( 0,  1,  0), ( 1,  0,  0),
                 ( 0,  3,  1)), {}),                                    # L1
        'Lb6': ((( 0,  3,  0), ( 0,  2,  0), ( 0,  1,  0), ( 1,  0,  0),
                 ( 0,  0,  1)), {}),                                    # L4
        'Lc6': ((( 0,  3,  0), ( 0,  2,  0), ( 0,  1,  0), ( 1,  0,  0),
                 ( 1,  0,  1)), {}),                                    # L5
        'Ld6': ((( 0,  3,  0), ( 0,  2,  0), ( 0,  1,  0), ( 1,  0,  0),
                 ( 0,  3, -1)), {}),                                    # Lb1
        'Le6': ((( 0,  3,  0), ( 0,  2,  0), ( 0,  1,  0), ( 1,  0,  0),
                 ( 1,  0, -1)), {}),                                    # Lb5
        # tetromino L plus two cubes out of plane:
        'Lf6': ((( 0,  2,  0), ( 0,  1,  0), ( 1,  0,  0),
                 ( 0,  2,  1), (-1,  2,  1)), {}),                      # L1l
        'Lg6': ((( 0,  2,  0), ( 0,  1,  0), ( 1,  0,  0),
                 ( 0,  2,  1), ( 1,  2,  1)), {}),                      # L1r
        'Lh6': ((( 0,  2,  0), ( 0,  1,  0), ( 1,  0,  0),
                 ( 0,  1,  1), (-1,  1,  1)), {}),                      # L2l
        'Li6': ((( 0,  2,  0), ( 0,  1,  0), ( 1,  0,  0),
                 ( 0,  1,  1), ( 1,  1,  1)), {}),                      # L2r
        'Lj6': ((( 0,  2,  0), ( 0,  1,  0), ( 1,  0,  0),
                 ( 0,  0,  1), (-1,  0,  1)), {}),                      # L3l
        'Lk6': ((( 0,  2,  0), ( 0,  1,  0), ( 1,  0,  0),
                 ( 1,  0,  1), ( 2,  0,  1)), {}),                      # L4r
        'Ll6': ((( 0,  2,  0), ( 0,  1,  0), ( 1,  0,  0),
                 ( 1,  0,  1), ( 1,  1,  1)), {}),                      # L4u
        'Lm6': ((( 0,  2,  0), ( 0,  1,  0), ( 1,  0,  0),
                 ( 1,  0,  1), ( 1, -1,  1)), {}),                      # L4d
        'Ln6': ((( 0,  2,  0), ( 0,  1,  0), ( 1,  0,  0),
                 ( 1,  0,  1), ( 1,  0,  2)), {}),                      # L4v
        # pentomino N plus one cube out of plane:
        'Na6': ((( 1,  3,  0), ( 1,  2,  0), ( 0,  2,  0), ( 0,  1,  0),
                 ( 1,  3,  1)), {}),                                    # N1
        'Nb6': ((( 1,  3,  0), ( 1,  2,  0), ( 0,  2,  0), ( 0,  1,  0),
                 ( 1,  2,  1)), {}),                                    # N2
        'Nc6': ((( 1,  3,  0), ( 1,  2,  0), ( 0,  2,  0), ( 0,  1,  0),
                 ( 0,  2,  1)), {}),                                    # N3
        'Nd6': ((( 1,  3,  0), ( 1,  2,  0), ( 0,  2,  0), ( 0,  1,  0),
                 ( 0,  1,  1)), {}),                                    # N4
        'Ne6': ((( 1,  3,  0), ( 1,  2,  0), ( 0,  2,  0), ( 0,  1,  0),
                 ( 0,  0,  1)), {}),                                    # N5
        'Nf6': ((( 1,  3,  0), ( 1,  2,  0), ( 0,  2,  0), ( 0,  1,  0),
                 ( 1,  3, -1)), {}),                                    # Nb1
        'Ng6': ((( 1,  3,  0), ( 1,  2,  0), ( 0,  2,  0), ( 0,  1,  0),
                 ( 1,  2, -1)), {}),                                    # Nb2
        'Nh6': ((( 1,  3,  0), ( 1,  2,  0), ( 0,  2,  0), ( 0,  1,  0),
                 ( 0,  2, -1)), {}),                                    # Nb3
        'Ni6': ((( 1,  3,  0), ( 1,  2,  0), ( 0,  2,  0), ( 0,  1,  0),
                 ( 0,  1, -1)), {}),                                    # Nb4
        'Nj6': ((( 1,  3,  0), ( 1,  2,  0), ( 0,  2,  0), ( 0,  1,  0),
                 ( 0,  0, -1)), {}),                                    # Nb5
        # tetromino N plus two cubes out of plane:
        'Nk6': ((( 1,  2,  0), ( 1,  1,  0), ( 0,  1,  0),
                 ( 1,  2,  1), ( 0,  1,  1)), {}),                      # N13
        'Nl6': ((( 1,  2,  0), ( 1,  1,  0), ( 0,  1,  0),
                 ( 1,  2,  1), ( 0,  0,  1)), {}),                      # N14
        'Nm6': ((( 1,  2,  0), ( 1,  1,  0), ( 0,  1,  0),
                 ( 1,  2,  1), ( 0,  2,  1)), {}),                      # N1l
        'Nn6': ((( 1,  2,  0), ( 1,  1,  0), ( 0,  1,  0),
                 ( 1,  2,  1), ( 2,  2,  1)), {}),                      # N1r
        'No6': ((( 1,  2,  0), ( 1,  1,  0), ( 0,  1,  0),
                 ( 1,  2,  1), ( 1,  3,  1)), {}),                      # N1u
        'Np6': ((( 1,  2,  0), ( 1,  1,  0), ( 0,  1,  0),
                 ( 1,  2,  1), ( 0,  1, -1)), {}),                      # N1b3
        'Nq6': ((( 1,  2,  0), ( 1,  1,  0), ( 0,  1,  0),
                 ( 1,  2,  1), ( 0,  0, -1)), {}),                      # N1b4
        'Nr6': ((( 1,  2,  0), ( 1,  1,  0), ( 0,  1,  0),
                 ( 1,  1,  1), ( 0,  1,  1)), {}),                      # N23
        'Ns6': ((( 1,  2,  0), ( 1,  1,  0), ( 0,  1,  0),
                 ( 1,  1,  1), ( 2,  1,  1)), {}),                      # N2r
        'Nt6': ((( 1,  2,  0), ( 1,  1,  0), ( 0,  1,  0),
                 ( 1,  1,  1), ( 0,  1, -1)), {}),                      # N2b3
        'Nu6': ((( 1,  2,  0), ( 1,  1,  0), ( 0,  1,  0),
                 ( 1,  1,  1), ( 0,  0, -1)), {}),                      # N2b4
        # pentomino P plus one cube out of plane:
        'Pa6': ((( 0,  2,  0), ( 1,  2,  0), ( 0,  1,  0), ( 1,  1,  0),
                 ( 0,  2,  1)), {}),                                    # P1
        'Pb6': ((( 0,  2,  0), ( 1,  2,  0), ( 0,  1,  0), ( 1,  1,  0),
                 ( 1,  2,  1)), {}),                                    # P2
        'Pc6': ((( 0,  2,  0), ( 1,  2,  0), ( 0,  1,  0), ( 1,  1,  0),
                 ( 0,  1,  1)), {}),                                    # P3
        'Pd6': ((( 0,  2,  0), ( 1,  2,  0), ( 0,  1,  0), ( 1,  1,  0),
                 ( 1,  1,  1)), {}),                                    # P4
        'Pe6': ((( 0,  2,  0), ( 1,  2,  0), ( 0,  1,  0), ( 1,  1,  0),
                 ( 0,  0,  1)), {}),                                    # P5
        'Pf6': ((( 0,  2,  0), ( 1,  2,  0), ( 0,  1,  0), ( 1,  1,  0),
                 ( 0,  2, -1)), {}),                                    # Pb1
        'Pg6': ((( 0,  2,  0), ( 1,  2,  0), ( 0,  1,  0), ( 1,  1,  0),
                 ( 1,  2, -1)), {}),                                    # Pb2
        'Ph6': ((( 0,  2,  0), ( 1,  2,  0), ( 0,  1,  0), ( 1,  1,  0),
                 ( 0,  1, -1)), {}),                                    # Pb3
        'Pi6': ((( 0,  2,  0), ( 1,  2,  0), ( 0,  1,  0), ( 1,  1,  0),
                 ( 1,  1, -1)), {}),                                    # Pb4
        'Pj6': ((( 0,  2,  0), ( 1,  2,  0), ( 0,  1,  0), ( 1,  1,  0),
                 ( 0,  0, -1)), {}),                                    # Pb5
        # tetromino O plus two cubes out of plane:
        'Qa6': ((( 0,  1,  0), ( 1,  1,  0), ( 1,  0,  0),
                 ( 0,  1,  1), ( 1,  0,  1)), {}),                      # Q14
        'Qb6': ((( 0,  1,  0), ( 1,  1,  0), ( 1,  0,  0),
                 ( 1,  0,  1), ( 2,  0,  1)), {}),                      # Q4r
        'Qc6': ((( 0,  1,  0), ( 1,  1,  0), ( 1,  0,  0),
                 ( 1,  0,  1), ( 1, -1,  1)), {}),                      # Q4d
        'Qd6': ((( 0,  1,  0), ( 1,  1,  0), ( 1,  0,  0),
                 ( 1,  0,  1), ( 1,  0,  2)), {}),                      # Q4v
        'Qe6': ((( 0,  1,  0), ( 1,  1,  0), ( 1,  0,  0),
                 ( 1,  0,  1), ( 0,  1, -1)), {}),                      # Q4b1
        # tetromino S plus two cubes out of plane:
        'Sa6': (((-1,  2,  0), (-1,  1,  0), ( 0,  1,  0),
                 (-1,  2,  1), ( 0,  1,  1)), {}),                      # S13
        'Sb6': (((-1,  2,  0), (-1,  1,  0), ( 0,  1,  0),
                 (-1,  2,  1), ( 0,  0,  1)), {}),                      # S14
        'Sc6': (((-1,  2,  0), (-1,  1,  0), ( 0,  1,  0),
                 (-1,  2,  1), (-2,  2,  1)), {}),                      # S1l
        'Sd6': (((-1,  2,  0), (-1,  1,  0), ( 0,  1,  0),
                 (-1,  2,  1), ( 0,  2,  1)), {}),                      # S1r
        'Se6': (((-1,  2,  0), (-1,  1,  0), ( 0,  1,  0),
                 (-1,  2,  1), (-1,  3,  1)), {}),                      # S1u
        'Sf6': (((-1,  2,  0), (-1,  1,  0), ( 0,  1,  0),
                 (-1,  1,  1), ( 0,  1,  1)), {}),                      # S23
        'Sg6': (((-1,  2,  0), (-1,  1,  0), ( 0,  1,  0),
                 (-1,  1,  1), (-2,  1,  1)), {}),                      # S2l
        'Sh6': (((-1,  2,  0), (-1,  1,  0), ( 0,  1,  0),
                 (-1,  1,  1), (-1,  0,  1)), {}),                      # S2d
        # pentomino T plus one cube out of plane:
        'Ta6': (((-1,  2,  0), ( 0,  2,  0), ( 1,  2,  0), ( 0,  1,  0),
                 (-1,  2,  1)), {}),                                    # T1
        'Tb6': (((-1,  2,  0), ( 0,  2,  0), ( 1,  2,  0), ( 0,  1,  0),
                 ( 0,  2,  1)), {}),                                    # T2
        'Tc6': (((-1,  2,  0), ( 0,  2,  0), ( 1,  2,  0), ( 0,  1,  0),
                 ( 1,  2,  1)), {}),                                    # T3
        'Td6': (((-1,  2,  0), ( 0,  2,  0), ( 1,  2,  0), ( 0,  1,  0),
                 ( 0,  1,  1)), {}),                                    # T4
        'Te6': (((-1,  2,  0), ( 0,  2,  0), ( 1,  2,  0), ( 0,  1,  0),
                 ( 0,  0,  1)), {}),                                    # T5
        # tetromino T plus two cubes out of plane:
        'Tf6': (((-1,  1,  0), ( 0,  1,  0), ( 1,  1,  0),
                 (-1,  1,  1), (-1,  2,  1)), {}),                      # T1u
        'Tg6': (((-1,  1,  0), ( 0,  1,  0), ( 1,  1,  0),
                 (-1,  1,  1), (-1,  0,  1)), {}),                      # T1d
        'Th6': (((-1,  1,  0), ( 0,  1,  0), ( 1,  1,  0),
                 ( 0,  1,  1), ( 0,  0,  1)), {}),                      # T24
        'Ti6': (((-1,  1,  0), ( 0,  1,  0), ( 1,  1,  0),
                 ( 0,  1,  1), ( 0,  2,  1)), {}),                      # T2u
        'Tj6': (((-1,  1,  0), ( 0,  1,  0), ( 1,  1,  0),
                 ( 1,  1,  1), ( 1,  2,  1)), {}),                      # T3u
        'Tk6': (((-1,  1,  0), ( 0,  1,  0), ( 1,  1,  0),
                 ( 1,  1,  1), ( 1,  0,  1)), {}),                      # T3d
        'Tl6': (((-1,  1,  0), ( 0,  1,  0), ( 1,  1,  0),
                 ( 0,  0,  1), (-1,  0,  1)), {}),                      # T4l
        'Tm6': (((-1,  1,  0), ( 0,  1,  0), ( 1,  1,  0),
                 ( 0,  0,  1), ( 1,  0,  1)), {}),                      # T4r
        'Tn6': (((-1,  1,  0), ( 0,  1,  0), ( 1,  1,  0),
                 ( 0,  0,  1), ( 0, -1,  1)), {}),                      # T4d
        'To6': (((-1,  1,  0), ( 0,  1,  0), ( 1,  1,  0),
                 ( 0,  0,  1), ( 0,  0,  2)), {}),                      # T4v
        'Tp6': (((-1,  1,  0), ( 0,  1,  0), ( 1,  1,  0),
                 ( 0,  0,  1), ( 0,  0, -1)), {}),                      # T4b4
        # pentomino U plus one cube out of plane:
        'Ua6': ((( 0,  1,  0), ( 1,  0,  0), ( 2,  0,  0), ( 2,  1,  0),
                 ( 0,  1,  1)), {}),                                    # U1
        'Ub6': ((( 0,  1,  0), ( 1,  0,  0), ( 2,  0,  0), ( 2,  1,  0),
                 ( 0,  0,  1)), {}),                                    # U2
        'Uc6': ((( 0,  1,  0), ( 1,  0,  0), ( 2,  0,  0), ( 2,  1,  0),
                 ( 1,  0,  1)), {}),                                    # U3
        'Ud6': ((( 0,  1,  0), ( 1,  0,  0), ( 2,  0,  0), ( 2,  1,  0),
                 ( 2,  0,  1)), {}),                                    # U4
        'Ue6': ((( 0,  1,  0), ( 1,  0,  0), ( 2,  0,  0), ( 2,  1,  0),
                 ( 2,  1,  1)), {}),                                    # U5
        # pentomino V plus one cube out of plane:
        'Va6': ((( 0,  2,  0), ( 0,  1,  0), ( 1,  0,  0), ( 2,  0,  0),
                 ( 0,  2,  1)), {}),                                    # V1
        'Vb6': ((( 0,  2,  0), ( 0,  1,  0), ( 1,  0,  0), ( 2,  0,  0),
                 ( 0,  1,  1)), {}),                                    # V2
        'Vc6': ((( 0,  2,  0), ( 0,  1,  0), ( 1,  0,  0), ( 2,  0,  0),
                 ( 0,  0,  1)), {}),                                    # V3
        'Vd6': ((( 0,  2,  0), ( 0,  1,  0), ( 1,  0,  0), ( 2,  0,  0),
                 ( 1,  0,  1)), {}),                                    # V4
        'Ve6': ((( 0,  2,  0), ( 0,  1,  0), ( 1,  0,  0), ( 2,  0,  0),
                 ( 2,  0,  1)), {}),                                    # V5
        # tromino V plus another out of plane:
        'Vf6': ((( 0,  1,  0), ( 1,  0,  0),
                 ( 0,  1,  1), (-1,  1,  1), (-1,  2,  1)), {}),        # V1l
        'Vg6': ((( 0,  1,  0), ( 1,  0,  0),
                 ( 0,  1,  1), (-1,  1,  1), (-1,  0,  1)), {}),        # V1d
        'Vh6': ((( 0,  1,  0), ( 1,  0,  0),
                 ( 1,  0,  1), ( 1, -1,  1), ( 2, -1,  1)), {}),        # V3r
        'Vi6': ((( 0,  1,  0), ( 1,  0,  0),
                 ( 1,  0,  1), ( 1, -1,  1), ( 0, -1,  1)), {}),        # V3d
        # pentomino W plus one cube out of plane:
        'Wa6': (((-1,  2,  0), (-1,  1, 0), ( 0,  1,  0), ( 1,  0,  0),
                 (-1,  2,  1)), {}),                                    # W1
        'Wb6': (((-1,  2,  0), (-1,  1, 0), ( 0,  1,  0), ( 1,  0,  0),
                 (-1,  1,  1)), {}),                                    # W2
        'Wc6': (((-1,  2,  0), (-1,  1, 0), ( 0,  1,  0), ( 1,  0,  0),
                 ( 0,  1,  1)), {}),                                    # W3
        'Wd6': (((-1,  2,  0), (-1,  1, 0), ( 0,  1,  0), ( 1,  0,  0),
                 ( 0,  0,  1)), {}),                                    # W4
        'We6': (((-1,  2,  0), (-1,  1, 0), ( 0,  1,  0), ( 1,  0,  0),
                 ( 1,  0,  1)), {}),                                    # W5
        # pentomino X plus one cube out of plane:
        'Xa6': ((( 0,  2,  0), (-1,  1,  0), ( 0,  1,  0), ( 1,  1,  0),
                 ( 0,  2,  1)), {}),                                    # X1
        'Xb6': ((( 0,  2,  0), (-1,  1,  0), ( 0,  1,  0), ( 1,  1,  0),
                 ( 0,  1,  1)), {}),                                    # X3
        # pentomino Y plus one cube out of plane:
        'Ya6': ((( 0,  3,  0), (-1,  2,  0), ( 0,  2,  0), ( 0,  1,  0),
                 ( 0,  3,  1)), {}),                                    # Y1
        'Yb6': ((( 0,  3,  0), (-1,  2,  0), ( 0,  2,  0), ( 0,  1,  0),
                 (-1,  2,  1)), {}),                                    # Y2
        'Yc6': ((( 0,  3,  0), (-1,  2,  0), ( 0,  2,  0), ( 0,  1,  0),
                 ( 0,  2,  1)), {}),                                    # Y3
        'Yd6': ((( 0,  3,  0), (-1,  2,  0), ( 0,  2,  0), ( 0,  1,  0),
                 ( 0,  1,  1)), {}),                                    # Y4
        'Ye6': ((( 0,  3,  0), (-1,  2,  0), ( 0,  2,  0), ( 0,  1,  0),
                 ( 0,  0,  1)), {}),                                    # Y5
        'Yf6': ((( 0,  3,  0), (-1,  2,  0), ( 0,  2,  0), ( 0,  1,  0),
                 ( 0,  3, -1)), {}),                                    # Yb1
        'Yg6': ((( 0,  3,  0), (-1,  2,  0), ( 0,  2,  0), ( 0,  1,  0),
                 (-1,  2, -1)), {}),                                    # Yb2
        'Yh6': ((( 0,  3,  0), (-1,  2,  0), ( 0,  2,  0), ( 0,  1,  0),
                 ( 0,  1, -1)), {}),                                    # Yb4
        'Yi6': ((( 0,  3,  0), (-1,  2,  0), ( 0,  2,  0), ( 0,  1,  0),
                 ( 0,  0, -1)), {}),                                    # Yb5
        # pentomino Z plus one cube out of plane:
        'Za6': (((-1,  2,  0), ( 0,  2,  0), ( 0,  1,  0), ( 1,  0,  0),
                 (-1,  2,  1)), {}),                                    # Z1
        'Zb6': (((-1,  2,  0), ( 0,  2,  0), ( 0,  1,  0), ( 1,  0,  0),
                 ( 0,  2,  1)), {}),                                    # Z2
        'Zc6': (((-1,  2,  0), ( 0,  2,  0), ( 0,  1,  0), ( 1,  0,  0),
                 ( 0,  1,  1)), {}),                                    # Z3
        'Zd6': (((-1,  2,  0), ( 0,  2,  0), ( 0,  1,  0), ( 1,  0,  0),
                 (-1,  2, -1)), {}),                                    # Zb1
        'Ze6': (((-1,  2,  0), ( 0,  2,  0), ( 0,  1,  0), ( 1,  0,  0),
                 ( 0,  2, -1)), {}),                                    # Zb2
        'Zf6': (((-1,  2,  0), ( 0,  2,  0), ( 0,  1,  0), ( 1,  0,  0),
                 ( 0,  1, -1)), {}),                                    # Zb3
        }
    """(0,0,0) is implied.  The names are partly based on Kadon's names (see
    http://gamepuzzles.com/sxnames.htm)."""

    piece_colors = {
        'Aa6': 'darkseagreen',
        'Ba6': 'peru',
        'Fa6': 'rosybrown',
        'Fb6': 'yellowgreen',
        'Fc6': 'steelblue',
        'Fd6': 'darkviolet',
        'Fe6': 'lightcoral',
        'Ff6': 'olive',
        'Fg6': 'teal',
        'Fh6': 'tan',
        'Fi6': 'indigo',
        'Fj6': 'darkkhaki',
        'Ja6': 'orangered',
        'Jb6': 'darkorchid',
        'Jc6': 'tomato',
        'Jd6': 'thistle',
        'Je6': 'cadetblue',
        'Jf6': 'darkseagreen',
        'Jg6': 'peru',
        'Jh6': 'rosybrown',
        'Ji6': 'yellowgreen',
        'La6': 'steelblue',
        'Lb6': 'darkviolet',
        'Lc6': 'lightcoral',
        'Ld6': 'olive',
        'Le6': 'teal',
        'Lf6': 'tan',
        'Lg6': 'indigo',
        'Lh6': 'darkkhaki',
        'Li6': 'orangered',
        'Lk6': 'darkorchid',
        'Ll6': 'tomato',
        'Lm6': 'thistle',
        'Ln6': 'cadetblue',
        'Lo6': 'darkseagreen',
        'Na6': 'peru',
        'Nb6': 'rosybrown',
        'Nc6': 'yellowgreen',
        'Nd6': 'steelblue',
        'Ne6': 'darkviolet',
        'Nf6': 'lightcoral',
        'Ng6': 'olive',
        'Nh6': 'teal',
        'Ni6': 'tan',
        'Nj6': 'indigo',
        'Nk6': 'darkkhaki',
        'Nl6': 'orangered',
        'Nm6': 'darkorchid',
        'Nn6': 'tomato',
        'No6': 'thistle',
        'Np6': 'cadetblue',
        'Nq6': 'darkseagreen',
        'Nr6': 'peru',
        'Ns6': 'rosybrown',
        'Nt6': 'yellowgreen',
        'Nu6': 'steelblue',
        'Pa6': 'darkviolet',
        'Pb6': 'lightcoral',
        'Pc6': 'olive',
        'Pd6': 'teal',
        'Pe6': 'tan',
        'Pf6': 'indigo',
        'Pg6': 'darkkhaki',
        'Ph6': 'orangered',
        'Pi6': 'darkorchid',
        'Pj6': 'tomato',
        'Qa6': 'thistle',
        'Qb6': 'cadetblue',
        'Qc6': 'darkseagreen',
        'Qd6': 'peru',
        'Qe6': 'rosybrown',
        'Sa6': 'yellowgreen',
        'Sb6': 'steelblue',
        'Sc6': 'darkviolet',
        'Sd6': 'lightcoral',
        'Se6': 'olive',
        'Sf6': 'teal',
        'Sg6': 'tan',
        'Sh6': 'indigo',
        'Ta6': 'darkkhaki',
        'Tb6': 'orangered',
        'Tc6': 'darkorchid',
        'Td6': 'tomato',
        'Te6': 'thistle',
        'Tf6': 'cadetblue',
        'Tg6': 'darkseagreen',
        'Th6': 'peru',
        'Ti6': 'rosybrown',
        'Tj6': 'yellowgreen',
        'Tk6': 'steelblue',
        'Tl6': 'darkviolet',
        'Tm6': 'lightcoral',
        'Tn6': 'olive',
        'To6': 'teal',
        'Tp6': 'tan',
        'Ua6': 'indigo',
        'Ub6': 'darkkhaki',
        'Uc6': 'orangered',
        'Ud6': 'darkorchid',
        'Ue6': 'tomato',
        'Va6': 'thistle',
        'Vb6': 'cadetblue',
        'Vc6': 'darkseagreen',
        'Vd6': 'peru',
        'Ve6': 'rosybrown',
        'Vf6': 'yellowgreen',
        'Vg6': 'steelblue',
        'Vh6': 'darkviolet',
        'Vi6': 'lightcoral',
        'Wa6': 'olive',
        'Wb6': 'teal',
        'Wc6': 'tan',
        'Wd6': 'indigo',
        'We6': 'darkkhaki',
        'Xa6': 'orangered',
        'Xb6': 'darkorchid',
        'Ya6': 'tomato',
        'Yb6': 'thistle',
        'Yc6': 'cadetblue',
        'Yd6': 'darkseagreen',
        'Ye6': 'peru',
        'Yf6': 'rosybrown',
        'Yg6': 'yellowgreen',
        'Yh6': 'steelblue',
        'Yi6': 'darkviolet',
        'Za6': 'lightcoral',
        'Zb6': 'olive',
        'Zc6': 'teal',
        'Zd6': 'tan',
        'Ze6': 'indigo',
        'Zf6': 'darkkhaki',
        '0':  'gray',
        '1':  'black'}

    # add solid hexominoes:
    for _name, (_data, _kwargs) in SolidHexominoes.piece_data.items():
        piece_data[_name] = (_data, _kwargs)
        piece_colors[_name] = SolidHexominoes.piece_colors[_name]
    del _name, _data, _kwargs

    # for format_solution:
    piece_width = 4


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


class Polycubes123456(Polycubes12345):

    piece_data = copy.deepcopy(Polycubes12345.piece_data)
    piece_data.update(copy.deepcopy(Hexacubes.piece_data))
    piece_colors = copy.deepcopy(Polycubes12345.piece_colors)
    piece_colors.update(Hexacubes.piece_colors)

    # for format_solution:
    piece_width = 4


class Polycubes12345p6(Polycubes12345):

    """
    Polycubes of order 1 - 5 (complete) & 6 (partial; 5 pieces).

    216 cubes total.
    """

    piece_data = copy.deepcopy(Polycubes12345.piece_data)
    piece_colors = copy.deepcopy(Polycubes12345.piece_colors)
    for _n in ('Ba6', 'O06', 'Tp6', 'Nt6', 'Qe6'):
        piece_data[_n] = copy.deepcopy(Hexacubes.piece_data[_n])
        piece_colors[_n] = Hexacubes.piece_colors[_n]
    del _n

    # for format_solution:
    piece_width = 4


class DigitCubes(Polycubes):

    """
    Based on the 'Digits In A Box' puzzle `designed by Eric Harshbarger`__ and
    `manufactured by Popular Playthings`__.

    __ http://www.ericharshbarger.org/puzzles/digits_in_a_box/
    __ http://www.popularplaythings.com/index.php?id_product=430&controller=product
    """

    piece_data = {
        'd0': (((0, 1, 0), (0, 2, 0), (0, 3, 0), (0, 4, 0),
                (1, 0, 0), (1, 4, 0),
                (2, 0, 0), (2, 1, 0), (2, 2, 0), (2, 3, 0), (2, 4, 0),), {}),
        'd1': (((0, 4, 0),
                (1, 0, 0), (1, 1, 0), (1, 2, 0), (1, 3, 0), (1, 4, 0),
                (2, 0, 0),), {}),
        'd2': (((0, 1, 0), (0, 2, 0), (0, 4, 0),
                (1, 0, 0), (1, 2, 0), (1, 4, 0),
                (2, 0, 0), (2, 2, 0), (2, 3, 0), (2, 4, 0),), {}),
        'd3': (((0, 2, 0), (0, 4, 0),
                (1, 0, 0), (1, 2, 0), (1, 4, 0),
                (2, 0, 0), (2, 1, 0), (2, 2, 0), (2, 3, 0), (2, 4, 0),), {}),
        'd4': (((-2, 2, 0), (-2, 3, 0), (-2, 4, 0),
                (-1, 2, 0),
                (0, 1, 0), (0, 2, 0), (0, 3, 0), (0, 4, 0),), {}),
        'd5': (((0, 2, 0), (0, 3, 0), (0, 4, 0),
                (1, 0, 0), (1, 2, 0), (1, 4, 0),
                (2, 0, 0), (2, 1, 0), (2, 2, 0), (2, 4, 0),), {}),
        'd6': (((0, 1, 0), (0, 2, 0), (0, 3, 0), (0, 4, 0),
                (1, 0, 0), (1, 2, 0), (1, 4, 0),
                (2, 0, 0), (2, 1, 0), (2, 2, 0), (2, 4, 0),), {}),
        'd7': (((-2, 3, 0), (-2, 4, 0),
                (-1, 4, 0),
                (0, 1, 0), (0, 2, 0), (0, 3, 0), (0, 4, 0),), {}),
        'd8': (((0, 1, 0), (0, 2, 0), (0, 3, 0), (0, 4, 0),
                (1, 0, 0), (1, 2, 0), (1, 4, 0),
                (2, 0, 0), (2, 1, 0), (2, 2, 0), (2, 3, 0), (2, 4, 0),), {}),
        'd9': (((0, 2, 0), (0, 3, 0), (0, 4, 0),
                (1, 0, 0), (1, 2, 0), (1, 4, 0),
                (2, 0, 0), (2, 1, 0), (2, 2, 0), (2, 3, 0), (2, 4, 0),), {}),}
    """(0,0,0) is implied."""

    internal_coords = {
        'd0': ((0, 1, 0), (0, 2, 0), (0, 3, 0),
               (1, 0, 0), (1, 1, 0), (1, 2, 0), (1, 3, 0), (1, 4, 0), 
               (2, 1, 0), (2, 2, 0), (2, 3, 0),),
        'd1': ((1, 1, 0), (1, 2, 0), (1, 3, 0),),
        'd2': ((0, 1, 0), (1, 2, 0), (2, 3, 0),),
        'd3': ((2, 1, 0), (2, 3, 0),),
        'd4': ((-1, 2, 0),),
        'd5': ((0, 3, 0), (1, 2, 0), (2, 1, 0),),
        'd6': ((0, 1, 0), (0, 3, 0), (1, 0, 0), (1, 1, 0), (1, 2, 0),
               (2, 1, 0),),
        'd7': ((-1, 4, 0),),
        'd8': ((0, 1, 0), (0, 3, 0),
               (1, 0, 0), (1, 1, 0), (1, 2, 0), (1, 3, 0), (1, 4, 0),
               (2, 1, 0), (2, 3, 0),),
        'd9': ((0, 3, 0), (1, 2, 0), (1, 3, 0), (1, 4, 0),
               (2, 1, 0), (2, 3, 0),),}
    """These are secondary coordinates, internal holes and inaccessible
    cubies, to prevent impossible solutions. Coordinates overlay `piece_data`
    coords."""

    piece_colors = {
        'd0': 'plum',
        'd1': 'red',
        'd2': 'black',
        'd3': 'gold',
        'd4': 'pink',
        'd5': 'steelblue',
        'd6': 'darkorange',
        'd7': 'darkgreen',
        'd8': 'violet',
        'd9': 'blue',
        '0': 'gray',
        '1': 'lightgray'}

    check_for_duplicates = False

    # for format_solution:
    piece_width = 3

    def build_matrix_header(self):
        Polycubes.build_matrix_header(self)
        headers = self.matrix[0]
        primary = len(headers)
        for (x, y, z) in sorted(self.solution_coords):
            header = '%0*i,%0*i,%0*ii' % (
                self.x_width, x, self.y_width, y, self.z_width, z)
            self.matrix_columns[header] = len(headers)
            headers.append(header)
        self.secondary_columns = len(headers) - primary

    #    ?
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
