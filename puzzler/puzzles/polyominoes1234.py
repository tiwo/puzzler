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


class Polyominoes1234_7x3Plus(Polyominoes1234):

    """
    17 solutions

    Discovered by Dan Klarskov.
    """

    width = 11
    height = 7

    def coordinates(self):
        coords = set(
            list(self.coordinates_rectangle(7, 3, offset=(2,2)))
            + list(self.coordinates_rectangle(11, 1, offset=(0,3)))
            + list(self.coordinates_rectangle(1, 7, offset=(5,0))))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['L4'][-1]['rotations'] = (0, 1)
        self.piece_data['L4'][-1]['flips'] = None

class Polyominoes1234_7x4PlusOne(Polyominoes1234):

    """
    1,522 solutions

    Discovered by Dan Klarskov.
    """

    width = 7
    height = 6

    def coordinates(self):
        coords = set(self.coordinates_rectangle(7, 4))
        coords.add(self.coordinate_offset(3, 5, None))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['L4'][-1]['rotations'] = (0, 1)
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


class Polyominoes1234SkeweredSquare(Polyominoes1234):

    """
    1,320 solutions

    Puzzle design by Dan Klarskov.
    """

    width = 9
    height = 5

    def coordinates(self):
        coords = set(
            list(self.coordinates_rectangle(5, 5, offset=(2,0)))
            + list(self.coordinates_rectangle(9, 1, offset=(0,2))))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['L4'][-1]['rotations'] = (0, 1)
        self.piece_data['L4'][-1]['flips'] = None


class Polyominoes1234Skewered9x3(Polyominoes1234):

    """
    5,249 solutions

    Puzzle design by Dan Klarskov.
    """

    width = 11
    height = 3

    def coordinates(self):
        coords = set(
            list(self.coordinates_rectangle(9, 3, offset=(1,0)))
            + list(self.coordinates_rectangle(11, 1, offset=(0,1))))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['L4'][-1]['rotations'] = (0, 1)
        self.piece_data['L4'][-1]['flips'] = None


class Polyominoes1234Skewered7x3(Polyominoes1234):

    """747 solutions"""

    width = 15
    height = 3

    def coordinates(self):
        coords = set(
            list(self.coordinates_rectangle(7, 3, offset=(4,0)))
            + list(self.coordinates_rectangle(15, 1, offset=(0,1))))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['L4'][-1]['rotations'] = (0, 1)
        self.piece_data['L4'][-1]['flips'] = None


class Polyominoes1234_7x5CrossHole(Polyominoes1234):

    """
    19 solutions

    Puzzle design by Dan Klarskov.
    """

    width = 7
    height = 5

    holes = set(((1,2), (2,2), (3,1), (3,3), (4,2), (5,2)))

    def coordinates(self):
        coords = set(self.coordinates_rectangle(7, 5)) - self.holes
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['L4'][-1]['rotations'] = (0, 1)
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
