#!/usr/bin/env python
# $Id$

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2012 by David J. Goodger
# License: GPL 2 (see __init__.py)

"""
Concrete tetracube puzzles.
"""

from puzzler.puzzles import Puzzle3D
from puzzler.puzzles.polycubes import Tetracubes


class Tetracubes2x4x4(Tetracubes):

    """1390 solutions"""

    width = 4
    height = 4
    depth = 2

    transform_solution_matrix = Puzzle3D.swap_yz_transform

    def customize_piece_data(self):
        self.piece_data['V2'][-1]['rotations'] = None
        self.piece_data['V2'][-1]['flips'] = None
        self.piece_data['V2'][-1]['axes'] = None


class Tetracubes2x2x8(Tetracubes):

    """224 solutions"""

    width = 8
    height = 2
    depth = 2

    def customize_piece_data(self):
        self.piece_data['V2'][-1]['rotations'] = None
        self.piece_data['V2'][-1]['flips'] = None
        self.piece_data['V2'][-1]['axes'] = None
