#!/usr/bin/env python
# -*- coding: utf-8 -*-
# $Id$

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2012 by David J. Goodger
# License: GPL 2 (see __init__.py)

"""
Concrete polytwig (orders 1 through 3) puzzles.
"""

from puzzler.puzzles.polytwigs import Polytwigs123, OneSidedPolytwigs123


class OneSidedPolytwigs123Triangle(OneSidedPolytwigs123):

    """3 solutions"""

    height = 3
    width = 3

    def coordinates(self):
        return self.coordinates_triangle(2)

    def customize_piece_data(self):
        OneSidedPolytwigs123.customize_piece_data(self)
        self.piece_data['C3'][-1]['rotations'] = (1,)
