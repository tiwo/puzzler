#!/usr/bin/env python
# $Id$

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2015 by David J. Goodger
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
        self.piece_data['P4'][-1]['rotations'] = None
        self.piece_data['P4'][-1]['flips'] = None
        self.piece_data['P4'][-1]['axes'] = None


class Tetracubes2x2x8(Tetracubes):

    """224 solutions"""

    width = 8
    height = 2
    depth = 2

    def customize_piece_data(self):
        self.piece_data['P4'][-1]['rotations'] = None
        self.piece_data['P4'][-1]['flips'] = None
        self.piece_data['P4'][-1]['axes'] = None


class Tetracubes2x2x2x4(Tetracubes):

    """10? solutions"""

    width = 4
    height = 5
    depth = 2

    transform_solution_matrix = Puzzle3D.swap_yz_transform

    def coordinates(self):
        coords = set(
            list(self.coordinates_cuboid(4, 2, 2))
            + list(self.coordinates_cuboid(4, 2, 2, offset=(0,3,0))))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P4'][-1]['rotations'] = None
        self.piece_data['P4'][-1]['flips'] = None
        self.piece_data['P4'][-1]['axes'] = None
        self.piece_data['L4'][-1]['rotations'] = (0,)
        self.piece_data['L4'][-1]['flips'] = None
        self.piece_data['L4'][-1]['axes'] = None

    def build_matrix(self):
        keys = sorted(self.pieces.keys())
        assert len(self.pieces['P4']) == 1
        coords, aspect = self.pieces['P4'][0]
        for x in range(3):
            translated = aspect.translate((x, 0, 0))
            self.build_matrix_row('P4', translated)
        keys.remove('P4')

        # assert len(self.pieces['L4']) == 1
        # coords, aspect = self.pieces['L4'][0]
        # for x in range(2):
        #     translated = aspect.translate((x, 3, 0))
        #     pprint(translated)
        #     self.build_matrix_row('L4', translated)
        # keys.remove('L4')

        self.build_regular_matrix(keys)
