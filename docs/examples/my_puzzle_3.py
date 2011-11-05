#!/usr/bin/env python

import puzzler.coordsys
from puzzler.puzzles.polyominoes import Pentominoes


class MyPuzzle(Pentominoes):

    height = 3
    width = 21

    def customize_piece_data(self):
        self.piece_data['V'][-1]['flips'] = None
        self.piece_data['V'][-1]['rotations'] = None

    def coordinates(self):
        holes = set(((4,1), (10,1), (16,1)))
        for y in range(self.height):
            for x in range(self.width):
                if (x,y) not in holes:
                    yield puzzler.coordsys.Cartesian2D((x, y))


if __name__ == '__main__':
    puzzler.run(MyPuzzle)
