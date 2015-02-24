#!/usr/bin/env python
# $Id$

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2015 by David J. Goodger
# License: GPL 2 (see __init__.py)

"""
Concrete polytrig (orders 1 through 4) puzzles.
"""

from puzzler.puzzles.polytrigs import Polytrigs1234


class Polytrigs1234Trapezoid15x8(Polytrigs1234):

    """ solutions."""

    width = 16
    height = 9

    # create multiple sub-puzzles, each with O04 & I1 placed

    def coordinates(self):
        return self.coordinates_trapezoid(15, 8)

    def customize_piece_data(self):
        self.piece_data['P3'][-1]['flips'] = None
