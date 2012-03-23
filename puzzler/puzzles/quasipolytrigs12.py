#!/usr/bin/env python
# -*- coding: utf-8 -*-
# $Id$

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2012 by David J. Goodger
# License: GPL 2 (see __init__.py)

"""
Concrete quasi-polytrigs (order 1 & 2) puzzles.
"""

from puzzler.puzzles.polytrigs import QuasiPolytrigs12, OneSidedQuasiPolytrigs12


class QuasiPolytrigs12ElongatedHexagon2x1(QuasiPolytrigs12):

    """542 solutions"""

    width = 4
    height = 3

    def coordinates(self):
        return self.coordinates_elongated_hexagon(2, 1)

    def customize_piece_data(self):
        self.piece_data['P12'][-1]['flips'] = None
        self.piece_data['P12'][-1]['rotations'] = (0, 1, 2)


class QuasiPolytrigs12Trapezoid5x1(QuasiPolytrigs12):

    """358 solutions"""

    width = 6
    height = 2

    def coordinates(self):
        return self.coordinates_trapezoid(5, 1)

    def customize_piece_data(self):
        self.piece_data['P12'][-1]['flips'] = None
