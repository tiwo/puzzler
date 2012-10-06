#!/usr/bin/env python
# -*- coding: utf-8 -*-
# $Id$

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2012 by David J. Goodger
# License: GPL 2 (see __init__.py)

"""
Concrete polyomino (orders 1 through 6) puzzles.
"""

from puzzler.puzzles import polyominoes
from puzzler.puzzles.polyominoes import (
    Polyominoes123456, OneSidedPolyominoes123456)


class Polyominoes123456Star(Polyominoes123456):

    """
    Monomono, domino, & triominoes restricted to a central 3x3 square.

    Pentominoes & tetrominoes restricted to the middle ring, as per
    Polyominoes12345Diamond2.

    Hexominoes restricted to an outer ring.

    4,579 unique solutions for the pentominoes & tetrominoes (outer ring).
    6 unique solutions for the inner square.
    8 relative orientations.
    Total unique solutions: 219,792.

    many solutions

    Design by `Jack Wetterer and Chris Patterson, with symmetry refinements by
    Darian Jenkins <http://gamepuzzles.com/polystar.htm>`__, extending Kadon's
    'Poly-5' (gamepuzzles.com/polycub2.htm#P5).
    """

    width = 27
    height = 29

    def coordinates(self):
        self.inner_square_coords = set(
            self.coordinates_rectangle(3, 3, offset=(12,13)))
        coords_5 = set(
            list(self.coordinates_diamond(7, offset=(7,8)))
            + list(self.coordinates_rectangle(15, 1, offset=(6, 14)))
            + list(self.coordinates_rectangle(1, 15, offset=(13, 7))))
        self.middle_ring_coords = coords_5 - set(self.inner_square_coords)
        coords_6 = set(
            list(self.coordinates_rectangle(27, 1, offset=(0, 14)))
            + list(self.coordinates_rectangle(1, 29, offset=(13, 0))))
        for i in range(6):
            coords_6.update(set(self.coordinates_rectangle(
                23 - 4 * i, 3 + 4 * i, offset=(2 * i + 2, 13 - 2 * i))))
        self.outer_ring_coords = coords_6 - coords_5
        return sorted(coords_6)

    def customize_piece_data(self):
        self.piece_data['P06'][-1]['rotations'] = None
        self.piece_data['P06'][-1]['flips'] = None

    fixed_inner_pieces = True

    if fixed_inner_pieces:

        restrictions = {
            #name: [(aspect, offset), ...],
            'O1': [(0, (13, 14))],
            'I2': [(1, (13, 15))],
            'I3': [(0, (12, 13))],
            'V3': [(2, (13, 13))],
            'I4': [(1, ( 6, 14))],
            'L4': [(1, (13,  7))],
            'O4': [(0, (16, 12))],
            'T4': [(2, (11, 17))],
            'Z4': [(1, ( 9, 16))],
            'F':  [(5, (11,  9))],
            'I':  [(0, (13, 17))],
            'L':  [(3, (11, 15))],
            'N':  [(6, ( 8, 14))],
            'P':  [(0, (14, 17))],
            'T':  [(0, (18, 13))],
            'U':  [(1, (15, 14))],
            'V':  [(3, (12, 10))],
            'W':  [(3, ( 8, 11))],
            'X':  [(0, (15, 15,))],
            'Y':  [(0, (15, 10))],
            'Z':  [(3, (10, 11))],
            }

        def build_matrix(self):
            self.build_restricted_matrix()

    else:

        def build_matrix(self):
            self.build_regular_matrix(
                (polyominoes.Monomino.piece_data.keys()
                 + polyominoes.Domino.piece_data.keys()
                 + sorted(polyominoes.Trominoes.piece_data.keys())),
                sorted(self.inner_square_coords))
            self.build_regular_matrix(
                (sorted(polyominoes.Tetrominoes.piece_data.keys())
                 + sorted(polyominoes.Pentominoes.piece_data.keys())),
                sorted(self.middle_ring_coords))
            self.build_regular_matrix(
                sorted(polyominoes.Hexominoes.piece_data.keys()),
                sorted(self.outer_ring_coords))
