#!/usr/bin/env python
# $Id$

"""
Concrete pentahex puzzles.
"""

from puzzler.puzzles.polyhexes import Pentahexes


class Pentahex10x11(Pentahexes):

    """? (many) solutions"""

    height = 10
    width = 11

    duplicate_conditions = ({'rotate_180': True},)


class Pentahex5x22(Pentahexes):

    """? (many) solutions"""

    height = 5
    width = 22

    duplicate_conditions = ({'rotate_180': True},)


class Pentahex15x11Trapezium(Pentahexes):

    height = 11
    width = 15

    def coordinates(self):
        for y in range(self.height):
            for x in range(self.width):
                if x + y < self.width:
                    yield (x, y)


class Pentahex5x24Trapezium(Pentahex15x11Trapezium):

    height = 5
    width = 24


class PentahexHexagon1(Pentahexes):

    """ solutions"""

    height = 13
    width = 13

    duplicate_conditions = ({'rotate_180': True},)

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


class PentahexHexagon2(Pentahexes):

    """ solutions"""

    height = 13
    width = 13

    duplicate_conditions = ({'rotate_180': True},)

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


class PentahexHexagon3(Pentahexes):

    """ solutions"""

    height = 15
    width = 15

    duplicate_conditions = ({'rotate_180': True},)

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


class PentahexHexagon4(Pentahexes):

    """ solutions"""

    height = 15
    width = 15

    duplicate_conditions = ({'rotate_180': True},)

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


class PentahexTriangle1(Pentahexes):

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


class PentahexTriangle2(Pentahexes):

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


class PentahexTriangle3(Pentahexes):

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


class PentahexTriangle4(Pentahexes):

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


class PentahexTriangle5(Pentahexes):

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


class PentahexTriangle6(Pentahexes):

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


class PentahexHexagram1(Pentahexes):

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


class PentahexHexagram2(PentahexHexagram1):

    def hole_coordinates(self):
        return set(((8,6), (10,6),
                    (8,7), (9,7),
                    (7,8), (8,8), (9,8),
                    (7,9), (8,9),
                    (6,10), (8,10)))


class PentahexHexagram3(PentahexHexagram1):

    def hole_coordinates(self):
        return set(((9,6),
                    (8,7), (9,7),
                    (6,8), (7,8), (8,8), (9,8), (10,8),
                    (7,9), (8,9),
                    (7,10)))


class PentahexHexagram4(PentahexHexagram1):

    def hole_coordinates(self):
        return set(((8,6), (9,6), (10,6),
                    (8,7), (9,7),
                    (8,8),
                    (7,9), (8,9),
                    (6,10), (7,10), (8,10)))


class PentahexHexagram5(PentahexHexagram1):

    def hole_coordinates(self):
        return set(((9,6),
                    (7,7), (8,7), (9,7), (10,7),
                    (8,8),
                    (6,9), (7,9), (8,9), (9,9),
                    (7,10)))


class PentahexHexagram6(PentahexHexagram1):

    def hole_coordinates(self):
        return set(((8,7), (9,7),
                    (5,8), (6,8), (7,8), (8,8), (9,8), (10,8), (11,8),
                    (7,9), (8,9)))


class PentahexHexagram7(PentahexHexagram1):

    def hole_coordinates(self):
        return set(((9,5), (10,5),
                    (9,6),
                    (8,7), (9,7),
                    (8,8),
                    (7,9), (8,9),
                    (7,10),
                    (6,11), (7,11)))
