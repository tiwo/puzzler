#!/usr/bin/env python
# $Id$

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2012 by David J. Goodger
# License: GPL 2 (see __init__.py)

"""
Concrete tetrastick puzzles.
"""

import copy
from puzzler import coordsys
from puzzler.puzzles.polysticks import Tetrasticks, OneSidedTetrasticks


class Tetrasticks6x6(Tetrasticks):

    """
    1795 solutions total:

    * 72 solutions omitting H
    * 382 omitting J
    * 607 omitting L
    * 530 omitting N
    * 204 omitting Y

    All are perfect solutions (i.e. no pieces cross).
    """

    width = 8
    height = 6

    # These 9 coordinates form a minimal cover for all 12 pentominoes
    omitted_piece_coordinates = (
        (6,1,0), (6,1,1), (6,2,0), (6,2,1), (6,3,0), (6,3,1),
        (7,1,1), (7,2,1), (7,3,1))

    # These are the fixed positions for omitted pieces, to prevent duplicates.
    omitted_piece_positions = {
        'H': ((6,1,1), (6,2,0), (6,2,1), (7,1,1)),
        'J': ((6,1,1), (6,1,0), (7,2,1), (7,1,1)),
        'L': ((6,1,1), (6,1,0), (6,2,1), (6,3,1)),
        'N': ((6,1,1), (6,2,0), (7,2,1), (7,3,1)),
        'Y': ((7,1,1), (6,3,0), (7,2,1), (7,3,1)),}

    def coordinates(self):
        for coord in self.coordinates_bordered(self.height, self.height):
            yield coord
        for coord in self.omitted_piece_coordinates:
            yield coordsys.SquareGrid3D(coord)

    def customize_piece_data(self):
        self.piece_data['P'][-1]['flips'] = None
        self.piece_data['P'][-1]['rotations'] = None

    def build_matrix(self):
        self.secondary_columns += len(self.omitted_piece_coordinates)
        self.build_rows_for_omitted_pieces()
        self.build_regular_matrix(sorted(self.piece_data.keys()))

    def build_rows_for_omitted_pieces(self):
        for key, coords in self.omitted_piece_positions.items():
            row = [0] * len(self.matrix[0])
            row[self.matrix_columns[key]] = key
            for (x,y,z) in coords:
                label = '%0*i,%0*i,%0*i' % (
                    self.x_width, x, self.y_width, y, self.z_width, z)
                row[self.matrix_columns[label]] = label
            self.matrix.append(row)
            #self.build_matrix_row(key, coords)

    def build_regular_matrix(self, keys):
        for key in keys:
            for coords, aspect in self.pieces[key]:
                for y in range(self.height - aspect.bounds[1]):
                    # can't use self.width; omitted pieces are handled above:
                    for x in range(self.height - aspect.bounds[0]):
                        translated = aspect.translate((x, y, 0))
                        if translated.issubset(self.solution_coords):
                            self.build_matrix_row(key, translated)


class Tetrasticks7x7Unbordered(Tetrasticks6x6):

    """0 solutions"""

    width = 9
    height = 7

    # These 9 coordinates form a minimal cover for all 12 pentominoes
    omitted_piece_coordinates = (
        (7,1,0), (7,1,1), (7,2,0), (7,2,1), (7,3,0), (7,3,1),
        (8,1,1), (8,2,1), (8,3,1))

    # These are the fixed positions for omitted pieces, to prevent duplicates.
    omitted_piece_positions = {
        'H': ((7,1,1), (7,2,0), (7,2,1), (8,1,1)),
        'J': ((7,1,1), (7,1,0), (8,2,1), (8,1,1)),
        'L': ((7,1,1), (7,1,0), (7,2,1), (7,3,1)),
        'N': ((7,1,1), (7,2,0), (8,2,1), (8,3,1)),
        'Y': ((8,1,1), (7,3,0), (8,2,1), (8,3,1)),}

    def coordinates(self):
        for coord in self.coordinates_unbordered(self.height, self.height):
            yield coord
        for coord in self.omitted_piece_coordinates:
            yield coordsys.SquareGrid3D(coord)


class Tetrasticks3x5DiamondLattice(Tetrasticks):

    """0 solutions"""

    width = 8
    height = 8

    svg_rotation = -45

    def customize_piece_data(self):
        self.piece_data['!'] = ((), {})
        self.piece_data['P'][-1]['flips'] = None
        self.piece_data['P'][-1]['rotations'] = (0,1)

    def build_matrix(self):
        self.build_rows_for_omitted_pieces()
        self.build_regular_matrix(sorted(self.pieces.keys()))

    def coordinates(self):
        return self.coordinates_diamond_lattice(5, 3)


class OneSidedTetrasticks5x5DiamondLattice(OneSidedTetrasticks):

    """
    107 solutions (see "Covering the Aztec Diamond with One-sided Tetrasticks,
    Extended Version", by `Alfred Wassermann`_).

    .. _Alfred Wassermann:
       http://did.mat.uni-bayreuth.de/~alfred/home/index.html
    """

    width = 10
    height = 10

    check_for_duplicates = False

    svg_rotation = -45

    @classmethod
    def components(cls):
        return (OneSidedTetrasticks5x5DiamondLattice_A,
                OneSidedTetrasticks5x5DiamondLattice_B,
                OneSidedTetrasticks5x5DiamondLattice_C,
                OneSidedTetrasticks5x5DiamondLattice_D,
                OneSidedTetrasticks5x5DiamondLattice_E,
                OneSidedTetrasticks5x5DiamondLattice_F,)

    def _customize_piece_data_I(self):
        """
        Limit I piece to horizontal when X is symmetrical (on the diagonal).
        """
        OneSidedTetrasticks.customize_piece_data(self)
        self.piece_data['I'][-1]['rotations'] = None

    def coordinates(self):
        return self.coordinates_diamond_lattice(5, 5)

    def build_matrix(self):
        """"""
        keys = sorted(self.pieces.keys())
        x_coords, x_aspect = self.pieces['X'][0]
        translated = x_aspect.translate(self.X_offset)
        self.build_matrix_row('X', translated)
        keys.remove('X')
        self.build_regular_matrix(keys)


class OneSidedTetrasticks5x5DiamondLattice_A(
    OneSidedTetrasticks5x5DiamondLattice):

    """? solutions."""

    X_offset = (4,4,0)

    def customize_piece_data(self):
        self._customize_piece_data_I()


class OneSidedTetrasticks5x5DiamondLattice_B(
    OneSidedTetrasticks5x5DiamondLattice):

    """? solutions."""

    X_offset = (4,5,0)


class OneSidedTetrasticks5x5DiamondLattice_C(
    OneSidedTetrasticks5x5DiamondLattice):

    """? solutions."""

    X_offset = (5,5,0)

    def customize_piece_data(self):
        self._customize_piece_data_I()


class OneSidedTetrasticks5x5DiamondLattice_D(
    OneSidedTetrasticks5x5DiamondLattice):

    """? solutions."""

    X_offset = (4,6,0)


class OneSidedTetrasticks5x5DiamondLattice_E(
    OneSidedTetrasticks5x5DiamondLattice):

    """? solutions."""

    X_offset = (5,6,0)


class OneSidedTetrasticks5x5DiamondLattice_F(
    OneSidedTetrasticks5x5DiamondLattice):

    """? solutions."""

    X_offset = (4,7,0)


class OneSidedTetrasticks8x8CenterHole(OneSidedTetrasticks):

    """
    ? solutions
    """

    width = 8
    height = 8

    def customize_piece_data(self):
        OneSidedTetrasticks.customize_piece_data(self)
        self.piece_data['P'][-1]['rotations'] = None
        # enough for uniqueness?

    def coordinates(self):
        hole = coordsys.SquareGrid3DCoordSet(self.coordinates_unbordered(4, 4))
        hole = hole.translate((2, 2, 0))
        for coord in self.coordinates_bordered(self.width, self.height):
            if coord not in hole:
                yield coord


class OneSidedTetrasticks8x8ClippedCorners1(OneSidedTetrasticks):

    """
    ? solutions
    """

    width = 8
    height = 8

    def coordinates(self):
        hole = set(
            ((0,5,1),(0,6,0),(0,6,1),(0,7,0),(1,6,1),(1,7,0),
             (5,0,0),(6,0,0),(6,0,1),(6,1,0),(7,0,1),(7,1,1)))
        for coord in self.coordinates_bordered(self.width, self.height):
            if coord not in hole:
                yield coord


class OneSidedTetrasticks8x8ClippedCorners2(OneSidedTetrasticks):

    """
    ? solutions
    """

    width = 8
    height = 8

    def coordinates(self):
        hole = set(
            ((0,5,1),(0,6,0),(0,6,1),(0,7,0),(1,6,1),(1,7,0),
             (5,7,0),(6,6,0),(6,6,1),(6,7,0),(7,5,1),(7,6,1)))
        for coord in self.coordinates_bordered(self.width, self.height):
            if coord not in hole:
                yield coord


class OneSidedTetrasticks8x8ClippedCorner(OneSidedTetrasticks):

    """
    ? solutions
    """

    width = 8
    height = 8

    def coordinates(self):
        hole = set(
            ((0,4,1),(0,5,0),(0,5,1),(0,6,0),(0,6,1),(0,7,0),
             (1,5,1),(1,6,0),(1,6,1),(1,7,0),(2,6,1),(2,7,0)))
        for coord in self.coordinates_bordered(self.width, self.height):
            if coord not in hole:
                yield coord


class OneSidedTetrasticks6x10CenterHole(OneSidedTetrasticks):

    """
    ? solutions
    """

    width = 10
    height = 6

    def coordinates(self):
        hole = coordsys.SquareGrid3DCoordSet(self.coordinates_bordered(2, 2))
        hole = hole.translate((4, 2, 0))
        for coord in self.coordinates_bordered(self.width, self.height):
            if coord not in hole:
                yield coord


class OneSidedTetrasticks6x10Slot(OneSidedTetrasticks):

    """
    ? solutions
    """

    width = 10
    height = 6

    def coordinates(self):
        hole = set(((3,2,1),(4,2,1),(5,2,1),(6,2,1)))
        for coord in self.coordinates_bordered(self.width, self.height):
            if coord not in hole:
                yield coord


class OneSidedTetrasticks6x10SideHoles(OneSidedTetrasticks):

    """
    ? solutions
    """

    width = 10
    height = 6

    def coordinates(self):
        hole = set(((0,2,1),(4,0,0),(4,5,0),(9,2,1)))
        for coord in self.coordinates_bordered(self.width, self.height):
            if coord not in hole:
                yield coord


class OneSidedTetrasticks6x10ClippedCorners1(OneSidedTetrasticks):

    """
    ? solutions
    """

    width = 10
    height = 6

    def coordinates(self):
        hole = set(((0,4,1),(0,5,0),(8,0,0),(9,0,1)))
        for coord in self.coordinates_bordered(self.width, self.height):
            if coord not in hole:
                yield coord


class OneSidedTetrasticks6x10ClippedCorners2(OneSidedTetrasticks):

    """
    ? solutions
    """

    width = 10
    height = 6

    def coordinates(self):
        hole = set(((0,4,1),(0,5,0),(8,5,0),(9,4,1)))
        for coord in self.coordinates_bordered(self.width, self.height):
            if coord not in hole:
                yield coord


class OneSidedTetrasticks6x10ClippedCorners3(OneSidedTetrasticks):

    """
    ? solutions
    """

    width = 10
    height = 6

    def coordinates(self):
        hole = set(((8,0,0),(8,5,0),(9,0,1),(9,4,1)))
        for coord in self.coordinates_bordered(self.width, self.height):
            if coord not in hole:
                yield coord


class OneSidedWeldedTetrasticks5x5(OneSidedTetrasticks):

    """
    3 solutions (perfect solutions, i.e. no pieces cross).
    2 solutions are perfectly symmetrical in reflection.
    """

    width = 5
    height = 5

    check_for_duplicates = True
    duplicate_conditions = (
        {'rotation': 1},
        {'rotation': 2},
        {'rotation': 3},
        {'x_reversed': True},
        {'y_reversed': True},
        {'xy_swapped': True},
        {'x_reversed': True,
         'rotation': 1},
        {'y_reversed': True,
         'rotation': 1},
        {'xy_swapped': True,
         'rotation': 1},
        {'x_reversed': True,
         'rotation': 2},
        {'y_reversed': True,
         'rotation': 2},
        {'xy_swapped': True,
         'rotation': 2},
        {'x_reversed': True,
         'rotation': 3},
        {'y_reversed': True,
         'rotation': 3},
        {'xy_swapped': True,
         'rotation': 3},)

    def customize_piece_data(self):
        for key in self.unwelded_pieces:
            del self.piece_data[key]
        self.asymmetric_pieces = sorted(
            set(self.asymmetric_pieces) - set(self.unwelded_pieces))
        OneSidedTetrasticks.customize_piece_data(self)


class OneSidedWeldedTetrasticks5x2DiamondLattice(OneSidedWeldedTetrasticks5x5):

    """0 solutions"""

    width = 7
    height = 7

    check_for_duplicates = False

    def coordinates(self):
        return self.coordinates_diamond_lattice(5, 2)


class OneSidedWeldedTetrasticks6x6Unbordered(OneSidedWeldedTetrasticks5x5):

    """0 solutions"""

    width = 6
    height = 6

    check_for_duplicates = False

    def coordinates(self):
        return self.coordinates_unbordered(6, 6)
