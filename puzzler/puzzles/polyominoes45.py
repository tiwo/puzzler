#!/usr/bin/env python
# -*- coding: utf-8 -*-
# $Id$

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2012 by David J. Goodger
# License: GPL 2 (see __init__.py)

"""
Concrete pentomino & tetromino (polyominoes of order 4 & 5) puzzles.
"""

from puzzler.puzzles.polyominoes import Polyominoes45, OneSidedPolyominoes45


class Polyominoes45_8x10(Polyominoes45):

    """many solutions"""

    width = 10
    height = 8

    def customize_piece_data(self):
        self.piece_data['P'][-1]['flips'] = None
        self.piece_data['P'][-1]['rotations'] = (0, 1)


class Polyominoes45_5x16(Polyominoes45_8x10):

    """many solutions"""

    width = 16
    height = 5


class Polyominoes45_4x20(Polyominoes45_8x10):

    """many solutions"""

    width = 20
    height = 4


class Polyominoes45Square(Polyominoes45):

    """many solutions"""

    width = 9
    height = 9

    hole = set(((4,4),))

    def coordinates(self):
        coords = set(self.coordinates_rectangle(9, 9)) - self.hole
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P'][-1]['rotations'] = None
        self.piece_data['P'][-1]['flips'] = None


class Polyominoes45Diamond(Polyominoes45):

    """7,302 solutions"""

    width = 13
    height = 13

    holes = set(((5,6), (6,5), (6,6), (6,7), (7,6)))

    def coordinates(self):
        coords = set(self.coordinates_diamond(7)) - self.holes
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P'][-1]['rotations'] = None
        self.piece_data['P'][-1]['flips'] = None


class Polyominoes45AztecDiamond(Polyominoes45):

    """11,162 solutions"""

    width = 12
    height = 12

    def coordinates(self):
        coords = (
            set(self.coordinates_aztec_diamond(6))
            - set(self.coordinates_rectangle(2, 2, offset=(5,5))))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P'][-1]['rotations'] = None
        self.piece_data['P'][-1]['flips'] = None
