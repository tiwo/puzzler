#!/usr/bin/env python
# $Id$

"""
Concrete polystick (orders 1 through 3) puzzles.
"""

from puzzler import coordsys
from puzzler.puzzles.polysticks import Polysticks123


class Polysticks123_4x4Corners(Polysticks123):

    """
    0 solutions
    """

    width = 4
    height = 4

    def coordinates(self):
        last_x = self.width - 1
        last_y = self.height - 1
        for y in range(self.height):
            for x in range(self.width):
                for z in range(self.depth):
                    if ( (z == 1 and y == last_y)
                         or (z == 0 and x == last_x)
                         or (x,y,z) in ((1,1,0),(1,1,1),(1,2,0),(2,1,1))):
                        continue
                    yield (x, y, z)
