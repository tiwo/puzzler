#!/usr/bin/env python
# -*- coding: utf-8 -*-
# $Id$

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2015 by David J. Goodger
# License: GPL 2 (see __init__.py)

"""
Concrete polyomino (orders 2 through 5) puzzles.
"""

from puzzler.puzzles.polyominoes import Polyominoes2345, OneSidedPolyominoes2345


class Polyominoes2345X1(Polyominoes2345):

    """178,355,676 solutions"""

    height = 14
    width = 14

    holes = set(((5,6), (5,7), (6,5), (6,8), (7,5), (7,8), (8,6), (8,7)))

    svg_rotation = 45

    def coordinates(self):
        coords = set(
            list(self.coordinates_rectangle(14, 4, offset=(0,5)))
            + list(self.coordinates_rectangle(4, 14, offset=(5,0))))
        for coord in sorted(coords):
            if coord not in self.holes:
                yield coord

    def customize_piece_data(self):
        self.piece_data['P'][-1]['rotations'] = None
        self.piece_data['P'][-1]['flips'] = None
