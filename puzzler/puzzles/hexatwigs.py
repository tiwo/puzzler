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
