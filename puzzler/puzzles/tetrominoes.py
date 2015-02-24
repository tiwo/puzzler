#!/usr/bin/env python
# $Id$

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2015 by David J. Goodger
# License: GPL 2 (see __init__.py)

"""
Concrete tetromino puzzles.
"""

from puzzler.puzzles.polyominoes import Tetrominoes, OneSidedTetrominoes


class Tetrominoes5x4Tube(Tetrominoes):

    """
    7 solutions

    Short sides joined, forming a loop/tube.

    All solutions except one fit into the following shape::

        [][][][][]
        [][][][][]
        [][][][][]
          [][][][][]

    The exception fits into this shape::

        [][][][][]
        [][][][][]
          [][][][][]
        [][][][][]
    """

    width = 5
    height = 4

    def customize_piece_data(self):
        self.piece_data['L4'][-1]['flips'] = None
        self.piece_data['L4'][-1]['rotations'] = (0, 1)

    def build_matrix(self):
        for coords, aspect in self.pieces['L4']:
            for y in range(self.height - aspect.bounds[1]):
                translated = aspect.translate((0, y))
                self.build_matrix_row('L4', translated)
        keys = sorted(self.pieces.keys())
        keys.remove('L4')
        for key in keys:
            for coords, aspect in self.pieces[key]:
                for y in range(self.height - aspect.bounds[1]):
                    for x in range(self.width):
                        translated = aspect.translate((x, y), (self.width, 0))
                        self.build_matrix_row(key, translated)
