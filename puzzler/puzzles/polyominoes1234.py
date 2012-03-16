#!/usr/bin/env python
# -*- coding: utf-8 -*-
# $Id$

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2012 by David J. Goodger
# License: GPL 2 (see __init__.py)

"""
Concrete polyomino (orders 1 through 4) puzzles.
"""

from puzzler.puzzles.polyominoes import Polyominoes1234, OneSidedPolyominoes1234


class Polyominoes1234SquarePlus(Polyominoes1234):

    """
    563 solutions

    Puzzle design from Kadon (Kate Jones).
    """

    width = 7
    height = 7

    extras = set(((0,3), (3,0), (3,6), (6,3)))

    def coordinates(self):
        coords = set(self.coordinates_rectangle(5, 5, offset=(1,1)))
        for x, y in self.extras:
            coords.add(self.coordinate_offset(x, y, None))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['L4'][-1]['rotations'] = None
        self.piece_data['L4'][-1]['flips'] = None


class Polyominoes1234Astroid(Polyominoes1234):

    """
    18 solutions

    Puzzle design from Kadon (Kate Jones).
    """

    width = 9
    height = 9

    holes = set(((2,2), (2,6), (6,2), (6,6)))

    def coordinates(self):
        coords = (
            set(list(self.coordinates_rectangle(5, 5, offset=(2,2)))
                + list(self.coordinates_rectangle(9, 1, offset=(0,4)))
                + list(self.coordinates_rectangle(1, 9, offset=(4,0))))
            - self.holes)
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['L4'][-1]['rotations'] = None
        self.piece_data['L4'][-1]['flips'] = None


class OneSidedPolyominoes1234Octagon(OneSidedPolyominoes1234):

    """many solutions"""

    width = 7
    height = 7

    holes = set(((-1,3), (3,-1), (3,7), (7,3)))

    def coordinates(self):
        coords = (
            set(self.coordinates_diamond(5, offset=(-1,-1)))
            - self.holes)
        return sorted(coords)


class Polyominoes1234Cross_x(Polyominoes1234):

    """0 solutions"""

    width = 7
    height = 7

    holes = set(((3,4), (4,3), (4,5), (5,4)))

    holes = set(((3,3), (3,5), (5,3), (5,5)))

    def coordinates(self):
        coords = (
            set(list(self.coordinates_rectangle(5, 5, offset=(2,2)))
               + list(self.coordinates_rectangle(9, 1, offset=(0,4)))
               + list(self.coordinates_rectangle(1, 9, offset=(4,0))))
            - self.holes)
        return sorted(coords)
