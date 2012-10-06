#!/usr/bin/env python
# $Id$

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2012 by David J. Goodger
# License: GPL 2 (see __init__.py)

"""
Concrete hexomino puzzles.
"""

from puzzler.puzzles.polyominoes import (
    Hexominoes, HexominoesPlus, OneSidedHexominoes)


class HexominoesTriangle(Hexominoes):

    """
    many solutions

    Design from `Andrew Clarke's Poly Pages
    <http://www.recmath.com/PolyPages/PolyPages/index.htm?Polyominoes.html>`_.
    """

    width = 20
    height = 20

    def coordinates(self):
        return self.coordinates_triangle(self.width)

    def customize_piece_data(self):
        self.piece_data['P06'][-1]['flips'] = None


class HexominoesParallelogram15x14(Hexominoes):

    """
    many solutions

    Design from `Polyominoes`, by Solomon W. Golomb.
    """

    width = 28
    height = 14

    def coordinates(self):
        segment_width = self.width - self.height + 1
        for y in range(self.height):
            for x in range(y, y + segment_width):
                yield self.coordinate_offset(x, y, None)

    def customize_piece_data(self):
        self.piece_data['P06'][-1]['rotations'] = (0, 1)


class HexominoesParallelogram21x10(HexominoesParallelogram15x14):

    """
    many solutions

    Design from `Andrew Clarke's Poly Pages (Hexomino Constructions)
    <http://recmath.com/PolyPages/PolyPages/index.htm?hexopatts.htm>`_.
    """

    width = 30
    height = 10


class HexominoesParallelogram35x6(HexominoesParallelogram15x14):

    """
    many solutions
    """

    width = 40
    height = 6


# The 30x7 & 42x5 parallelograms are not possible due to the same parity
# imbalance that prevents simple rectangles.


class HexominoesSquare(Hexominoes):

    """many solutions"""

    width = 15
    height = 15

    def coordinates(self):
        coords = (
            set(self.coordinates_rectangle(self.width, self.height))
            - set(self.coordinates_rectangle(5, 3, offset=(5, 6))))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P06'][-1]['flips'] = None
        self.piece_data['P06'][-1]['rotations'] = (0, 1)


class HexominoesRectanglePlusNub1(Hexominoes):

    """
    many solutions

    Design from Tenyo Pla-Puzzle.
    """

    width = 19
    height = 12

    extra = (9, 11)

    def coordinates(self):
        coords = (set(self.coordinates_rectangle(self.width, self.height - 1)))
        x, y = self.extra
        coords.add(self.coordinate_offset(x, y, None))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P06'][-1]['flips'] = None


class HexominoesRectanglePlusNub2(Hexominoes):

    """many solutions"""

    width = 20
    height = 11

    extra = (19, 5)

    def coordinates(self):
        coords = (set(self.coordinates_rectangle(self.width - 1, self.height)))
        x, y = self.extra
        coords.add(self.coordinate_offset(x, y, None))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P06'][-1]['flips'] = None


class HexominoesHoleyRectangle1(Hexominoes):

    """
    many solutions

    Design by W. Stead from `Andrew Clarke's Poly Pages (Hexomino
    Constructions)`_.
    """

    width = 45
    height = 5

    def coordinates(self):
        coords = set(self.coordinates_rectangle(self.width, self.height))
        for x in range(1, self.width, 3):
            coords.remove((x, 2))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P06'][-1]['flips'] = None
        self.piece_data['P06'][-1]['rotations'] = (0, 1)


class HexominoesHoleyRectangle2(Hexominoes):

    """
    many solutions

    Design from `Andrew Clarke's Poly Pages (Hexomino Constructions)`_.
    """

    width = 33
    height = 7

    def coordinates(self):
        coords = (
            set(self.coordinates_rectangle(self.width, self.height))
            - set(self.coordinates_rectangle(7, 3, offset=(13,2))))
        return sorted(coords)

    _find_known_solution = True

    if _find_known_solution:
        # Find a known solution (from Andrew Clarke's Poly Pages).
        # Fix pieces in known positions:
        restrictions = {
            #name: [(aspect, offset), ...],
            'I06': [(1, (16,6))],
            'F36': [(0, (12,3))],
            'X06': [(1, (11,0))],
            'Y16': [(1, (13,0)),
                    (1, (16,0))],
            'F06': [(4, (19,4))],
            'T06': [(1, (19,1))],
            }

        def build_matrix(self):
            self.build_restricted_matrix()

    else:
        # General case
        def customize_piece_data(self):
            self.piece_data['P06'][-1]['flips'] = None
            self.piece_data['P06'][-1]['rotations'] = (0, 1)


class HexominoesHoleyRectangle3(Hexominoes):

    """
    many solutions

    Design from `Polyominoes`, by Solomon W. Golomb.
    """

    width = 17
    height = 15

    def coordinates(self):
        coords = (
            set(self.coordinates_rectangle(self.width, self.height))
            - set(self.coordinates_rectangle(9, 3, offset=(4,6)))
            - set(self.coordinates_rectangle(3, 9, offset=(7,3))))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P06'][-1]['flips'] = None
        self.piece_data['P06'][-1]['rotations'] = (0, 1)


class HexominoesRhombus(Hexominoes):

    """
    many solutions

    Design by David Bird from `Andrew Clarke's Poly Pages (Hexomino
    Constructions)`_.
    """

    width = 29
    height = 15

    def coordinates(self):
        x_middle = self.width / 2
        y_middle = self.height / 2
        coords = set()
        for y in range(y_middle + 1):
            coords.update(
                set(self.coordinates_rectangle(
                4 * y + 1, self.height - 2 * y, offset=(x_middle - 2 * y, y))))
        coords.remove((x_middle, y_middle))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P06'][-1]['flips'] = None
        self.piece_data['P06'][-1]['rotations'] = (0, 1)


class HexominoesCross1(Hexominoes):

    """
    many solutions

    Design from `Andrew Clarke's Poly Pages (Hexomino Constructions)`_.
    """

    width = 43
    height = 5

    def coordinates(self):
        coords = set(
            list(self.coordinates_rectangle(self.width, self.height - 2,
                                            offset=(0,1)))
            + list(self.coordinates_rectangle(self.width - 2, self.height,
                                              offset=(1,0))))
        coords.remove((self.width / 2, self.height / 2))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P06'][-1]['flips'] = None
        self.piece_data['P06'][-1]['rotations'] = (0, 1)


class HexominoesPlusSquare(HexominoesPlus):

    """
    many solutions

    Design from `Kadon's Sextillions
    <http://gamepuzzles.com/polycub2.htm#SX>`_.
    """

    width = 15
    height = 15

    def coordinates(self):
        coords = (
            set(self.coordinates_rectangle(self.width, self.height))
            - set(self.coordinates_rectangle(3, 3, offset=(6,6))))
        return sorted(coords)

    def customize_piece_data(self):
        HexominoesPlus.customize_piece_data(self)
        self.piece_data['P06'][-1]['flips'] = None
        self.piece_data['P06'][-1]['rotations'] = None


class HexominoesPlus18x12(HexominoesPlus):

    """many solutions"""

    width = 18
    height = 12

    def customize_piece_data(self):
        HexominoesPlus.customize_piece_data(self)
        self.piece_data['P06'][-1]['flips'] = None
        self.piece_data['P06'][-1]['rotations'] = (0, 1)


class HexominoesPlus24x9(HexominoesPlus):

    """many solutions"""

    width = 24
    height = 9

    def customize_piece_data(self):
        HexominoesPlus.customize_piece_data(self)
        self.piece_data['P06'][-1]['flips'] = None
        self.piece_data['P06'][-1]['rotations'] = (0, 1)


class HexominoesPlus27x8(HexominoesPlus):

    """many solutions"""

    width = 27
    height = 8

    def customize_piece_data(self):
        HexominoesPlus.customize_piece_data(self)
        self.piece_data['P06'][-1]['flips'] = None
        self.piece_data['P06'][-1]['rotations'] = (0, 1)


class HexominoesPlus36x6(HexominoesPlus):

    """many solutions"""

    width = 36
    height = 6

    def customize_piece_data(self):
        HexominoesPlus.customize_piece_data(self)
        self.piece_data['P06'][-1]['flips'] = None
        self.piece_data['P06'][-1]['rotations'] = (0, 1)


class OneSidedHexominoes20x18(OneSidedHexominoes):

    """many solutions"""

    width = 20
    height = 18


class OneSidedHexominoes24x15(OneSidedHexominoes):

    """many solutions"""

    width = 24
    height = 15


class OneSidedHexominoes30x12(OneSidedHexominoes):

    """many solutions"""

    width = 30
    height = 12


class OneSidedHexominoes36x10(OneSidedHexominoes):

    """many solutions"""

    width = 36
    height = 10


class OneSidedHexominoes40x9(OneSidedHexominoes):

    """many solutions"""

    width = 40
    height = 9


class OneSidedHexominoes45x8(OneSidedHexominoes):

    """many solutions"""

    width = 45
    height = 8


class OneSidedHexominoes60x6(OneSidedHexominoes):

    """many solutions"""

    width = 60
    height = 6


class OneSidedHexominoes72x5(OneSidedHexominoes):

    """many solutions"""

    width = 72
    height = 5


class OneSidedHexominoesDiamond1(OneSidedHexominoes):

    """
    many solutions

    Design from `Andrew Clarke's Poly Pages (Hexomino Constructions)`_.
    """

    width = 27
    height = 27

    def coordinates(self):
        coords = (
            set(self.coordinates_diamond(self.width / 2 + 1))
            - set(self.coordinates_diamond(2, offset=(12,12))))
        return sorted(coords)


class OneSidedHexominoesDiamond2(OneSidedHexominoes):

    """many solutions"""

    width = 25
    height = 25

    holes = ((-1,12), (12,-1), (12,25), (25,12), (12,12))

    def coordinates(self):
        coords = set(self.coordinates_diamond(14, offset=(-1,-1)))
        for coord in self.holes:
            coords.remove(coord)
        return sorted(coords)


class OneSidedHexominoesSquareFort(OneSidedHexominoes):

    """
    many solutions

    Design by David Bird from `Andrew Clarke's Poly Pages (Hexomino
    Constructions)`_.
    """

    width = 20
    height = 20

    offsets = ((0,0), (0,15), (15,0), (15,15))

    def coordinates(self):
        coords = set(self.coordinates_rectangle(18, 18, offset=(1,1)))
        for offset in self.offsets:
            coords.update(set(self.coordinates_rectangle(5, 5, offset=offset)))
        return sorted(coords)


class OneSidedHexominoesHoleyRectangle1(OneSidedHexominoes):

    """
    many solutions

    Design from `Andrew Clarke's Poly Pages (Hexomino Constructions)`_.
    """

    width = 40
    height = 10

    def coordinates(self):
        coords = (
            set(self.coordinates_rectangle(self.width, self.height))
            - set(self.coordinates_rectangle(10, 4, offset=(15,3))))
        return sorted(coords)


class OneSidedHexominoesSixCrosses(OneSidedHexominoes):

    """
    many solutions

    Design from `Andrew Clarke's Poly Pages (Hexomino Constructions)`_.
    """

    width = 53
    height = 8

    def coordinates(self):
        coords = set()
        for i in range(6):
            coords.update(set(
                self.coordinates_rectangle(8, 6, offset=(i * 9, 1))))
            coords.update(set(
                self.coordinates_rectangle(6, 8, offset=(i * 9 + 1, 0))))
        return sorted(coords)
