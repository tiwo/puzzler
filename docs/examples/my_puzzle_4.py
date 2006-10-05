#!/usr/bin/env python

import puzzler.puzzles
import puzzler.coordsys


class MyPuzzle(puzzler.puzzles.Pentominoes):

    height = 3
    width = 21

    def build_matrix(self):
        keys = sorted(self.pieces.keys())
        x_coords, x_aspect = self.pieces['X'][0]
        translated = x_aspect.translate((1, 0))
        self.build_matrix_row('X', translated)
        keys.remove('X')
        i_coords, i_aspect = self.pieces['I'][1]
        for x in range(3, 17):
            translated = i_aspect.translate((x, 0))
            self.build_matrix_row('I', translated)
        keys.remove('I')
        self.build_regular_matrix(keys)

    def coordinates(self):
        holes = set(((4,1), (10,1), (16,1)))
        for y in range(self.height):
            for x in range(self.width):
                if (x,y) not in holes:
                    yield puzzler.coordsys.Cartesian2D((x, y))


if __name__ == '__main__':
    puzzler.run(MyPuzzle)
