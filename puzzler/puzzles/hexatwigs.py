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


class HexatwigsHexagonRing(Hexatwigs):

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


class HexatwigsHexagonRing2(HexatwigsHexagonRing):

    """ solutions"""

    holes = set(((2,4,1), (2,7,2), (4,2,0), (4,7,0), (7,2,2), (7,4,1)))

    def customize_piece_data(self):
        self.piece_data['R06'][-1]['flips'] = None
        self.piece_data['R06'][-1]['rotations'] = None


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

    """ solutions"""

    height = 16
    width = 16

    svg_rotation = 0

    def coordinates(self):
        hole = set(self.coordinates_hexagon_unbordered(2, offset=(4,4,0)))
        for coord in self.coordinates_hexagon(6):
            if coord not in hole:
                yield coord

    def customize_piece_data(self):
        OneSidedHexatwigs.customize_piece_data(self)
        self.piece_data['R06'][-1]['rotations'] = None


class OneSidedHexatwigsElongatedHexagon26x2(OneSidedHexatwigs):

    """
     solutions

    Discovered by Peter F. Esser.
    """

    height = 4
    width = 28

    def coordinates(self):
        return self.coordinates_elongated_hexagon(26, 2)

    def customize_piece_data(self):
        OneSidedHexatwigs.customize_piece_data(self)
        self.piece_data['R06'][-1]['flips'] = None
        self.piece_data['R06'][-1]['rotations'] = (0, 1, 2)
