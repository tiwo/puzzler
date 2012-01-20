#!/usr/bin/env python
# $Id$

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2012 by David J. Goodger
# License: GPL 2 (see __init__.py)

"""
Concrete tritrig puzzles.
"""

from puzzler import coordsys
from puzzler.puzzles.polytrigs import Tritrigs, OneSidedTritrigs


class TritrigsHex2Ring(Tritrigs):

    """0 solutions."""

    width = 5
    height = 5

    def coordinates(self):
        hole = set([(2,2,0), (2,2,1), (2,2,2), (1,2,0), (2,1,1), (3,1,2)])
        for coord in self.coordinates_hexagon(2):
            if coord not in hole:
                yield coord

    def customize_piece_data(self):
        self.piece_data['P3'][-1]['flips'] = None
        self.piece_data['P3'][-1]['rotations'] = None


class TritrigsHex3x1Ring(Tritrigs):

    """1 solution."""

    width = 5
    height = 5

    def coordinates(self):
        hole = set([(1,2,0), (2,1,1), (2,1,2)])
        for coord in self.coordinates_semiregular_hexagon(3, 1):
            if coord not in hole:
                yield coord

    def customize_piece_data(self):
        self.piece_data['Z3'][-1]['flips'] = None
        self.piece_data['Z3'][-1]['rotations'] = None


class TritrigsTrapezoid5x3Ring(Tritrigs):

    """1 solution."""

    width = 6
    height = 4

    def coordinates(self):
        hole = set([(2,1,1), (2,1,2)])
        for coord in self.coordinates_trapezoid(5, 3):
            if coord not in hole:
                yield coord

    def customize_piece_data(self):
        self.piece_data['Z3'][-1]['flips'] = None


class TritrigsStackedElongatedHexagons2x2x1(Tritrigs):

    """9 solutions."""

    width = 5
    height = 5

    def coordinates(self):
        hole = set([(1,1,2), (0,2,0), (0,2,1), (4,1,1), (3,2,0), (4,2,2)])
        for coord in self.coordinates_hexagon(2):
            if coord not in hole:
                yield coord

    def customize_piece_data(self):
        self.piece_data['P3'][-1]['flips'] = None
        self.piece_data['P3'][-1]['rotations'] = (0,1,2)


class TritrigsJaggedTrapezoid5x3(Tritrigs):

    """1 solution."""

    width = 6
    height = 4

    def coordinates(self):
        for coord in self.coordinates_trapezoid(5, 3):
            x, y, z = coord
            if y != 3:
                yield coord

    def customize_piece_data(self):
        self.piece_data['Z3'][-1]['flips'] = None


class TritrigsSpikedTriangle1(Tritrigs):

    """6 solutions."""

    width = 6
    height = 6

    def coordinates(self):
        for coord in self.coordinates_triangle(4, (1,1,0)):
            yield coord
        for coord in ((0,5,0), (1,4,2), (2,0,1), (2,0,2), (4,2,0), (5,1,1)):
            yield coordsys.TriangularGrid3D(coord)

    def customize_piece_data(self):
        self.piece_data['I3'][-1]['rotations'] = None
        self.piece_data['I3'][-1]['flips'] = None


class TritrigsSpikedTriangle2(TritrigsSpikedTriangle1):

    """0 solutions."""

    width = 6
    height = 6

    def coordinates(self):
        for coord in self.coordinates_triangle(4, (1,1,0)):
            yield coord
        for coord in ((0,4,0), (1,3,2), (3,0,1), (3,0,2), (3,3,0), (4,2,1)):
            yield coordsys.TriangularGrid3D(coord)


class TritrigsParallelogram5x2(Tritrigs):

    """9 solutions."""

    width = 6
    height = 3

    def coordinates(self):
        for coord in self.coordinates_bordered(5, 2):
            if coord != (2,1,0):
                yield coord

    def customize_piece_data(self):
        self.piece_data['P3'][-1]['rotations'] = (0,1,2)
    

class TritrigsTrapezoid6x2(Tritrigs):

    """8 solutions."""

    width = 7
    height = 3

    def coordinates(self):
        for coord in self.coordinates_trapezoid(6, 2):
            if coord != (2,1,0):
                yield coord

    def customize_piece_data(self):
        self.piece_data['P3'][-1]['flips'] = None
    

class TritrigsTrefoil1(Tritrigs):

    """0 solutions."""

    width = 5
    height = 5

    def coordinates(self):
        holes = set([(1,0,2), (4,0,1), (0,4,0)])
        for coord in self.coordinates_semiregular_hexagon(3, 1):
            if coord not in holes:
                yield coord

#     def customize_piece_data(self):
#         self.piece_data['Z3'][-1]['flips'] = None
#         self.piece_data['Z3'][-1]['rotations'] = None


class TritrigsTrefoil2(Tritrigs):

    """0 solutions."""

    width = 5
    height = 5

    def coordinates(self):
        holes = set([(2,0,0), (0,2,1), (3,2,2)])
        for coord in self.coordinates_semiregular_hexagon(3, 1):
            if coord not in holes:
                yield coord

#     def customize_piece_data(self):
#         self.piece_data['Z3'][-1]['flips'] = None
#         self.piece_data['Z3'][-1]['rotations'] = None


class TritrigsWhorl(Tritrigs):

    """0 solutions."""

    width = 5
    height = 5

    def coordinates(self):
        holes = set([(1,0,0), (0,3,1), (4,1,2)])
        for coord in self.coordinates_semiregular_hexagon(3, 1):
            if coord not in holes:
                yield coord

#     def customize_piece_data(self):
#         self.piece_data['Z3'][-1]['flips'] = None
#         self.piece_data['Z3'][-1]['rotations'] = None


class TritrigsTriangle1(Tritrigs):

    """1 solution."""

    width = 6
    height = 5

    def coordinates_hole(self):
        hole = set(self.coordinates_hexagon_unbordered(1, offset=(1, 0, 0)))
        hole.update(
            set(self.coordinates_triangle_unbordered(2, offset=(0, 3, 0))))
        return hole

    def coordinates(self):
        hole = self.coordinates_hole()
        for coord in self.coordinates_triangle(5):
            if coord not in hole:
                yield coord

    def customize_piece_data(self):
        self.piece_data['Z3'][-1]['flips'] = None


class TritrigsTriangle2(TritrigsTriangle1):

    """4 solutions."""

    def coordinates_hole(self):
        hole = set(((2,0,2), (3,0,1), (0,4,0)))
        hole.update(
            set(self.coordinates_hexagon_unbordered(1, offset=(1, 0, 0))))
        return hole


class TritrigsTriangle_no_solutions(TritrigsTriangle1):

    """
    0 solutions for each set of hole coordinates:

    set(Tritrigs().coordinates_triangle(2, offset=(1, 1, 0)))

    set(((1,0,2), (4,0,1), (0,4,0),
         (2,0,2), (3,0,1),
         (1,1,2), (0,3,0),
         (3,1,1), (1,3,0)))

    set(((1,0,2), (4,0,1), (0,4,0),
         (2,0,1), (3,0,2),
         (1,2,2), (0,2,0),
         (2,2,1), (2,2,0)))

    set(((1,0,2), (4,0,1), (0,4,0),
         (2,1,1), (2,1,2), (1,2,0),
         (2,0,1), (1,2,2), (2,2,0)))

    set(self.coordinates_triangle_unbordered(3, offset=(1, 0, 0))))

    set(self.coordinates_triangle_unbordered(3, offset=(0, 2, 0)))
    """


class TritrigsHeart1(Tritrigs):

    """50 solutions."""

    width = 5
    height = 5

    hole = set(((2,1,1), (2,2,0), (2,2,2)))

    svg_rotation = -30

    def coordinates(self):
        hole = set(((2,3,1), (1,4,0), (3,3,2)))
        hole.update(self.hole)
        for coord in self.coordinates_hexagon(2):
            if coord not in hole:
                yield coord

    def customize_piece_data(self):
        self.piece_data['Z3'][-1]['flips'] = None


class TritrigsHeart2(TritrigsHeart1):

    """52 solutions."""

    hole = set(((2,2,1), (1,2,0), (3,1,2)))


class OneSidedTritrigsSemiRegularHexagon4x1(OneSidedTritrigs):

    """many solutions."""

    width = 6
    height = 6

    def coordinates(self):
        for coord in self.coordinates_semiregular_hexagon(4,1):
            yield coord

    def customize_piece_data(self):
        """Limit I3 piece to one aspect."""
        OneSidedTritrigs.customize_piece_data(self)
        self.piece_data['I3'][-1]['rotations'] = None
        self.piece_data['I3'][-1]['flips'] = None


class OneSidedTritrigsTriangle6(OneSidedTritrigs):

    """many solutions."""

    width = 7
    height = 6

    def coordinates(self):
        hole = set(self.coordinates_hexagon_unbordered(1, offset=(1, 1, 0)))
        for coord in self.coordinates_triangle(6):
            if coord not in hole:
                yield coord

    def customize_piece_data(self):
        """Limit I3 piece to one aspect."""
        OneSidedTritrigs.customize_piece_data(self)
        self.piece_data['I3'][-1]['rotations'] = None
        self.piece_data['I3'][-1]['flips'] = None


class OneSidedTritrigsButterfly5x2(OneSidedTritrigs):

    """many solutions."""

    width = 8
    height = 5

    def coordinates(self):
        return self.coordinates_butterfly(5, 2)

    #def customize_piece_data(self):
    #    OneSidedTritrigs.customize_piece_data(self)


class OneSidedTritrigsChevron3x3(OneSidedTritrigs):

    """many solutions."""

    width = 7
    height = 7

    def coordinates(self):
        hole = set(self.coordinates_hexagon_unbordered(1, offset=(3, 2, 0)))
        for coord in self.coordinates_chevron(3, 3):
            if coord not in hole:
                yield coord

    #def customize_piece_data(self):
    #    OneSidedTritrigs.customize_piece_data(self)


class OneSidedTritrigsChevron2x4_1(OneSidedTritrigs):

    """many solutions."""

    width = 7
    height = 9

    hole = set([(4,4,0)])

    def coordinates(self):
        for coord in self.coordinates_chevron(2, 4):
            if coord not in self.hole:
                yield coord


class OneSidedTritrigsChevron2x4_2(OneSidedTritrigsChevron2x4_1):

    """many solutions."""

    hole = set([(5,4,0)])


class OneSidedTritrigsChevron8x1(OneSidedTritrigs):

    """many solutions."""

    width = 10
    height = 3

    hole = set([(8,1,0)])

    def coordinates(self):
        for coord in self.coordinates_chevron(8, 1):
            if coord not in self.hole:
                yield coord


class OneSidedTritrigsTrapezoid7x3_1(OneSidedTritrigs):

    """many solutions."""

    width = 8
    height = 4

    hole = set([(2,2,0)])

    def coordinates(self):
        for coord in self.coordinates_trapezoid(self.width - 1,
                                                self.height - 1):
            if coord not in self.hole:
                yield coord


class OneSidedTritrigsTrapezoid7x3_2(OneSidedTritrigsTrapezoid7x3_1):

    """many solutions."""

    hole = set([(3,0,0)])


class OneSidedTritrigsTrapezoid9x2_1(OneSidedTritrigsTrapezoid7x3_1):

    """many solutions."""

    width = 10
    height = 3

    hole = set([(4,0,0)])


class OneSidedTritrigsTrapezoid9x2_2(OneSidedTritrigsTrapezoid9x2_1):

    """many solutions."""

    hole = set([(3,2,0)])
