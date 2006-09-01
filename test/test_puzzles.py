#!/usr/bin/env python
# $Id$

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2006 by David J. Goodger
# License: GPL 2 (see alltests.py)

import sys
import copy
import unittest
from puzzler import puzzles


class MockPuzzle(puzzles.Puzzle2D):

    height = 4
    width = 5
    svg_fills = {'#': 'black'}

    def make_aspects(self, data, **kwargs):
        pass

    def build_matrix_header(self):
        pass

    def build_matrix(self):
        pass

    def build_regular_matrix(self, keys):
        pass


class SVGTests(unittest.TestCase):

    s_matrix_1 = (                        # includes 1-unit margin all around
        [[' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', '#', ' ', '#', ' '],
         [' ', '#', '#', '#', '#', '#', ' '],
         [' ', ' ', '#', '#', '#', ' ', ' '],
         [' ', '#', '#', ' ', '#', '#', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' '],])
    polygon_points_1 = [
        (30, 50), (40, 50), (40, 40), (50, 40), (50, 50), (60, 50), (60, 30),
        (50, 30), (50, 20), (60, 20), (60, 10), (40, 10), (40, 20), (30, 20),
        (30, 10), (10, 10), (10, 20), (20, 20), (20, 30), (10, 30), (10, 40),
        (30, 40)]
    polygon_1 = '''\
<polygon fill="black" stroke="white" stroke-width="1"
         points="30.000,50.000 40.000,50.000 40.000,40.000 50.000,40.000 50.000,50.000 60.000,50.000 60.000,30.000 50.000,30.000 50.000,20.000 60.000,20.000 60.000,10.000 40.000,10.000 40.000,20.000 30.000,20.000 30.000,10.000 10.000,10.000 10.000,20.000 20.000,20.000 20.000,30.000 10.000,30.000 10.000,40.000 30.000,40.000" />
'''
    pentominoes_solution = """\
U U X P P P L L L L F T T T W W Z V V V
U X X X P P L N N F F F T W W Y Z Z Z V
U U X I I I I I N N N F T W Y Y Y Y Z V"""
    pentominoes_svg = '''\
<?xml version="1.0" standalone="no"?>
<!-- Created by Polyform Puzzler (http://puzzler.sourceforge.net/) -->
<svg width="220" height="50" viewBox="0 0 220 50"
     xmlns="http://www.w3.org/2000/svg">
<g>
<polygon fill="turquoise" stroke="white" stroke-width="1"
         points="10.000,40.000 30.000,40.000 30.000,30.000 20.000,30.000 20.000,20.000 30.000,20.000 30.000,10.000 10.000,10.000" />
<polygon fill="red" stroke="white" stroke-width="1"
         points="30.000,40.000 40.000,40.000 40.000,30.000 50.000,30.000 50.000,20.000 40.000,20.000 40.000,10.000 30.000,10.000 30.000,20.000 20.000,20.000 20.000,30.000 30.000,30.000" />
<polygon fill="magenta" stroke="white" stroke-width="1"
         points="40.000,40.000 70.000,40.000 70.000,20.000 50.000,20.000 50.000,30.000 40.000,30.000" />
<polygon fill="lime" stroke="white" stroke-width="1"
         points="70.000,40.000 110.000,40.000 110.000,30.000 80.000,30.000 80.000,20.000 70.000,20.000" />
<polygon fill="green" stroke="white" stroke-width="1"
         points="110.000,40.000 120.000,40.000 120.000,30.000 130.000,30.000 130.000,10.000 120.000,10.000 120.000,20.000 100.000,20.000 100.000,30.000 110.000,30.000" />
<polygon fill="orange" stroke="white" stroke-width="1"
         points="120.000,40.000 150.000,40.000 150.000,30.000 140.000,30.000 140.000,10.000 130.000,10.000 130.000,30.000 120.000,30.000" />
<polygon fill="maroon" stroke="white" stroke-width="1"
         points="150.000,40.000 170.000,40.000 170.000,30.000 160.000,30.000 160.000,20.000 150.000,20.000 150.000,10.000 140.000,10.000 140.000,30.000 150.000,30.000" />
<polygon fill="salmon" stroke="white" stroke-width="1"
         points="170.000,40.000 180.000,40.000 180.000,30.000 200.000,30.000 200.000,10.000 190.000,10.000 190.000,20.000 170.000,20.000" />
<polygon fill="blueviolet" stroke="white" stroke-width="1"
         points="180.000,40.000 210.000,40.000 210.000,10.000 200.000,10.000 200.000,30.000 180.000,30.000" />
<polygon fill="navy" stroke="white" stroke-width="1"
         points="80.000,30.000 100.000,30.000 100.000,20.000 120.000,20.000 120.000,10.000 90.000,10.000 90.000,20.000 80.000,20.000" />
<polygon fill="gold" stroke="white" stroke-width="1"
         points="160.000,30.000 170.000,30.000 170.000,20.000 190.000,20.000 190.000,10.000 150.000,10.000 150.000,20.000 160.000,20.000" />
<polygon fill="blue" stroke="white" stroke-width="1"
         points="40.000,20.000 90.000,20.000 90.000,10.000 40.000,10.000" />
</g>
</svg>
'''

    def test_get_polygon_points(self):
        p = MockPuzzle()
        s_matrix = copy.deepcopy(self.s_matrix_1)
        points = p.get_polygon_points(s_matrix, 3, 1)
        self.assertEquals(points, self.polygon_points_1)

    def test_build_polygon(self):
        p = MockPuzzle()
        s_matrix = copy.deepcopy(self.s_matrix_1)
        polygon = p.build_polygon(s_matrix, 3, 1)
        self.assertEquals(polygon, self.polygon_1)

    def test_format_svg(self):
        rows = [line.split() for line in self.pentominoes_solution.splitlines()]
        width = len(rows[0]) + 2
        s_matrix = ([[' '] * width]
                    + [[' '] + row + [' '] for row in rows]
                    + [[' '] * width])
        p = puzzles.Pentominoes3x20Matrix()
        svg = p.format_svg(None, s_matrix)
        self.assertEquals(svg, self.pentominoes_svg)


if __name__ == '__main__':
    unittest.main()
