#!/usr/bin/env python
# -*- coding: utf-8 -*-
# $Id$

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2012 by David J. Goodger
# License: GPL 2 (see __init__.py)

"""
Concrete polyomino (orders 1 through 3) puzzles.
"""

from puzzler.puzzles.polyominoes import Polyominoes123


class Polyominoes123Square(Polyominoes123):

    """6 solutions"""

    width = 3
    height = 3

    def customize_piece_data(self):
        self.piece_data['V3'][-1]['rotations'] = (0, 2)
        self.piece_data['V3'][-1]['flips'] = None

    def build_matrix(self):
        keys = sorted(self.pieces.keys())
        coords, aspect = self.pieces['I3'][0]
        self.build_matrix_row('I3', aspect)
        keys.remove('I3')
        self.build_regular_matrix(keys)
