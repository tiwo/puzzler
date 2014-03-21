#!/usr/bin/env python
# -*- coding: utf-8 -*-
# $Id: polyominoes45.py 452 2012-03-31 12:25:25Z goodger $

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2014 by David J. Goodger
# License: GPL 2 (see __init__.py)

"""
Concrete miscellaneous polyomino puzzles.
"""

import copy
from pprint import pprint, pformat

from puzzler.puzzles.polyominoes import Polyominoes


class PolyominoesPuzzleArt(Polyominoes):

    """
    Specify a puzzle graphically. Whitespace in `self.puzzle_art` defines the
    puzzle space (via `self.coordinates`, which sets `self.height` and
    `self.width`). The `self.piece_art` dictionary defines pieces graphically.
    """

    implied_0 = False

    puzzle_art = None
    """A multi-line string where '#' is a border square (not part of the
    puzzle space), and spaces form the puzzle space."""

    piece_art = None
    """A mapping of piece name to 2-tuple: puzzle piece art multi-line string
    ('#' is a filled square), and a dictionary of piece-specific aspect
    restrictions."""

    base_aspect_restrictions = {}

    def customize_piece_data(self):
        total_squares = 0
        for name, art_data in self.piece_art.iteritems():
            art, piece_aspect_restrictions = art_data
            aspect_restrictions = copy.deepcopy(self.base_aspect_restrictions)
            aspect_restrictions.update(piece_aspect_restrictions)
            coordinates, width, height, squares = self.coordinates_from_art(art)
            total_squares += len(coordinates)
            self.piece_data[name] = (tuple(coordinates), aspect_restrictions)

    def coordinates_from_art(self, art, include='#'):
        lines = art.splitlines()
        squares = 0
        height = len(lines)
        width = 0
        coordinates = []
        for y, line in enumerate(reversed(lines)):
            width = max(width, len(line))
            for x, char in enumerate(line):
                if char == include:
                    coordinates.append((x, y))
                    squares += 1
        return coordinates, width, height, squares

    def coordinates(self):
        coordinates, width, height, squares = self.coordinates_from_art(
            self.puzzle_art, include=' ')
        self.height = height
        self.width = width
        coordinates.sort()
        assert len(coordinates) == squares
        for coord in coordinates:
            yield coord


class PolyominoesPuzzleArtFixed(PolyominoesPuzzleArt):

    """
    Pieces each have a single fixed aspect, no rotation or flipping alowed.
    """

    base_aspect_restrictions = {'flips': None, 'rotations': None}


class PuzzleBits56(PolyominoesPuzzleArtFixed):

    puzzle_art = """\
###########
###   #####
###   #####
##  #  ####
##     ####
#   #   ###
#       ###
#   #   ###
##     ####
###########"""

    piece_art = {
        'I': (
"""\
###
""", {}),
        'D1': (
"""\
#
#
""", {}),
        'L4': (
"""\
#
#
##
""", {}),
        'I3': (
"""\
#
#
#
""", {}),
        'Z': (
"""\
##
 #
 ##
""", {}),
        'P': (
"""\
###
 ##
""", {}),
        'T ': (
"""\
 #
 #
###
""", {}),
        'V3': (
"""\
#
##
""", {}),
        'Y': (
"""\
#
#
##
#
""", {}),
        'L2': (
"""\
##
#
#
""", {}),
        }


class PuzzleBitsA(PolyominoesPuzzleArtFixed):

    puzzle_art = """\
###########
#         #
#         #
#         #
#         #
#         #
##### #####
####   ####
###########"""

    piece_art = {
        'T6': (
"""\
 #
 #
 #
###
""", {}),
        'I3': (
"""\
#
#
#
""", {}),
        'L4': (
"""\
 #
 #
##
""", {}),
        'D1': (
"""\
#
#
""", {}),
        'N': (
"""\
 ###
##
""", {}),
        'T': (
"""\
####
 #
 #
""", {}),
        'T4': (
"""\
 #
###
""", {}),
        'Q': (
"""\
 #  #
 ####
## #
""", {}),
        'Z4': (
"""\
 #
##
#
""", {}),
        'V3': (
"""\
##
#
""", {}),
        'I': (
"""\
###
""", {}),
        }


class PuzzleBits25(PolyominoesPuzzleArtFixed):

    puzzle_art = """\
###############
###      ######
##        #####
##        #####
##        #####
#          ####
###############"""

    piece_art = {
        'T4': (
"""\
 #
###
""", {}),
        'T5': (
"""\
###
 #
 #
""", {}),
        'L1': (
"""\
 #
 #
 #
##
""", {}),
        'L2': (
"""\
#
####
""", {}),
        'Y': (
"""\
#
##
#
#
""", {}),
        'D1': (
"""\
#
#
""", {}),
        'I4': (
"""\
####
""", {}),
        'S4': (
"""\
##
##
""", {}),
        'C6': (
"""\
##
 #
 #
##
""", {}),
        }


class PuzzleBits9(PolyominoesPuzzleArtFixed):

    puzzle_art = """\
###############
#####   #######
#####   #######
#####   #######
###### ########
### #   # #####
##         ####
### #   # #####
#####   #######
##### # #######
##### # #######
####  #  ######
###############
###############"""

    piece_art = {
        'X': (
"""\
 #
###
 #
""", {}),
        'T1': (
"""\
#
##
#
""", {}),
        'T2': (
"""\
 #
###
""", {}),
        'L5': (
"""\
#
#
#
##
""", {}),
        'L4': (
"""\
 #
 #
##
""", {}),
        'Y': (
"""\
#
##
#
#
""", {}),
        'V1': (
"""\
#
##
""", {}),
        'V2': (
"""\
##
#
""", {}),
        'D1': (
"""\
#
#
""", {}),
        'D2': (
"""\
##
""", {}),
        'I3': (
"""\
#
#
#
""", {}),
        }
