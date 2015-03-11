#!/usr/bin/env python
# $Id$

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2015 by David J. Goodger
# License: GPL 2 (see __init__.py)

"""
Concrete seven-segment-digits polystick puzzles.
"""

from puzzler import coordsys
from puzzler.puzzles.polysticks import SevenSegmentDigits


class SevenSegmentDigits6x5(SevenSegmentDigits):

    """
    5 solutions (counting d2 & d5, and d6 & d9, as identical).

    This is the same as the Digigrams puzzle (AKA 'Count On Me' or 'Count Me
    In') designed by Martin H. Watson.
    """

    width = 6
    height = 5

    check_for_duplicates = True

    duplicate_conditions = ({'swapped_25': True},
                            {'swapped_69': True},
                            {'swapped_25': True, 'swapped_69': True})

    def customize_piece_data(self):
        self.piece_data['d7'][-1]['flips'] = None
        self.piece_data['d7'][-1]['rotations'] = (0, 1)


class UnflippedSevenSegmentDigits6x5(SevenSegmentDigits6x5):

    """
    0 solutions.

    There is no solution without a mirror-reversed (flipped) digit.
    """

    def customize_piece_data(self):
        for name in self.asymmetric_pieces:
            self.piece_data[name][-1]['flips'] = None
        self.piece_data['d9'][-1]['rotations'] = (0, 1)
