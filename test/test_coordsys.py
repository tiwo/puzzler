#!/usr/bin/env python
# $Id$

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2006 by David J. Goodger
# License: GPL 2 (see alltests.py)

import unittest
from puzzler import coordsys


class Cartesian1DTests(unittest.TestCase):

    def test_flip0(self):
        c = coordsys.Cartesian1D((0,))
        self.assertEquals(c.flip0(), c)
        c = coordsys.Cartesian1D((1,))
        self.assertEquals(c.flip0(), (-1,))
        c = coordsys.Cartesian1D((5,))
        self.assertEquals(c.flip0(), (-5,))

    def test_flip(self):
        p = coordsys.Cartesian1D((1,))
        c0 = coordsys.Cartesian1D((0,))
        c2 = coordsys.Cartesian1D((2,))
        c5 = coordsys.Cartesian1D((5,))
        self.assertEquals(c0.flip(p), c2)
        self.assertEquals(c2.flip(p), c0)
        self.assertEquals(p.flip(p), p)
        self.assertEquals(c5.flip(p), (-3,))


class Cartesian2DTests(unittest.TestCase):

    o = coordsys.Cartesian2D((0,0))
    c = coordsys.Cartesian2D((2,5))
    p = coordsys.Cartesian2D((1,1))
    rotated = {'c/0': [(2, 5), (-5, 2), (-2, -5), (5, -2)],
               'o/p': [(0, 0), (2, 0), (2, 2), (0, 2)],
               'c/p': [(2, 5), (-3, 2), (0, -3), (5, 0)]}

    def test_rotate0(self):
        for r in range(4):
            self.assertEquals(self.o.rotate0(r), self.o)
        for r in range(4):
            self.assertEquals(self.c.rotate0(r), self.rotated['c/0'][r])

    def test_rotate(self):
        for r in range(4):
            self.assertEquals(self.o.rotate(r, self.o), self.o)
        for r in range(4):
            self.assertEquals(self.o.rotate(r, self.p), self.rotated['o/p'][r])
        for r in range(4):
            self.assertEquals(self.c.rotate(r, self.p), self.rotated['c/p'][r])

    def test_arithmetic(self):
        self.assertEquals(self.o + self.c, self.c)
        self.assertEquals(self.c + self.p, (3,6))
        self.assertEquals(self.c - self.p, (1,4))
        self.assertEquals(self.p - self.c, (-1, -4))


class Hexagonal2DTests(unittest.TestCase):

    o = coordsys.Hexagonal2D((0,0))
    c10 = coordsys.Hexagonal2D((1,0))
    c01 = coordsys.Hexagonal2D((0,1))
    c11 = coordsys.Hexagonal2D((1,1))
    c23 = coordsys.Hexagonal2D((2,3))
    rotated = {'c10/0': [(1,0), (0,1), (-1,1), (-1,0), (0,-1), (1,-1)],
               'c23/c11': [(2, 3), (-1, 4), (-2, 2), (0, -1), (3, -2), (4, 0)]}

    def test_flip0(self):
        self.assertEquals(self.o.flip0(), self.o)
        self.assertEquals(self.c01.flip0(), self.c01)
        self.assertEquals(self.c10.flip0(), (-1,1))
        self.assertEquals(self.c11.flip0(), (-1,2))
        c = coordsys.Hexagonal2D((2,-1))
        self.assertEquals(c.flip0(), (-2,1))

    def test_flip(self):
        self.assertEquals(self.o.flip(self.o), self.o)
        self.assertEquals(self.c01.flip(self.o), self.c01)
        self.assertEquals(self.c10.flip(self.o), (-1,1))
        self.assertEquals(self.c11.flip(self.o), (-1,2))

        self.assertEquals(self.o.flip(self.c11), (2,-1))
        self.assertEquals(self.c01.flip(self.c11), (2,0))
        self.assertEquals(self.c10.flip(self.c11), self.c10)
        self.assertEquals(self.c11.flip(self.c11), self.c11)

    def test_rotate0(self):
        for r in range(6):
            self.assertEquals(self.o.rotate0(r), self.o)
        for r in range(6):
            self.assertEquals(self.c10.rotate0(r), self.rotated['c10/0'][r])

    def test_rotate(self):
        for r in range(6):
            self.assertEquals(self.c10.rotate(r, self.o),
                              self.rotated['c10/0'][r])
        for r in range(6):
            self.assertEquals(self.c23.rotate(r, self.c11),
                              self.rotated['c23/c11'][r])


class Triangular3DTests(unittest.TestCase):

    o = coordsys.Triangular3D((0,0,0))
    o_rotated = ((0,0,0), (-1,0,1), (-1,0,0), (-1,-1,1), (0,-1,0), (0,-1,1))
    c100 = coordsys.Triangular3D((1,0,0))
    rotated = {'c100/0': ((1,0,0), (-1,1,1), (-2,1,0),
                          (-2,-1,1), (0,-2,0), (1,-2,1)),}

    def test_flip0(self):
        self.assertEquals(self.o.flip0(), self.o)
        self.assertEquals(self.c100.flip0(), (-1,0,0))

    def test_rotate0(self):
        o = self.o
        for r in range(6):
            self.assertEquals(self.o.rotate0(r), self.o_rotated[r])
            o = o.rotate0(1)
            self.assertEquals(o, self.o_rotated[(r + 1) % 6])
        c = self.c100
        for r in range(6):
            self.assertEquals(self.c100.rotate0(r), self.rotated['c100/0'][r])
            c = c.rotate0(1)
            self.assertEquals(c, self.rotated['c100/0'][(r + 1) % 6])


class SquareGrid3DTests(unittest.TestCase):

    o = coordsys.SquareGrid3D((0,0,0))
    o_rotated = ((0,0,0), (0,0,1), (-1,0,0), (0,-1,1))
    c100 = coordsys.SquareGrid3D((1,0,0))
    c111 = coordsys.SquareGrid3D((1,1,1))
    rotated = {'c100/0': ((1,0,0), (0,1,1), (-2,0,0), (0,-2,1)),
               'c111/0': ((1,1,1), (-2,1,0), (-1,-2,1), (1,-1,0)),}

    def test_flip0(self):
        self.assertEquals(self.o.flip0(), (-1,0,0))
        self.assertEquals(self.c100.flip0(), (-2,0,0))

    def test_rotate0(self):
        o = self.o
        for r in range(4):
            self.assertEquals(self.o.rotate0(r), self.o_rotated[r])
            o = o.rotate0(1)
            self.assertEquals(o, self.o_rotated[(r + 1) % 4])
        c = self.c100
        for r in range(4):
            self.assertEquals(self.c100.rotate0(r), self.rotated['c100/0'][r])
            c = c.rotate0(1)
            self.assertEquals(c, self.rotated['c100/0'][(r + 1) % 4])
        c = self.c111
        for r in range(4):
            self.assertEquals(self.c111.rotate0(r), self.rotated['c111/0'][r])
            c = c.rotate0(1)
            self.assertEquals(c, self.rotated['c111/0'][(r + 1) % 4])


class TriangularGrid3DTests(unittest.TestCase):

    o = coordsys.TriangularGrid3D((0,0,0))
    o_rotated = ((0,0,0), (0,0,1), (0,0,2), (-1,0,0), (0,-1,1), (1,-1,2))
    c100 = coordsys.TriangularGrid3D((1,0,0))
    c111 = coordsys.TriangularGrid3D((1,1,1))
    rotated = {
        'c100/0': ((1,0,0), (0,1,1), (-1,1,2), (-2,0,0), (0,-2,1), (2,-2,2)),
        'c111/0': ((1,1,1), (-1,2,2), (-3,1,0), (-1,-2,1), (2,-3,2), (2,-1,0)),}
    p = ((1,0,1), (1,1,1), (1,2,0))
    p_rotated = (
        ((0,0,1), (0,1,1), (0,2,0)),
        ((2,0,2), (1,1,2), (0,2,1)),
        ((2,0,0), (1,0,0), (1,0,2)),
        ((1,1,1), (1,0,1), (0,0,0)),
        ((1,2,2), (2,1,2), (2,0,1)),
        ((0,1,0), (1,1,0), (3,0,2)),)

    def test_flip0(self):
        self.assertEquals(self.o.flip0(), (0,0,2))
        self.assertEquals(self.c100.flip0(), (-1,1,2))
        self.assertEquals(self.c111.flip0(), (-1,2,1))

    def test_rotate0(self):
        o = self.o
        for r in range(6):
            self.assertEquals(self.o.rotate0(r), self.o_rotated[r])
            o = o.rotate0(1)
            self.assertEquals(o, self.o_rotated[(r + 1) % 6])
        c = self.c100
        for r in range(6):
            self.assertEquals(self.c100.rotate0(r), self.rotated['c100/0'][r])
            c = c.rotate0(1)
            self.assertEquals(c, self.rotated['c100/0'][(r + 1) % 6])
        c = self.c111
        for r in range(6):
            self.assertEquals(self.c111.rotate0(r), self.rotated['c111/0'][r])
            c = c.rotate0(1)
            self.assertEquals(c, self.rotated['c111/0'][(r + 1) % 6])

    def test_view(self):
        v = coordsys.TriangularGrid3DView(self.p)
        for r in range(7):
            v = v.rotate0(1)
            self.assertEquals(v, set(self.p_rotated[(r + 1) % 6]))

    def test_intersection_coordinates(self):
        self.assertEquals(
            self.c100.intersection_coordinates(),
            [(1, 0, 0), (1, 0, 1), (1, 0, 2), (1, 0, 3), (1, 0, 4), (1, 0, 5),
             (2, 0, 0), (2, 0, 1), (2, 0, 2), (2, 0, 3), (2, 0, 4), (2, 0, 5)])


if __name__ == '__main__':
    unittest.main()
