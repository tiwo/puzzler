#!/usr/bin/env python
# $Id$

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2012 by David J. Goodger
# License: GPL 2 (see __init__.py)

"""
Concrete polyhex (order 3 & 4) puzzles.
"""

from puzzler.puzzles.polyhexes import Polyhexes34


class Polyhexes34Hexagon(Polyhexes34):

    """12,290 solutions"""

    width = 7
    height = 7

    def coordinates(self):
        return self.coordinates_hexagon(4)

    def customize_piece_data(self):
        self.piece_data['P4'][-1]['flips'] = None
        self.piece_data['P4'][-1]['rotations'] = None


class Polyhexes34Hexagram(Polyhexes34):

    """167 solutions"""

    width = 9
    height = 9

    def coordinates(self):
        return self.coordinates_hexagram(3)

    def customize_piece_data(self):
        self.piece_data['P4'][-1]['flips'] = None
        self.piece_data['P4'][-1]['rotations'] = None




class Polyhexes34TrilobedCrown1(Polyhexes34):

    """127 solutions"""

    height = 9
    width = 9

    extras = ((1,4), (7,1), (4,7))

    holes = set(((3,5), (4,3), (5,4)))

    svg_rotation = -30

    def coordinates(self):
        for coord in self.coordinates_hexagram(3):
            if coord not in self.holes:
                yield coord
        for (x,y) in self.extras:
            yield self.coordinate_offset(x, y, None)

    def customize_piece_data(self):
        self.piece_data['P4'][-1]['flips'] = None
        self.piece_data['P4'][-1]['rotations'] = (0, 1)


class Polyhexes34TrilobedCrown2(Polyhexes34TrilobedCrown1):

    """159 solutions"""

    holes = set(((3,4), (4,5), (5,3)))
