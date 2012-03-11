#!/usr/bin/env python
# $Id$

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2012 by David J. Goodger
# License: GPL 2 (see __init__.py)

"""
Concrete polycube (order 1 through 5) puzzles.
"""

from puzzler.puzzles import Puzzle3D
from puzzler.puzzles.polycubes import Polycubes12345


class Polycubes12345_2x3x31(Polycubes12345):

    """ solutions"""

    width = 31
    height = 3
    depth = 2

    transform_solution_matrix = Puzzle3D.swap_yz_transform

    def customize_piece_data(self):
        self.piece_data['P4'][-1]['rotations'] = None
        self.piece_data['P4'][-1]['flips'] = None
        self.piece_data['P4'][-1]['axes'] = None
