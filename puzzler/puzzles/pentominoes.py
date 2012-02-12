#!/usr/bin/env python
# $Id$

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2012 by David J. Goodger
# License: GPL 2 (see __init__.py)

"""
Concrete pentomino puzzles.
"""

from puzzler.puzzles.polyominoes import (
    Pentominoes, OneSidedPentominoes,
    PentominoesPlusMonomino, PentominoesPlusSquareTetromino)


class Pentominoes6x10(Pentominoes):

    """2339 solutions"""

    height = 6
    width = 10

    def build_matrix(self):
        keys = sorted(self.pieces.keys())
        x_coords, x_aspect = self.pieces['X'][0]
        for y in range(2):
            for x in range(y==0, 4):
                translated = x_aspect.translate((x, y))
                self.build_matrix_row('X', translated)
        keys.remove('X')
        self.build_regular_matrix(keys)


class Pentominoes5x12(Pentominoes):

    """1010 solutions"""

    height = 5
    width = 12

    @classmethod
    def components(cls):
        return (Pentominoes5x12A, Pentominoes5x12B)


class Pentominoes5x12A(Pentominoes5x12):

    def build_matrix(self):
        keys = sorted(self.pieces.keys())
        x_coords, x_aspect = self.pieces['X'][0]
        for x in range(1, 5):
            translated = x_aspect.translate((x, 0))
            self.build_matrix_row('X', translated)
        keys.remove('X')
        self.build_regular_matrix(keys)


class Pentominoes5x12B(Pentominoes5x12):

    """symmetry: X at center; remove flip of P"""

    def customize_piece_data(self):
        self.piece_data['P'][-1]['flips'] = None

    def build_matrix(self):
        keys = sorted(self.pieces.keys())
        x_coords, x_aspect = self.pieces['X'][0]
        for x in range(5):
            translated = x_aspect.translate((x, 1))
            self.build_matrix_row('X', translated)
        keys.remove('X')
        self.build_regular_matrix(keys)


class Pentominoes4x15(Pentominoes):

    """368 solutions"""

    height = 4
    width = 15

    @classmethod
    def components(cls):
        return (Pentominoes4x15A, Pentominoes4x15B)


class Pentominoes4x15A(Pentominoes4x15):

    def build_matrix(self):
        keys = sorted(self.pieces.keys())
        x_coords, x_aspect = self.pieces['X'][0]
        for x in range(1, 6):
            translated = x_aspect.translate((x, 0))
            self.build_matrix_row('X', translated)
        keys.remove('X')
        self.build_regular_matrix(keys)


class Pentominoes4x15B(Pentominoes4x15):

    """symmetry: X at center; remove flip of P"""

    def customize_piece_data(self):
        self.piece_data['P'][-1]['flips'] = None

    def build_matrix(self):
        keys = sorted(self.pieces.keys())
        x_coords, x_aspect = self.pieces['X'][0]
        translated = x_aspect.translate((6, 0))
        self.build_matrix_row('X', translated)
        keys.remove('X')
        self.build_regular_matrix(keys)


class Pentominoes3x20(Pentominoes):

    """
    2 solutions.
    Symmetry: restrict I to y=0.
    """

    height = 3
    width = 20

    def build_matrix(self):
        keys = sorted(self.pieces.keys())
        x_coords, x_aspect = self.pieces['X'][0]
        for x in (1, 6):
            translated = x_aspect.translate((x, 0))
            self.build_matrix_row('X', translated)
        keys.remove('X')
        for key in keys:
            for coords, aspect in self.pieces[key]:
                for y in range(self.height - aspect.bounds[1]
                               - 2 * (key == 'I')):
                    for x in range(self.width - aspect.bounds[0]):
                        translated = aspect.translate((x, y))
                        self.build_matrix_row(key, translated)


class Pentominoes3x20Loop(Pentominoes):

    """
    2 solutions: same as non-loop `Pentominoes3x20`.
    Symmetry: fix X; restrict U to 2 quadrants; restrict I to y=0 & 1.
    """

    height = 3
    width = 20

    def customize_piece_data(self):
        self.piece_data['U'][-1]['rotations'] = (2, 3)

    def build_matrix(self):
        keys = sorted(self.pieces.keys())
        x_coords, x_aspect = self.pieces['X'][0]
        translated = x_aspect.translate((1, 0))
        self.build_matrix_row('X', translated)
        keys.remove('X')
        for key in keys:
            for coords, aspect in self.pieces[key]:
                for y in range(self.height - aspect.bounds[1] - (key == 'I')):
                    for x in range(self.width):
                        translated = aspect.translate((x, y), (self.width, 0))
                        self.build_matrix_row(key, translated)


class Pentominoes3x20Tube(Pentominoes):

    """
    Symmetry: restrict X to dx=1 & 6, dy=0; remove flip of F.
    """

    height = 3
    width = 20

    check_for_duplicates = True

    def customize_piece_data(self):
        self.piece_data['F'][-1]['flips'] = None

    def build_matrix(self):
        keys = sorted(self.pieces.keys())
        x_coords, x_aspect = self.pieces['X'][0]
        for x in (1, 6):
            translated = x_aspect.translate((x, 0))
            self.build_matrix_row('X', translated)
        keys.remove('X')
        for key in keys:
            for coords, aspect in self.pieces[key]:
                for y in range(self.height):
                    for x in range(self.width - aspect.bounds[0]):
                        translated = aspect.translate((x, y), (0, self.height))
                        self.build_matrix_row(key, translated)


class Pentominoes8x8CenterHole(Pentominoes):

    """65 solutions"""

    height = 8
    width = 8

    @classmethod
    def components(cls):
        return (Pentominoes8x8CenterHoleA,
                Pentominoes8x8CenterHoleB)

    def coordinates(self):
        for y in range(self.height):
            for x in range(self.width):
                if 3 <= x <= 4 and 3 <= y <= 4:
                    continue
                yield (x, y)


class Pentominoes8x8CenterHoleA(Pentominoes8x8CenterHole):

    def build_matrix(self):
        keys = sorted(self.pieces.keys())
        x_coords, x_aspect = self.pieces['X'][0]
        for x, y in ((1, 0), (2, 0)):
            translated = x_aspect.translate((x, 0))
            self.build_matrix_row('X', translated)
        keys.remove('X')
        self.build_regular_matrix(keys)


class Pentominoes8x8CenterHoleB(Pentominoes8x8CenterHole):

    """symmetry: X on diagonal; remove flip of P"""

    def customize_piece_data(self):
        self.piece_data['P'][-1]['flips'] = None

    def build_matrix(self):
        keys = sorted(self.pieces.keys())
        x_coords, x_aspect = self.pieces['X'][0]
        translated = x_aspect.translate((1, 1))
        self.build_matrix_row('X', translated)
        keys.remove('X')
        self.build_regular_matrix(keys)


class Pentominoes8x8WithoutCorners(Pentominoes):

    """2170 solutions"""

    height = 8
    width = 8

    def customize_piece_data(self):
        self.piece_data['P'][-1]['flips'] = None
        self.piece_data['P'][-1]['rotations'] = None

    def coordinates(self):
        for y in range(self.height):
            for x in range(self.width):
                if (x == 0 or x == 7) and (y == 0 or y == 7):
                    continue
                yield (x, y)


class PentominoesPlusSquareTetromino8x8(PentominoesPlusSquareTetromino):

    """16146 solutions"""

    height = 8
    width = 8

    def customize_piece_data(self):
        self.piece_data['P'][-1]['flips'] = None
        self.piece_data['P'][-1]['rotations'] = None


class PentominoesPlusSquareTetrominoTriangle(PentominoesPlusSquareTetromino):

    """473 solutions"""

    height = 8
    width = 15

    def coordinates(self):
        for coord in PentominoesPlusSquareTetromino.coordinates(self):
            x, y = coord
            if (y <= x) and (y < (self.width - x)):
                yield coord

    def customize_piece_data(self):
        self.piece_data['P'][-1]['flips'] = None


class PentominoesTriangle(Pentominoes):

    """
    55-square triangle, so 11 pieces are used and one piece must be omitted.
    All but the 'P' & 'W' pieces can be omitted.

    580 solutions
    """

    height = 10
    width = 14

    # These 9 coordinates form a minimal cover for all 12 pentominoes
    omitted_piece_coordinates = (
        (11,4), (11,5), (11,6), (12,2), (12,3), (12,4), (12,5), (12,6), (13,4))

    # Since there are only 9 coordinates for the omitted piece, only 1 piece
    # can fit.  By setting these 9 coordinates as secondary columns, the extra
    # 4 coordinates are ignored.
    secondary_columns = 9

    # These are the fixed positions for omitted pieces, to prevent duplicates.
    omitted_piece_positions = {
        'F': ((11,4), (11,5), (12,3), (12,4), (13,4)),
        'I': ((12,2), (12,3), (12,4), (12,5), (12,6)),
        'L': ((12,2), (12,3), (12,4), (12,5), (11,5)),
        'N': ((12,2), (12,3), (12,4), (11,4), (11,5)),
        'P': ((11,4), (11,5), (11,6), (12,5), (12,6)),
        'T': ((12,2), (12,3), (12,4), (11,4), (13,4)),
        'U': ((11,4), (11,5), (11,6), (12,4), (12,6)),
        'V': ((11,4), (11,5), (11,6), (12,4), (13,4)),
        'W': ((11,5), (11,6), (12,4), (12,5), (13,4)),
        'X': ((11,4), (12,3), (12,4), (12,5), (13,4)),
        'Y': ((12,2), (12,3), (12,4), (12,5), (11,4)),
        'Z': ((12,4), (12,5), (12,6), (11,6), (13,4)),}

    svg_rotation = -45

    def coordinates(self):
        for y in range(self.height):
            for x in range(self.height):
                if x + y >= (self.height - 1) and x < self.height:
                    yield (x, y)
        for coord in self.omitted_piece_coordinates:
            yield coord

    def customize_piece_data(self):
        self.piece_data['P'][-1]['flips'] = None

    def build_matrix(self):
        self.build_rows_for_omitted_pieces()
        self.build_regular_matrix(sorted(self.piece_data.keys()))

    def build_rows_for_omitted_pieces(self):
        for key, coords in self.omitted_piece_positions.items():
            self.build_matrix_row(key, coords)

    def build_regular_matrix(self, keys):
        for key in keys:
            for coords, aspect in self.pieces[key]:
                for y in range(self.height - aspect.bounds[1]):
                    # can't use self.width; omitted pieces are handled above:
                    for x in range(self.height - aspect.bounds[0]):
                        translated = aspect.translate((x, y))
                        if translated.issubset(self.solution_coords):
                            self.build_matrix_row(key, translated)


class PentominoesDiamond(Pentominoes):

    """
    8 solutions

    (Puzzle with central hole has no solutions.)
    """

    height = 10
    width = 11

    def coordinates(self):
        for coord in Pentominoes.coordinates(self):
            x, y = coord
            xy = x + y
            x_y = x - y
            if (5 <= xy <= 15) and (-5 <= x_y <= 5):
                yield coord

    def customize_piece_data(self):
        self.piece_data['P'][-1]['flips'] = None


class PentominoesPlusMonominoDiamond(PentominoesPlusMonomino):

    """10 solutions"""

    height = 11
    width = 11

    def coordinates(self):
        for coord in Pentominoes.coordinates(self):
            x, y = coord
            xy = x + y
            x_y = x - y
            if (5 <= xy <= 15) and (-5 <= x_y <= 5):
                yield coord

    def customize_piece_data(self):
        self.piece_data['P'][-1]['flips'] = None
        self.piece_data['P'][-1]['rotations'] = None


class PentominoesTrapezoid(Pentominoes):

    """
    140 solutions
    """

    height = 11
    width = 11

    svg_rotation = -45

    def coordinates(self):
        for coord in Pentominoes.coordinates(self):
            x, y = coord
            xy = x + y
            if xy >= (self.height - 1) and xy < (self.height * 2 - 4):
                yield coord

    def customize_piece_data(self):
        self.piece_data['P'][-1]['flips'] = None


class PentominoesTrapezoid2(Pentominoes):

    """
    0 solutions
    """

    height = 14
    width = 14

    def coordinates(self):
        for coord in Pentominoes.coordinates(self):
            x, y = coord
            xy = x + y
            if xy >= (self.height - 1) and xy < (self.height * 2 - 10):
                yield coord


class PentominoesChevron1(Pentominoes):

    """
    101 solutions
    """

    height = 11
    width = 11

    svg_rotation = -45

    def coordinates(self):
        for coord in Pentominoes.coordinates(self):
            x, y = coord
            xy = x + y
            if xy >= (self.height - 1) and ((x > 6) or (y > 6)):
                yield coord

    def customize_piece_data(self):
        self.piece_data['P'][-1]['flips'] = None


class PentominoesChevron2(Pentominoes):

    """
    82 solutions
    """

    height = 11
    width = 11

    svg_rotation = -45

    def coordinates(self):
        for coord in Pentominoes.coordinates(self):
            x, y = coord
            if ((x > 6) or (y > 6)) and (-7 <= y - x <= 7):
                yield coord

    def customize_piece_data(self):
        self.piece_data['P'][-1]['flips'] = None


class PentominoesChevron_X(Pentominoes):

    """
    0 solutions ("I" piece doesn't fit anywhere)
    """

    height = 11
    width = 15

    def coordinates(self):
        center = (self.width + 1) / 2
        for coord in Pentominoes.coordinates(self):
            x, y = coord
            if (  ((x < center) and (x <= y < x + 4))
                  or ((x >= center)
                      and ((self.width - x) <= y < (self.width - x + 4)))):
                yield coord


class PentominoesCross1(Pentominoes):

    """14 solutions"""

    height = 11
    width = 11

    def coordinates(self):
        coords = set(self.coordinates_rectangle(11, 3, offset=(0,4)))
        coords.update(self.coordinates_rectangle(3, 11, offset=(4,0)))
        coords.update(self.coordinates_rectangle(5, 5, offset=(3,3)))
        coords.remove((5,5))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P'][-1]['flips'] = None
        self.piece_data['P'][-1]['rotations'] = None


class PentominoesPlusMonominoCross1(PentominoesPlusMonomino):

    """
    366 solutions

    Suggested by Dan Klarskov.
    """

    height = 11
    width = 11

    def coordinates(self):
        coords = set(self.coordinates_rectangle(11, 3, offset=(0,4)))
        coords.update(self.coordinates_rectangle(3, 11, offset=(4,0)))
        coords.update(self.coordinates_rectangle(5, 5, offset=(3,3)))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P'][-1]['flips'] = None
        self.piece_data['P'][-1]['rotations'] = None


class PentominoesPlusSquareTetrominoCross1(PentominoesPlusSquareTetromino):

    """
    5380 solutions

    Designed by Dan Klarskov.
    """

    height = 8
    width = 10

    def coordinates(self):
        coords = set(self.coordinates_rectangle(10, 4, offset=(0,2)))
        coords.update(self.coordinates_rectangle(6, 8, offset=(2,0)))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P'][-1]['flips'] = None
        self.piece_data['P'][-1]['rotations'] = (0, 1)


class PentominoesCross2(Pentominoes):

    """
    84 solutions

    Designed by Dan Klarskov.
    """

    height = 8
    width = 10

    def coordinates(self):
        coords = set(self.coordinates_rectangle(10, 4, offset=(0,2)))
        coords.update(self.coordinates_rectangle(6, 8, offset=(2,0)))
        coords.difference_update(self.coordinates_rectangle(2, 2, offset=(4,3)))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P'][-1]['flips'] = None
        self.piece_data['P'][-1]['rotations'] = (0, 1)


class PentominoesPlusSquareTetrominoCross2(PentominoesPlusSquareTetromino):

    """
    2071 solutions

    Designed by Dan Klarskov.
    """

    height = 9
    width = 9

    def coordinates(self):
        coords = set(self.coordinates_rectangle(9, 5, offset=(0,2)))
        coords.update(self.coordinates_rectangle(5, 9, offset=(2,0)))
        coords.remove((4,4))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P'][-1]['flips'] = None
        self.piece_data['P'][-1]['rotations'] = None


class PentominoesCross3(Pentominoes):

    """
    28 solutions

    Designed by Dan Klarskov.
    """

    height = 9
    width = 9

    hole = set(((3,4), (4,3), (4,4), (4,5), (5,4)))

    def coordinates(self):
        coords = set(self.coordinates_rectangle(9, 5, offset=(0,2)))
        coords.update(self.coordinates_rectangle(5, 9, offset=(2,0)))
        coords.difference_update(self.hole)
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P'][-1]['flips'] = None
        self.piece_data['P'][-1]['rotations'] = None


class PentominoesPlusSquareTetrominoCross3(PentominoesPlusSquareTetromino):

    """
    177 solutions

    Designed by Dan Klarskov.
    """

    height = 10
    width = 10

    def coordinates(self):
        coords = set(self.coordinates_rectangle(10, 4, offset=(0,3)))
        coords.update(self.coordinates_rectangle(4, 10, offset=(3,0)))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P'][-1]['flips'] = None
        self.piece_data['P'][-1]['rotations'] = None


class PentominoesCross4(Pentominoes):

    """21 solutions"""

    height = 14
    width = 9

    def coordinates(self):
        coords = set(self.coordinates_rectangle(9, 3, offset=(0,8)))
        coords.update(self.coordinates_rectangle(3, 14, offset=(3,0)))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P'][-1]['flips'] = None


class PentominoesCross_X1(Pentominoes):

    """0 solutions"""

    height = 10
    width = 10

    def coordinates(self):
        coords = set(self.coordinates_rectangle(10, 4, offset=(0,3)))
        coords.update(self.coordinates_rectangle(4, 10, offset=(3,0)))
        coords.difference_update(self.coordinates_rectangle(2, 2, offset=(4,4)))
        return sorted(coords)


class PentominoesCross_X2(Pentominoes):

    """0 solutions"""

    height = 12
    width = 12

    def coordinates(self):
        coords = set(self.coordinates_rectangle(12, 2, offset=(0,5)))
        coords.update(self.coordinates_rectangle(2, 12, offset=(5,0)))
        coords.update(self.coordinates_rectangle(4, 8, offset=(4,2)))
        coords.update(self.coordinates_rectangle(8, 4, offset=(2,4)))
        coords.difference_update(self.coordinates_rectangle(2, 2, offset=(5,5)))
        return sorted(coords)


class PentominoesCross_X3(Pentominoes):

    """0 solutions"""

    height = 10
    width = 10

    holes = set(((3,3), (3,6), (6,3), (6,6)))

    def coordinates(self):
        coords = set(self.coordinates_rectangle(10, 4, offset=(0,3)))
        coords.update(self.coordinates_rectangle(4, 10, offset=(3,0)))
        coords.difference_update(self.holes)
        return sorted(coords)


class PentominoesCross_X4(Pentominoes):

    """0 solutions"""

    height = 9
    width = 9

    hole = set(((3,3), (3,5), (4,4), (5,3), (5,5)))

    def coordinates(self):
        coords = set(self.coordinates_rectangle(9, 5, offset=(0,2)))
        coords.update(self.coordinates_rectangle(5, 9, offset=(2,0)))
        coords.difference_update(self.hole)
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P'][-1]['flips'] = None
        self.piece_data['P'][-1]['rotations'] = None


class PentominoesPlusSquareTetrominoCross4(PentominoesPlusSquareTetromino):

    """
    2 solutions

    Designed by Dan Klarskov.
    """

    height = 12
    width = 12

    def coordinates(self):
        coords = set(self.coordinates_rectangle(12, 2, offset=(0,5)))
        coords.update(self.coordinates_rectangle(2, 12, offset=(5,0)))
        coords.update(self.coordinates_rectangle(4, 8, offset=(4,2)))
        coords.update(self.coordinates_rectangle(8, 4, offset=(2,4)))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P'][-1]['flips'] = None
        self.piece_data['P'][-1]['rotations'] = None


class PentominoesFlower1(Pentominoes):

    """
    47 solutions

    Designed by Dan Klarskov.
    """

    height = 9
    width = 9

    def coordinates(self):
        coords = set(self.coordinates_rectangle(7, 7, offset=(1,1)))
        coords.update(self.coordinates_rectangle(3, 9, offset=(3,0)))
        coords.update(self.coordinates_rectangle(9, 3, offset=(0,3)))
        coords.remove((4,4))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P'][-1]['flips'] = None
        self.piece_data['P'][-1]['rotations'] = None


class PentominoesFlower2(Pentominoes):

    """
    414 solutions

    Designed by Dan Klarskov.
    """

    height = 7
    width = 11

    def coordinates(self):
        coords = set(self.coordinates_rectangle(9, 5, offset=(1,1)))
        coords.update(self.coordinates_rectangle(5, 7, offset=(3,0)))
        coords.update(self.coordinates_rectangle(11, 3, offset=(0,2)))
        coords.remove((5,3))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P'][-1]['flips'] = None
        self.piece_data['P'][-1]['rotations'] = (0, 1)


class PentominoesFlower3(Pentominoes):

    """
    15 solutions

    Designed by Dan Klarskov.
    """

    height = 8
    width = 10

    def coordinates(self):
        coords = set(self.coordinates_rectangle(8, 6, offset=(1,1)))
        coords.update(self.coordinates_rectangle(4, 8, offset=(3,0)))
        coords.update(self.coordinates_rectangle(10, 4, offset=(0,2)))
        coords.difference_update(self.coordinates_rectangle(2, 2, offset=(4,3)))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P'][-1]['flips'] = None
        self.piece_data['P'][-1]['rotations'] = (0, 1)


class PentominoesFlower4(Pentominoes):

    """
    57 solutions

    Designed by Dan Klarskov.
    """

    height = 9
    width = 10

    def coordinates(self):
        coords = set(self.coordinates_rectangle(10, 3, offset=(0,3)))
        coords.update(self.coordinates_rectangle(8, 5, offset=(1,2)))
        coords.update(self.coordinates_rectangle(6, 7, offset=(2,1)))
        coords.update(self.coordinates_rectangle(4, 9, offset=(3,0)))
        coords.difference_update(self.coordinates_rectangle(2, 3, offset=(4,3)))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P'][-1]['flips'] = None
        self.piece_data['P'][-1]['rotations'] = (0, 1)


class PentominoesFlower5(Pentominoes):

    """1595 solutions"""

    height = 8
    width = 9

    def coordinates(self):
        coords = set(self.coordinates_rectangle(9, 4, offset=(0,2)))
        coords.update(self.coordinates_rectangle(7, 6, offset=(1,1)))
        coords.update(self.coordinates_rectangle(5, 8, offset=(2,0)))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P'][-1]['flips'] = None
        self.piece_data['P'][-1]['rotations'] = (0, 1)


class PentominoesTruncatedTriangle(Pentominoes):

    """3626 solutions"""

    height = 9
    width = 9

    svg_rotation = -45

    def coordinates(self):
        for coord in Pentominoes.coordinates(self):
            x, y = coord
            xy = x + y
            if xy >= 6:
                yield coord

    def customize_piece_data(self):
        self.piece_data['P'][-1]['flips'] = None


class PentominoesArch1(Pentominoes):

    """602 solutions"""

    height = 7
    width = 11

    holes = set((
        (0,3), (0,4), (0,5), (0,6), (1,5), (1,6), (2,6), (3,6), (5,0),
        (10,3), (10,4), (10,5), (10,6), (9,5), (9,6), (8,6), (7,6)))

    def coordinates(self):
        coords = set(self.coordinates_rectangle(self.width, self.height))
        coords.difference_update(self.holes)
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P'][-1]['flips'] = None


class PentominoesArch2(PentominoesArch1):

    """125 solutions"""

    height = 7
    width = 12

    holes = set((
        (0,3), (0,4), (0,5), (0,6), (1,5), (1,6), (2,6), (3,6),
        (4,0), (5,0), (6,0), (7,0), (4,1), (5,1), (6,1), (7,1),
        (11,3), (11,4), (11,5), (11,6), (10,5), (10,6), (9,6), (8,6)))


class OneSidedPentominoes3x30(OneSidedPentominoes):

    height = 3
    width = 30

    check_for_duplicates = True

    duplicate_conditions = ({'x_reversed': True},
                            {'y_reversed': True},
                            {'x_reversed': True, 'y_reversed': True})


class OneSidedPentominoes5x18(OneSidedPentominoes3x30):

    height = 5
    width = 18


class OneSidedPentominoes6x15(OneSidedPentominoes3x30):

    height = 6
    width = 15


class OneSidedPentominoes9x10(OneSidedPentominoes3x30):

    height = 9
    width = 10
