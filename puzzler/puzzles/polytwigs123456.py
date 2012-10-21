#!/usr/bin/env python
# -*- coding: utf-8 -*-
# $Id$

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2012 by David J. Goodger
# License: GPL 2 (see __init__.py)

"""
Concrete polytwig (orders 1 through 6) puzzles.
"""

from puzzler.puzzles import polytwigs
from puzzler.puzzles.polytwigs import Polytwigs123456, OneSidedPolytwigs123456
from puzzler.coordsys import HexagonalGrid3DCoordSet, HexagonalGrid3D


class Polytwigs123456ElongatedHexagon22x2(Polytwigs123456):

    """many solutions"""

    width = 24
    height = 4

    def coordinates(self):
        return self.coordinates_elongated_hexagon(22, 2)

    def customize_piece_data(self):
        self.piece_data['R5'][-1]['rotations'] = (0, 1, 2)
        self.piece_data['R5'][-1]['flips'] = None
