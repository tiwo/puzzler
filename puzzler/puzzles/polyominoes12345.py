#!/usr/bin/env python
# -*- coding: utf-8 -*-
# $Id$

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2012 by David J. Goodger
# License: GPL 2 (see __init__.py)

"""
Concrete polyomino (orders 1 through 5) puzzles.
"""

from puzzler.puzzles.polyominoes import (
    Polyominoes12345, OneSidedPolyominoes12345)


class Polyominoes12345Diamond(Polyominoes12345):

    """
    many solutions

    Puzzle design from Kadon's 'Poly-5' (gamepuzzles.com/polycub2.htm#P5).
    """

    width = 15
    height = 15

    extras = set(((0,7), (7,0), (7,14), (14,7)))

    def coordinates(self):
        coords = set(self.coordinates_diamond(7, offset=(1,1)))
        for x, y in self.extras:
            coords.add(self.coordinate_offset(x, y, None))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P'][-1]['rotations'] = None
        self.piece_data['P'][-1]['flips'] = None


class Polyominoes12345Cross1(Polyominoes12345):

    """
    many solutions

    Puzzle design by Kadon.
    """

    width = 11
    height = 11

    def coordinates(self):
        coords = set(
            list(self.coordinates_rectangle(7, 7, offset=(2,2)))
            + list(self.coordinates_rectangle(11, 5, offset=(0,3))) 
            + list(self.coordinates_rectangle(5, 11, offset=(3,0))))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P'][-1]['rotations'] = None
        self.piece_data['P'][-1]['flips'] = None


class Polyominoes12345Cross2(Polyominoes12345):

    """many solutions"""

    width = 13
    height = 13

    def coordinates(self):
        coords = set(
            list(self.coordinates_rectangle(9, 9, offset=(2,2)))
            + list(self.coordinates_rectangle(13, 1, offset=(0,6))) 
            + list(self.coordinates_rectangle(1, 13, offset=(6,0))))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P'][-1]['rotations'] = None
        self.piece_data['P'][-1]['flips'] = None
