#!/usr/bin/env python
# -*- coding: utf-8 -*-
# $Id$

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2012 by David J. Goodger
# License: GPL 2 (see __init__.py)

"""
Concrete hexatwig puzzles.
"""

from puzzler.puzzles.polytwigs import Hexatwigs, OneSidedHexatwigs


class HexatwigsTriangle(Hexatwigs):

    """at least 5 solutions, probably many more"""

    height = 10
    width = 10

    def coordinates(self):
        return self.coordinates_triangle(9)

    def customize_piece_data(self):
        self.piece_data['R06'][-1]['flips'] = None
        self.piece_data['R06'][-1]['rotations'] = (0,1)


class HexatwigsHexagonRing1(Hexatwigs):

    """
    many solutions

    Design by Peter F. Esser.
    """

    height = 10
    width = 10

    holes = set(((4,0,0), (4,0,1), (5,0,2), (5,8,1), (4,9,0), (4,9,2)))

    svg_rotation = 0

    def coordinates(self):
        hole = set(self.coordinates_hexagon_unbordered(3, offset=(2,2,0)))
        hole.update(self.holes)
        for coord in self.coordinates_hexagon(5):
            if coord not in hole:
                yield coord

    def customize_piece_data(self):
        self.piece_data['R06'][-1]['flips'] = None
        self.piece_data['R06'][-1]['rotations'] = (0, 1, 2)


class HexatwigsHexagonRing2(HexatwigsHexagonRing1):

    """many solutions"""

    holes = set(((2,4,1), (2,7,2), (4,2,0), (4,7,0), (7,2,2), (7,4,1)))

    def customize_piece_data(self):
        self.piece_data['R06'][-1]['flips'] = None
        self.piece_data['R06'][-1]['rotations'] = None


class HexatwigsHexagonRing3(HexatwigsHexagonRing2):

    """many solutions"""

    holes = set(((1,4,1), (1,8,2), (4,1,0), (4,8,0), (8,1,2), (8,4,1)))


class HexatwigsHexagonRing4(HexatwigsHexagonRing2):

    """many solutions"""

    holes = set(((1,6,0), (3,3,2), (3,7,1), (6,1,1), (6,6,2), (7,3,0)))


class HexatwigsElongatedHexagonRing(Hexatwigs):

    """
    many solutions

    Discovered by Peter F. Esser.
    """

    height = 10
    width = 10

    def coordinates(self):
        hole = set(self.coordinates_elongated_hexagon_unbordered(
            3, 2, offset=(2,3,0)))
        for coord in self.coordinates_elongated_hexagon(4, 5):
            if coord not in hole:
                yield coord

    def customize_piece_data(self):
        self.piece_data['R06'][-1]['flips'] = None
        self.piece_data['R06'][-1]['rotations'] = (0, 1, 2)


class OneSidedHexatwigsHexagonRing(OneSidedHexatwigs):

    """
    many solutions

    First solution discovered by Peter F. Esser, replicated in
    ``_find_all_solutions = False`` case below.
    """

    height = 12
    width = 12

    svg_rotation = 0

    def coordinates(self):
        hole = set(self.coordinates_hexagon_unbordered(2, offset=(4,4,0)))
        for coord in self.coordinates_hexagon(6):
            if coord not in hole:
                yield coord

    _find_known_solution = False

    if _find_known_solution:
        # Find a known solution (first found by Peter F. Esser).
        # Fix pieces in known positions:
        restrictions = {
            'O06': [(0, (5,10,0))],
            'I06': [(2, (11,1,0))],
            'U06': [(1, (9,2,0))],
            'V06': [(0, (9,3,0))],
            'M06': [(4, (1,3,0))],
            'Y06': [(1, (7,4,0))],
            'y06': [(0, (6,7,0))],
            'S06': [(0, (5,0,0))],
            's06': [(5, (8,6,0))],
            'l06': [(0, (0,5,0))],
            'L06': [(1, (4,8,0))],
            'J06': [(5, (9,5,0))],
            'j06': [(0, (0,10,0))],
            'H06': [(0, (2,4,0))],
            'h06': [(0, (3,9,0))],
            'R06': [(3, (2,8,0))],
            'r06': [(4, (1,9,0))],}

        def build_matrix(self):
            keys = sorted(self.pieces.keys())
            for key, details in sorted(self.restrictions.items()):
                for aspect_index, offset in details:
                    coords, aspect = self.pieces[key][aspect_index]
                    translated = aspect.translate(offset)
                    self.build_matrix_row(key, translated)
                    keys.remove(key)
            self.build_regular_matrix(keys)

    else:
        # General case
        def customize_piece_data(self):
            OneSidedHexatwigs.customize_piece_data(self)
            self.piece_data['R06'][-1]['rotations'] = None


class OneSidedHexatwigsElongatedHexagon26x2(OneSidedHexatwigs):

    """
    many solutions

    Discovered by Peter F. Esser.
    """

    height = 4
    width = 28

    def coordinates(self):
        return self.coordinates_elongated_hexagon(26, 2)

    _find_known_solution = True

    if _find_known_solution:
        # Find a known solution (first found by Peter F. Esser).
        # Fix pieces in known positions:
        restrictions = {
            'O06': [(0, (10,0,0))],
            'I06': [(1, (14,0,0))],
            'U06': [(1, (6,2,0))],
            'V06': [(5, (6,1,0))],
            'M06': [(5, (25,1,0))],
            'Y06': [(1, (5,0,0))],
            'y06': [(0, (7,0,0))],}

        def build_matrix(self):
            keys = sorted(self.pieces.keys())
            for key, details in sorted(self.restrictions.items()):
                for aspect_index, offset in details:
                    coords, aspect = self.pieces[key][aspect_index]
                    translated = aspect.translate(offset)
                    self.build_matrix_row(key, translated)
                    keys.remove(key)
            self.build_regular_matrix(keys)

    else:
        # General case
        def customize_piece_data(self):
            OneSidedHexatwigs.customize_piece_data(self)
            self.piece_data['R06'][-1]['rotations'] = (0, 1, 2)
