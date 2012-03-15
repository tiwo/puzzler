#!/usr/bin/env python
# -*- coding: utf-8 -*-
# $Id$

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2012 by David J. Goodger
# License: GPL 2 (see __init__.py)

"""
Concrete polyomino (orders 2 through 4) puzzles.
"""

from puzzler.puzzles.polyominoes import Polyominoes234, OneSidedPolyominoes234


class OneSidedPolyominoes234Square(OneSidedPolyominoes234):

    """many solutions"""

    width = 6
    height = 6


class OneSidedPolyominoes234Octagon(OneSidedPolyominoes234):

    """many solutions"""

    width = 7
    height = 7

    holes = set(((-1,3), (3,-1), (3,7), (7,3), (3,3)))

    def coordinates(self):
        coords = (
            set(self.coordinates_diamond(5, offset=(-1,-1)))
            - self.holes)
        return sorted(coords)
