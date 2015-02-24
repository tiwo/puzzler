#!/usr/bin/env python
# $Id$

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2015 by David J. Goodger
# License: GPL 2 (see __init__.py)

"""
Concrete polystick (orders 1 through 4) puzzles.
"""

from puzzler import coordsys
from puzzler.puzzles.polysticks import Polysticks1234, OneSidedPolysticks1234


class Polysticks1234_7x7(Polysticks1234):

    """
    many solutions (very large number; over 35000 unique solutions in first
    position of X, I, & I1)
    (perfect solutions, i.e. no pieces cross).
    """

    width = 7
    height = 7

    def customize_piece_data(self):
        self.piece_data['P'][-1]['flips'] = None
        self.piece_data['P'][-1]['rotations'] = None


class Polysticks1234_10x5(Polysticks1234):

    """many solutions"""

    width = 10
    height = 5

    holes = set(((4,2,0),))

    def coordinates(self):
        coords = (
            set(self.coordinates_bordered(self.width, self.height))
            - self.holes)
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P'][-1]['flips'] = None
        self.piece_data['P'][-1]['rotations'] = None


class Polysticks1234_3x7DiamondLattice(Polysticks1234):

    """
    many solutions
    """

    width = 10
    height = 10

    svg_rotation = -45

    def customize_piece_data(self):
        self.piece_data['P'][-1]['flips'] = None
        self.piece_data['P'][-1]['rotations'] = (0,1)

    def coordinates(self):
        return self.coordinates_diamond_lattice(7, 3)


class Polysticks1234TruncatedDiamondLattice6x4(Polysticks1234):

    """many solutions"""

    width = 8
    height = 8

    svg_rotation = -45

    def coordinates(self):
        coords = set(self.coordinates_diamond_lattice(4, 4))
        for offset in ((0,4,0), (1,5,0), (4,0,0), (5,1,0)):
            coords.update(set(self.coordinates_bordered(3, 3, offset=offset)))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P'][-1]['flips'] = None
        self.piece_data['P'][-1]['rotations'] = (0,1)


class Polysticks1234TruncatedDiamondLattice8x3(Polysticks1234):

    """many solutions"""

    width = 9
    height = 9

    svg_rotation = -45

    def coordinates(self):
        coords = set(self.coordinates_diamond_lattice(6, 3))
        for offset in ((0,6,0), (6,0,0)):
            coords.update(set(self.coordinates_bordered(3, 3, offset=offset)))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P'][-1]['flips'] = None
        self.piece_data['P'][-1]['rotations'] = (0,1)


class Polysticks1234TruncatedDiamondLattice12x2(Polysticks1234):

    """many solutions"""

    width = 12
    height = 12

    svg_rotation = -45

    def coordinates(self):
        coords = set(self.coordinates_diamond_lattice(10, 2))
        for offset in ((0,9,0), (9,0,0)):
            coords.update(set(self.coordinates_bordered(3, 3, offset=offset)))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P'][-1]['flips'] = None
        self.piece_data['P'][-1]['rotations'] = (0,1)


class Polysticks1234Octagon1(Polysticks1234):

    """many solutions"""

    width = 8
    height = 8

    def coordinates(self):
        coords = set(
            list(self.coordinates_bordered(4, 8, offset=(2,0,0)))
            + list(self.coordinates_bordered(8, 4, offset=(0,2,0)))
            + list(self.coordinates_bordered(6, 6, offset=(1,1,0))))
        coords -= set(self.coordinates_bordered(2, 2, offset=(3,3,0)))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P'][-1]['flips'] = None
        self.piece_data['P'][-1]['rotations'] = None


class Polysticks1234Octagon2(Polysticks1234):

    """many solutions"""

    width = 8
    height = 8

    def coordinates(self):
        coords = set(
            list(self.coordinates_bordered(4, 8, offset=(2,0,0)))
            + list(self.coordinates_bordered(8, 4, offset=(0,2,0)))
            + list(self.coordinates_bordered(6, 6, offset=(1,1,0))))
        coords -= set(self.coordinates_unbordered(6, 2, offset=(1,3,0)))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P'][-1]['flips'] = None
        self.piece_data['P'][-1]['rotations'] = (0, 1,)


class Polysticks1234FourSquares1(Polysticks1234):

    """many solutions"""

    width = 10
    height = 10

    svg_rotation = 45

    def coordinates(self):
        coords = set()
        for i in range(4):
            coords.update(
                set(self.coordinates_bordered(4, 4, offset=(i*2,i*2,0))))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P'][-1]['flips'] = None
        self.piece_data['P'][-1]['rotations'] = (0, 1,)


class Polysticks1234ThreeSquares1(Polysticks1234):

    """many solutions"""

    width = 9
    height = 9

    svg_rotation = 45

    def coordinates(self):
        coords = set(
            list(self.coordinates_bordered(5, 5))
            + list(self.coordinates_bordered(5, 5, offset=(4,4,0)))
            + list(self.coordinates_bordered(3, 3, offset=(3,3,0))))
        return sorted(coords)

    def customize_piece_data(self):
        self.piece_data['P'][-1]['flips'] = None
        self.piece_data['P'][-1]['rotations'] = (0, 1,)


class Polysticks1234_8x8Unbordered(Polysticks1234):

    """
    0? solutions
    """

    width = 8
    height = 8

    def coordinates(self):
        return self.coordinates_unbordered(self.width, self.height)

    def customize_piece_data(self):
        self.piece_data['P'][-1]['flips'] = None
        self.piece_data['P'][-1]['rotations'] = None


class Polysticks1234_5x5DiamondLatticeRing(Polysticks1234):

    """
    0 solutions
    """

    width = 10
    height = 10

    svg_rotation = -45

    def coordinates(self):
        hole = set(
            (coord + (3,3,0))
            for coord in self.coordinates_diamond_lattice(2, 2))
        return sorted(set(self.coordinates_diamond_lattice(5, 5)) - hole)

    def customize_piece_data(self):
        self.piece_data['P'][-1]['flips'] = None
        self.piece_data['P'][-1]['rotations'] = None
