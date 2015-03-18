#!/usr/bin/env python
# $Id$

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2015 by David J. Goodger
# License: GPL 2 (see __init__.py)

"""
Concrete polyiamonds (orders 1 through 7) puzzles.
"""

from puzzler.puzzles.polyiamonds import (
    Polyiamonds1234567, OneSidedPolyiamonds1234567)


class Polyiamonds1234567Hexagon1(Polyiamonds1234567):

    """many solutions"""

    height = 14
    width = 14

    holes = (set(Polyiamonds1234567.coordinates_diamond(2, (5,5,0)))
             .union(set(Polyiamonds1234567.coordinates_diamond(2, (7,5,0)))))
                
    def coordinates(self):
        coords = set(self.coordinates_hexagon(7)) - self.holes
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P5'][-1]['flips'] = None
        self.piece_data['P5'][-1]['rotations'] = (0,1,2)


class Polyiamonds1234567Hexagon2(Polyiamonds1234567Hexagon1):

    holes = (set(Polyiamonds1234567.coordinates_diamond(2, (5,7,0)))
             .union(set(Polyiamonds1234567.coordinates_diamond(2, (7,3,0)))))


class Polyiamonds1234567Hexagon3(Polyiamonds1234567Hexagon1):

    holes = (set(Polyiamonds1234567.coordinates_hexagon(2, (5,5,0)))
             - set(Polyiamonds1234567.coordinates_diamond(2, (6,5,0))))


class Polyiamonds1234567Hexagon4(Polyiamonds1234567Hexagon1):

    holes = (
        (set(Polyiamonds1234567.coordinates_elongated_hexagon(1, 2, (4,5,0)))
         - set(set(Polyiamonds1234567.coordinates_diamond(2, (4,5,0)))))
        .union(
        (set(Polyiamonds1234567.coordinates_elongated_hexagon(1, 2, (7,5,0)))
         - set(set(Polyiamonds1234567.coordinates_diamond(2, (8,5,0)))))))


class Polyiamonds1234567Hexagon5(Polyiamonds1234567Hexagon1):

    holes = (
        set(Polyiamonds1234567.coordinates_elongated_hexagon(3, 1, (5,6,0)))
        .union(set(Polyiamonds1234567.coordinates_diamond(2, (6,5,0)))))


class Polyiamonds1234567ElongatedHexagon2x10_1(Polyiamonds1234567):

    """many solutions"""

    height = 20
    width = 12

    svg_rotation = 90

    holes = set(((5,10,1), (6,9,0)))
                
    def coordinates(self):
        coords = set(self.coordinates_elongated_hexagon(2, 10)) - self.holes
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P5'][-1]['flips'] = None
        self.piece_data['P5'][-1]['rotations'] = (0,1,2)


class Polyiamonds1234567Butterfly12x10_1(Polyiamonds1234567):

    """many solutions"""

    height = 20
    width = 22

    svg_rotation = 90

    holes = set(((10,10,1), (11,9,0)))
                
    def coordinates(self):
        coords = set(self.coordinates_butterfly(12, 10)) - self.holes
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P5'][-1]['flips'] = None
        self.piece_data['P5'][-1]['rotations'] = (0,1,2)
