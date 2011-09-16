#!/usr/bin/env python
# $Id$

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2006 by David J. Goodger
# License: GPL 2 (see alltests.py)

import sys
import copy
import unittest
from cStringIO import StringIO
from pprint import pprint, pformat

import puzzler
from puzzler import puzzles
from puzzler import coordsys


class Struct:

    """Stores data attributes for dotted-attribute access."""

    def __init__(self, **keyword_args):
        self.__dict__.update(keyword_args)


class MockPuzzle(puzzles.Puzzle2D):

    height = 4
    width = 5
    piece_colors = {'#': 'black'}
    coord_class = coordsys.Cartesian2D

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
         points="30.000,50.000 40.000,50.000 40.000,40.000 50.000,40.000 50.000,50.000 60.000,50.000 60.000,30.000 50.000,30.000 50.000,20.000 60.000,20.000 60.000,10.000 40.000,10.000 40.000,20.000 30.000,20.000 30.000,10.000 10.000,10.000 10.000,20.000 20.000,20.000 20.000,30.000 10.000,30.000 10.000,40.000 30.000,40.000">
<desc>#</desc>
</polygon>
'''
    pentominoes_solution = """\
U U X P P P L L L L F T T T W W Z V V V
U X X X P P L N N F F F T W W Y Z Z Z V
U U X I I I I I N N N F T W Y Y Y Y Z V"""
    pentominoes_svg = '''\
<?xml version="1.0" standalone="no"?>
<!-- Created by Polyform Puzzler (http://puzzler.sourceforge.net/) -->
<svg width="220" height="50" viewBox="0 0 220 50"
     xmlns="http://www.w3.org/2000/svg"
     xmlns:xlink="http://www.w3.org/1999/xlink">
<g>
<polygon fill="turquoise" stroke="white" stroke-width="1"
         points="10.000,40.000 30.000,40.000 30.000,30.000 20.000,30.000 20.000,20.000 30.000,20.000 30.000,10.000 10.000,10.000">
<desc>U</desc>
</polygon>
<polygon fill="red" stroke="white" stroke-width="1"
         points="30.000,40.000 40.000,40.000 40.000,30.000 50.000,30.000 50.000,20.000 40.000,20.000 40.000,10.000 30.000,10.000 30.000,20.000 20.000,20.000 20.000,30.000 30.000,30.000">
<desc>X</desc>
</polygon>
<polygon fill="magenta" stroke="white" stroke-width="1"
         points="40.000,40.000 70.000,40.000 70.000,20.000 50.000,20.000 50.000,30.000 40.000,30.000">
<desc>P</desc>
</polygon>
<polygon fill="lime" stroke="white" stroke-width="1"
         points="70.000,40.000 110.000,40.000 110.000,30.000 80.000,30.000 80.000,20.000 70.000,20.000">
<desc>L</desc>
</polygon>
<polygon fill="green" stroke="white" stroke-width="1"
         points="110.000,40.000 120.000,40.000 120.000,30.000 130.000,30.000 130.000,10.000 120.000,10.000 120.000,20.000 100.000,20.000 100.000,30.000 110.000,30.000">
<desc>F</desc>
</polygon>
<polygon fill="darkorange" stroke="white" stroke-width="1"
         points="120.000,40.000 150.000,40.000 150.000,30.000 140.000,30.000 140.000,10.000 130.000,10.000 130.000,30.000 120.000,30.000">
<desc>T</desc>
</polygon>
<polygon fill="maroon" stroke="white" stroke-width="1"
         points="150.000,40.000 170.000,40.000 170.000,30.000 160.000,30.000 160.000,20.000 150.000,20.000 150.000,10.000 140.000,10.000 140.000,30.000 150.000,30.000">
<desc>W</desc>
</polygon>
<polygon fill="plum" stroke="white" stroke-width="1"
         points="170.000,40.000 180.000,40.000 180.000,30.000 200.000,30.000 200.000,10.000 190.000,10.000 190.000,20.000 170.000,20.000">
<desc>Z</desc>
</polygon>
<polygon fill="blueviolet" stroke="white" stroke-width="1"
         points="180.000,40.000 210.000,40.000 210.000,10.000 200.000,10.000 200.000,30.000 180.000,30.000">
<desc>V</desc>
</polygon>
<polygon fill="navy" stroke="white" stroke-width="1"
         points="80.000,30.000 100.000,30.000 100.000,20.000 120.000,20.000 120.000,10.000 90.000,10.000 90.000,20.000 80.000,20.000">
<desc>N</desc>
</polygon>
<polygon fill="gold" stroke="white" stroke-width="1"
         points="160.000,30.000 170.000,30.000 170.000,20.000 190.000,20.000 190.000,10.000 150.000,10.000 150.000,20.000 160.000,20.000">
<desc>Y</desc>
</polygon>
<polygon fill="blue" stroke="white" stroke-width="1"
         points="40.000,20.000 90.000,20.000 90.000,10.000 40.000,10.000">
<desc>I</desc>
</polygon>
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
        p = puzzles.Pentominoes3x20()
        svg = p.format_svg(s_matrix=s_matrix)
        self.assertEquals(svg, self.pentominoes_svg)


class Polytrig_Test_Puzzle(puzzles.Polytrigs12):

    width = 3
    height = 2

    def coordinates(self):
        return self.coordinates_trapezoid(self.width - 1, self.height - 1)

    def customize_piece_data(self):
        self.piece_data['L2'][-1]['flips'] = None
        self.piece_data['L2'][-1]['rotations'] = (0,1,2)

#     def format_svg(self, solution=None, s_matrix=None):
#         pprint(s_matrix)
#         return 'test'


class Test_Polytrigs(unittest.TestCase):

    def test_details(self):
        p = Polytrig_Test_Puzzle()
        self.assertEquals(
            sorted(p.solution_coords),
            [(0, 0, 0), (0, 0, 1), (0, 1, 0), (1, 0, 0), (1, 0, 1), (1, 0, 2),
             (2, 0, 2)])
        self.assertEquals(len(p.pieces), 4)
        # number of aspects:
        self.assertEquals(len(p.pieces['I1']), 3)
        self.assertEquals(len(p.pieces['I2']), 3)
        # 3 because of customize_piece_data; normally 6
        self.assertEquals(len(p.pieces['L2']), 3)
        self.assertEquals(len(p.pieces['V2']), 6)
        # number of rows in the matrix
        # (normally 1 + 7 + 1 + 4 + 9 = 22 for the full puzzle):
        self.assertEquals(len(p.matrix), 20)

    output = r"""solving Polytrig_Test_Puzzle:

solution 1:
0,0,0 1,0,0 I2
0,1,0 2,0,2 L2
0,0,1 I1
1,0,1 1,0,2 V2

   __L2__
  /V2   /L2
I1  \ V2  \
/_I2_\/_I2_\

solution 2:
0,0,0 1,0,0 I2
0,1,0 2,0,2 L2
0,0,1 1,0,2 V2
1,0,1 I1

   __L2__
  /V2   /L2
V2  \ I1  \
/_I2_\/_I2_\

2 solutions"""

    svg_output = """\
<?xml version="1.0" standalone="no"?>
<!-- Created by Polyform Puzzler (http://puzzler.sourceforge.net/) -->
<svg width="35.0" height="17.3205080757" viewBox="0 0 35.0 17.3205080757"
     xmlns="http://www.w3.org/2000/svg"
     xmlns:xlink="http://www.w3.org/1999/xlink">
<g>
<path stroke="steelblue" stroke-width="1.6" stroke-linecap="round"
      fill="none" d="M 6.300,10.739 l 2.400,-4.157">
<desc>I1</desc>
</path>
<path stroke="gray" stroke-width="1.6" stroke-linecap="round"
      fill="none" d="M 15.000,12.990 l 7.400,0.000 M 7.600,12.990 l 7.400,0.000">
<desc>I2</desc>
</path>
<path stroke="teal" stroke-width="1.6" stroke-linecap="round"
      fill="none" d="M 12.600,4.330 l 4.200,0.000 M 16.800,4.330 a 5.543,5.543 0 0,1 4.800,2.771 M 23.700,10.739 l -2.100,-3.637">
<desc>L2</desc>
</path>
<path stroke="lightcoral" stroke-width="1.6" stroke-linecap="round"
      fill="none" d="M 13.500,10.392 l -2.200,-3.811 M 16.500,10.392 a 1.732,1.732 0 0,1 -3.000,0.000 M 16.500,10.392 l 2.200,-3.811">
<desc>V2</desc>
</path>
</g>
</svg>
"""

    def test_solution(self):
        stream = StringIO()
        self.assertEquals(
            puzzler.run(Polytrig_Test_Puzzle, output_stream=stream), 2)
        output = stream.getvalue()
        self.assert_(output.startswith(self.output))
        stream.seek(0)
        svg_stream = StringIO()
        settings = Struct(
            read_solution = stream,
            svg = svg_stream,
            x3d = None)
        puzzler.read_solution(Polytrig_Test_Puzzle, settings)
        svg_output = svg_stream.getvalue()
        self.assertEquals(svg_output, self.svg_output)


if __name__ == '__main__':
    unittest.main()
