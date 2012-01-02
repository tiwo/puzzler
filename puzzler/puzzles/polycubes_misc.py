#!/usr/bin/env python
# $Id$

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2012 by David J. Goodger
# License: GPL 2 (see __init__.py)

"""
Miscellaneous concrete polycube puzzles.
"""

from puzzler.puzzles.polycubes import SomaCubes


class DiabolicalCube(SomaCubes):

    """
    13 solutions.

    The Diabolical Cube dates from the 19th century, published in `Puzzles Old
    and New`, London 1893, by Professor L. Hoffmann.  The puzzle contains one
    piece from each of the solid polyominoes of orders 2 through 7 (i.e one
    solid domino, ..., one solid heptomino).

    More info: http://www.johnrausch.com/PuzzlingWorld/chap03a.htm
    """

    height = 3
    width = 3
    depth = 3

    piece_data = {
        'I': (((0, 1, 0),), {}),
        'V': (((0, 1, 0), (1, 0, 0)), {}),
        'O': (((0, 1, 0), (1, 0, 0), (1, 1, 0)), {}),
        'U': (((0, 1, 0), (1, 0, 0), (2, 0, 0), (2, 1, 0)), {}),
        'W': (((0, 1, 0), (0, 2, 0), (1, 0, 0), (1, 1, 0), (2, 0, 0)), {}),
        'L': (((0, 1, 0), (0, 2, 0), (1, 0, 0), (1, 1, 0), (1, 2, 0),
               (2, 0, 0)), {})}
    """(0,0,0) is implied."""

    piece_colors = {
        'V': 'blue',
        'I': 'red',
        'O': 'green',
        'L': 'blueviolet',
        'U': 'orange',
        'W': 'navy',
        '0': 'gray',
        '1': 'black'}

    check_for_duplicates = True
    duplicate_conditions = ({'z_reversed': True},
                            {'xy_swapped': True},
                            {'z_reversed': True, 'xy_swapped': True},)

    def customize_piece_data(self):
        """
        Symmetry: W fixed to XY plane, one orientation; also L unflipped,
        since W has reflexive symmetry.
        """
        self.piece_data['W'][-1]['flips'] = None
        self.piece_data['W'][-1]['axes'] = None
        self.piece_data['W'][-1]['rotations'] = None
        self.piece_data['L'][-1]['flips'] = None


class SheldonsCube(DiabolicalCube):

    """
    Nancy Sheldon's variations on the Diabolical Cube:

    1. Replace the 'U' pentomino with a 'P' pentomino.
    2. Replace the 'L' heptomino with a symmetrical 'T' heptomino.
    3. Both 1 & 2.
    """

    piece_colors = DiabolicalCube.piece_colors.copy()
    piece_colors['P'] = 'magenta'
    piece_colors['T'] = 'teal'

    replace_U = False
    replace_L = False

    def customize_piece_data(self):
        if self.replace_U:
            del self.piece_data['U']
            self.piece_data['P'] = (
                ((0, 1, 0), (1, 0, 0), (1, 1, 0), (2, 0, 0)), {})
        if self.replace_L:
            del self.piece_data['L']
            self.piece_data['T'] = (
                ((0, 1, 0), (0, 2, 0), (1, 0, 0), (1, 1, 0), (1, 2, 0),
                 (2, 1, 0)), {})
        self.piece_data['W'][-1]['flips'] = None
        self.piece_data['W'][-1]['axes'] = None
        self.piece_data['W'][-1]['rotations'] = None


class SheldonsCube1(SheldonsCube):

    replace_U = True


class SheldonsCube2(SheldonsCube):

    replace_L = True


class SheldonsCube3(SheldonsCube):

    replace_U = True
    replace_L = True
