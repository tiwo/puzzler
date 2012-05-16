#!/usr/bin/env python
# $Id$

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2012 by David J. Goodger
# License: GPL 2 (see __init__.py)

"""
Concrete pentahex puzzles.
"""

from puzzler.puzzles.polyhexes import Pentahexes, OneSidedPentahexes


class Pentahexes10x11(Pentahexes):

    """? (many) solutions"""

    height = 10
    width = 11

    def customize_piece_data(self):
        self.piece_data['P5'][-1]['rotations'] = (0, 1, 2)


class Pentahexes5x22(Pentahexes):

    """? (many) solutions"""

    height = 5
    width = 22

    def customize_piece_data(self):
        self.piece_data['P5'][-1]['rotations'] = (0, 1, 2)


class Pentahexes15x11Trapezoid(Pentahexes):

    height = 11
    width = 15

    def coordinates(self):
        for y in range(self.height):
            for x in range(self.width):
                if x + y < self.width:
                    yield (x, y)

    def customize_piece_data(self):
        self.piece_data['P5'][-1]['flips'] = None


class Pentahexes5x24Trapezoid(Pentahexes15x11Trapezoid):

    height = 5
    width = 24


class PentahexesHexagon1(Pentahexes):

    """ solutions"""

    height = 13
    width = 13

    def coordinates(self):
        hole = set()
        for y in range(4, 9):
            for x in range(4, 9):
                if 9 < x + y < 15:
                    hole.add((x,y))
        hole.remove((8,6))
        hole.remove((4,6))
        for y in range(self.height):
            for x in range(self.width):
                if 5 < x + y < 19 and (x,y) not in hole:
                    yield (x, y)

    def customize_piece_data(self):
        self.piece_data['P5'][-1]['rotations'] = (0, 1, 2)
        self.piece_data['P5'][-1]['flips'] = None


class PentahexesHexagon2(Pentahexes):

    """ solutions"""

    height = 13
    width = 13

    def coordinates(self):
        hole = set()
        for y in range(4, 9):
            for x in range(4, 9):
                if 9 < x + y < 15:
                    hole.add((x,y))
        hole.remove((7,4))
        hole.remove((5,8))
        for y in range(self.height):
            for x in range(self.width):
                if 5 < x + y < 19 and (x,y) not in hole:
                    yield (x, y)

    def customize_piece_data(self):
        self.piece_data['P5'][-1]['rotations'] = (0, 1, 2)
        self.piece_data['P5'][-1]['flips'] = None


class PentahexesHexagon3(Pentahexes):

    """ solutions"""

    height = 15
    width = 15

    def coordinates(self):
        hole = set()
        for y in range(3, 12):
            for x in range(3, 12):
                if 9 < x + y < 19:
                    hole.add((x,y))
        hole.remove((11,7))
        hole.remove((3,7))
        for y in range(self.height):
            for x in range(self.width):
                if 6 < x + y < 22 and (x,y) not in hole:
                    yield (x, y)

    def customize_piece_data(self):
        self.piece_data['P5'][-1]['rotations'] = (0, 1, 2)
        self.piece_data['P5'][-1]['flips'] = None


class PentahexesHexagon4(Pentahexes):

    """ solutions"""

    height = 15
    width = 15

    def coordinates(self):
        hole = set()
        for y in range(3, 12):
            for x in range(3, 12):
                if 9 < x + y < 19:
                    hole.add((x,y))
        hole.remove((5,11))
        hole.remove((9,3))
        for y in range(self.height):
            for x in range(self.width):
                if 6 < x + y < 22 and (x,y) not in hole:
                    yield (x, y)

    def customize_piece_data(self):
        self.piece_data['P5'][-1]['rotations'] = (0, 1, 2)
        self.piece_data['P5'][-1]['flips'] = None


class PentahexesTriangle1(Pentahexes):

    height = 15
    width = 15

    def coordinates(self):
        hole = set()
        for y in range(3, 7):
            for x in range(4, 8):
                if x + y < 11:
                    hole.add((x,y))
        for y in range(self.height):
            for x in range(self.width):
                if x + y < self.width and (x,y) not in hole:
                    yield (x, y)

    def customize_piece_data(self):
        self.piece_data['P5'][-1]['flips'] = None


class PentahexesTriangle2(Pentahexes):

    height = 15
    width = 15

    def coordinates(self):
        hole = set()
        for y in range(5, 9):
            for x in range(3, 7):
                if x + y < 12:
                    hole.add((x,y))
        for y in range(self.height):
            for x in range(self.width):
                if x + y < self.width and (x,y) not in hole:
                    yield (x, y)

    def customize_piece_data(self):
        self.piece_data['P5'][-1]['flips'] = None


class PentahexesTriangle3(Pentahexes):

    height = 15
    width = 15

    def coordinates(self):
        hole = set()
        for y in range(7, 11):
            for x in range(2, 6):
                if x + y < 13:
                    hole.add((x,y))
        for y in range(self.height):
            for x in range(self.width):
                if x + y < self.width and (x,y) not in hole:
                    yield (x, y)

    def customize_piece_data(self):
        self.piece_data['P5'][-1]['flips'] = None


class PentahexesTriangle4(Pentahexes):

    height = 15
    width = 15

    def coordinates(self):
        hole = set()
        for y in range(9, 13):
            for x in range(1, 5):
                if x + y < 14:
                    hole.add((x,y))
        for y in range(self.height):
            for x in range(self.width):
                if x + y < self.width and (x,y) not in hole:
                    yield (x, y)

    def customize_piece_data(self):
        self.piece_data['P5'][-1]['flips'] = None


class PentahexesTriangle5(Pentahexes):

    height = 15
    width = 15

    def coordinates(self):
        hole = set()
        for y in range(1, 5):
            for x in range(5, 9):
                if x + y < 10:
                    hole.add((x,y))
        for y in range(self.height):
            for x in range(self.width):
                if x + y < self.width and (x,y) not in hole:
                    yield (x, y)

    def customize_piece_data(self):
        self.piece_data['P5'][-1]['flips'] = None


class PentahexesTriangle6(Pentahexes):

    height = 15
    width = 15

    def coordinates(self):
        hole = set()
        for y in range(4, 7):
            for x in range(3, 7):
                if 7 < x + y < 12:
                    hole.add((x,y))
        for y in range(self.height):
            for x in range(self.width):
                if x + y < self.width and (x,y) not in hole:
                    yield (x, y)

    def customize_piece_data(self):
        self.piece_data['P5'][-1]['flips'] = None


class PentahexesTwoTriangles(Pentahexes):

    """many solutions"""

    height = 10
    width = 12

    def coordinates(self):
        self.triangle1 = set(self.coordinates_triangle(10))
        self.triangle2 = set(
            self.coordinates_inverted_triangle(10, offset=(2,0)))
        coords = self.triangle1.union(self.triangle2)
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P5'][-1]['rotations'] = (0, 1,)
        self.piece_data['P5'][-1]['flips'] = None

    def build_matrix(self):
        names = sorted(self.piece_data.keys())
        self.build_regular_matrix(['P5'], self.triangle1)
        names.remove('P5')
        self.build_regular_matrix(names)


class PentahexesHexagram1(Pentahexes):

    height = 17
    width = 17

    def coordinates(self):
        hole = self.hole_coordinates()
        coords = set()
        for y in range(4, 17):
            for x in range(4, 17):
                if x + y < 21 and (x,y) not in hole:
                    yield (x, y)
                    coords.add((x,y))
        for y in range(13):
            for x in range(13):
                if x + y > 11 and (x,y) not in hole and (x,y) not in coords:
                    yield (x, y)

    def hole_coordinates(self):
        return set(((7,7), (8,7), (9,7), (10,7),
                    (7,8), (8,8), (9,8),
                    (6,9), (7,9), (8,9), (9,9)))

    def customize_piece_data(self):
        self.piece_data['P5'][-1]['rotations'] = (0, 1, 2)
        self.piece_data['P5'][-1]['flips'] = None


class PentahexesHexagram2(PentahexesHexagram1):

    def hole_coordinates(self):
        return set(((8,6), (10,6),
                    (8,7), (9,7),
                    (7,8), (8,8), (9,8),
                    (7,9), (8,9),
                    (6,10), (8,10)))


class PentahexesHexagram3(PentahexesHexagram1):

    def hole_coordinates(self):
        return set(((9,6),
                    (8,7), (9,7),
                    (6,8), (7,8), (8,8), (9,8), (10,8),
                    (7,9), (8,9),
                    (7,10)))


class PentahexesHexagram4(PentahexesHexagram1):

    def hole_coordinates(self):
        return set(((8,6), (9,6), (10,6),
                    (8,7), (9,7),
                    (8,8),
                    (7,9), (8,9),
                    (6,10), (7,10), (8,10)))


class PentahexesHexagram5(PentahexesHexagram1):

    def hole_coordinates(self):
        return set(((9,6),
                    (7,7), (8,7), (9,7), (10,7),
                    (8,8),
                    (6,9), (7,9), (8,9), (9,9),
                    (7,10)))


class PentahexesHexagram6(PentahexesHexagram1):

    def hole_coordinates(self):
        return set(((8,7), (9,7),
                    (5,8), (6,8), (7,8), (8,8), (9,8), (10,8), (11,8),
                    (7,9), (8,9)))


class PentahexesHexagram7(PentahexesHexagram1):

    def hole_coordinates(self):
        return set(((9,5), (10,5),
                    (9,6),
                    (8,7), (9,7),
                    (8,8),
                    (7,9), (8,9),
                    (7,10),
                    (6,11), (7,11)))


class OneSidedPentahexesTriangle1(OneSidedPentahexes):

    """many solutions"""

    width = 18
    height = 18

    def coordinates(self):
        return sorted(
            set(self.coordinates_triangle(18))
            - set(self.coordinates_triangle(3, offset=(5,5))))


class OneSidedPentahexesTrapezoid18x15(OneSidedPentahexes):

    """many solutions"""

    width = 18
    height = 15

    def coordinates(self):
        return self.coordinates_trapezoid(self.width, self.height)


class OneSidedPentahexesTrapezoid20x11(OneSidedPentahexesTrapezoid18x15):

    """many solutions"""

    width = 20
    height = 11


class OneSidedPentahexesTrapezoid21x10(OneSidedPentahexesTrapezoid18x15):

    """many solutions"""

    width = 21
    height = 10


class OneSidedPentahexesTrapezoid30x6(OneSidedPentahexesTrapezoid18x15):

    """many solutions"""

    width = 30
    height = 6
