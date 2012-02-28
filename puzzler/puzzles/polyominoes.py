#!/usr/bin/env python
# $Id$

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2012 by David J. Goodger
# License: GPL 2 (see __init__.py)

"""
Polyomino puzzle base classes.
"""

import copy

from puzzler import coordsys
from puzzler.puzzles import Puzzle2D, OneSidedLowercaseMixin


class Polyominoes(Puzzle2D):

    coord_class = coordsys.Cartesian2D

    asymmetric_pieces = []
    """Pieces without reflexive symmetry, different from their mirror images."""

    def format_solution(self, solution,  normalized=True, **kwargs):
        """Convert solutions to uppercase to avoid duplicates."""
        formatted = Puzzle2D.format_solution(
            self, solution, normalized, **kwargs)
        if normalized:
            return formatted.upper()
        else:
            return formatted


class Monomino(Polyominoes):

    piece_data = {'O1': ((), {}),}
    """(0,0) is implied."""

    symmetric_pieces = ['O1']
    """Pieces with reflexive symmetry, identical to their mirror images."""

    piece_colors = {'O1': 'blue',}


class Domino(Polyominoes):

    piece_data = {'I2': (((0,1),), {}),}
    """(0,0) is implied."""

    symmetric_pieces = ['I2']
    """Pieces with reflexive symmetry, identical to their mirror images."""

    piece_colors = {'I2': 'red',}


class Trominoes(Polyominoes):

    piece_data = {
        'I3': (((0,1), (0,2)), {}),
        'V3': (((0,1), (1,0)), {}),}
    """(0,0) is implied."""

    symmetric_pieces = ['I3', 'V3']
    """Pieces with reflexive symmetry, identical to their mirror images."""

    piece_colors = {
        'I3': 'green',
        'V3': 'darkorange'}


class OneSidedTrominoes(OneSidedLowercaseMixin, Trominoes):

    pass


class Tetrominoes(Polyominoes):

    piece_data = {
        'I4': (((0,1), (0,2), (0,3)), {}),
        'L4': (((0,1), (0,2), (1,0)), {}),
        'O4': (((0,1), (1,0), (1,1)), {}),
        'T4': (((1,1), (1,0), (2,0)), {}),
        'Z4': (((0,1), (1,1), (1,2)), {}),}
    """(0,0) is implied."""

    symmetric_pieces = ['I4', 'O4', 'T4']
    """Pieces with reflexive symmetry, identical to their mirror images."""

    asymmetric_pieces = ['L4', 'Z4']
    """Pieces without reflexive symmetry, different from their mirror images."""

    piece_colors = {
        'I4': 'magenta',
        'L4': 'lime',
        'O4': 'plum',
        'T4': 'blueviolet',
        'Z4': 'maroon'}


class OneSidedTetrominoes(OneSidedLowercaseMixin, Tetrominoes):

    pass


class Pentominoes(Polyominoes):

    piece_data = {
        'F': (((-1,-1), ( 0,-1), ( 1,0), ( 0,1)), {}),
        'I': (((-2, 0), (-1, 0), ( 1,0), ( 2,0)), {}),
        'L': (((-2, 0), (-1, 0), ( 1,0), ( 1,1)), {}),
        'N': (((-2, 0), (-1, 0), ( 0,1), ( 1,1)), {}), # flipped N
        'P': (((-1, 0), ( 1, 0), ( 0,1), ( 1,1)), {}), # flipped P
        'T': (((-1,-1), (-1, 0), (-1,1), ( 1,0)), {}),
        'U': (((-1,-1), ( 0,-1), ( 0,1), (-1,1)), {}),
        'V': (((-2, 0), (-1, 0), ( 0,1), ( 0,2)), {}),
        'W': ((( 1,-1), ( 1, 0), ( 0,1), (-1,1)), {}),
        'X': (((-1, 0), ( 0,-1), ( 1,0), ( 0,1)), {}),
        'Y': (((-2, 0), (-1, 0), ( 1,0), ( 0,1)), {}),
        'Z': (((-1,-1), (-1, 0), ( 1,0), ( 1,1)), {}),}
    """(0,0) is implied."""

    symmetric_pieces = 'I T U V W X'.split()
    """Pieces with reflexive symmetry, identical to their mirror images."""

    asymmetric_pieces = 'F L P N Y Z'.split()
    """Pieces without reflexive symmetry, different from their mirror images."""

    piece_colors = {
        'I': 'blue',
        'X': 'red',
        'F': 'green',
        'L': 'lime',
        'N': 'navy',
        'P': 'magenta',
        'T': 'darkorange',
        'U': 'turquoise',
        'V': 'blueviolet',
        'W': 'maroon',
        'Y': 'gold',
        'Z': 'plum',
        '0': 'gray',
        '1': 'black'}


class OneSidedPentominoes(OneSidedLowercaseMixin, Pentominoes):

    pass


class PentominoesPlusSquareTetromino(Pentominoes):

    piece_data = copy.deepcopy(Pentominoes.piece_data)
    piece_data['S'] = (((1, 0), (0, 1), (1, 1)), {})
    symmetric_pieces = (
        Pentominoes.symmetric_pieces + ['S'])
    piece_colors = copy.deepcopy(Pentominoes.piece_colors)
    piece_colors['S'] = 'gray'


class PentominoesPlusMonomino(Pentominoes):

    piece_data = copy.deepcopy(Pentominoes.piece_data)
    piece_data['M'] = ((), {})
    symmetric_pieces = (
        Pentominoes.symmetric_pieces + ['M'])
    piece_colors = copy.deepcopy(Pentominoes.piece_colors)
    piece_colors['M'] = 'black'


class PentominoesPlusTetrominoes(Pentominoes):

    piece_data = copy.deepcopy(Pentominoes.piece_data)
    piece_data.update(copy.deepcopy(Tetrominoes.piece_data))
    symmetric_pieces = (
        Pentominoes.symmetric_pieces + Tetrominoes.symmetric_pieces)
    asymmetric_pieces = (
        Pentominoes.asymmetric_pieces + Tetrominoes.asymmetric_pieces)
    piece_colors = copy.deepcopy(Pentominoes.piece_colors)
    piece_colors.update(Tetrominoes.piece_colors)


class Polyominoes12(Polyominoes):

    piece_data = copy.deepcopy(Monomino.piece_data)
    piece_data.update(copy.deepcopy(Domino.piece_data))
    symmetric_pieces = (
        Monomino.symmetric_pieces + Domino.symmetric_pieces)
    asymmetric_pieces = []
    piece_colors = copy.deepcopy(Monomino.piece_colors)
    piece_colors.update(Domino.piece_colors)


class Polyominoes123(Polyominoes12):

    piece_data = copy.deepcopy(Polyominoes12.piece_data)
    piece_data.update(copy.deepcopy(Trominoes.piece_data))
    symmetric_pieces = (
        Polyominoes12.symmetric_pieces + Trominoes.symmetric_pieces)
    asymmetric_pieces = Trominoes.asymmetric_pieces[:]
    piece_colors = copy.deepcopy(Polyominoes12.piece_colors)
    piece_colors.update(Trominoes.piece_colors)


class Polyominoes1234(Polyominoes123):

    piece_data = copy.deepcopy(Polyominoes123.piece_data)
    piece_data.update(copy.deepcopy(Tetrominoes.piece_data))
    symmetric_pieces = (
        Polyominoes123.symmetric_pieces + Tetrominoes.symmetric_pieces)
    asymmetric_pieces = (
        Polyominoes123.asymmetric_pieces + Tetrominoes.asymmetric_pieces)
    piece_colors = copy.deepcopy(Polyominoes123.piece_colors)
    piece_colors.update(Tetrominoes.piece_colors)


class OneSidedPolyominoes1234(OneSidedLowercaseMixin, Polyominoes1234):

    pass


class Polyominoes234(Polyominoes1234):

    piece_data = copy.deepcopy(Polyominoes1234.piece_data)
    del piece_data['O1']
    symmetric_pieces = Polyominoes1234.symmetric_pieces[1:]
    piece_colors = copy.deepcopy(Polyominoes1234.piece_colors)
    del piece_colors['O1']


class Polyominoes12345(Polyominoes1234):

    piece_data = copy.deepcopy(Polyominoes1234.piece_data)
    piece_data.update(copy.deepcopy(Pentominoes.piece_data))
    symmetric_pieces = (
        Polyominoes1234.symmetric_pieces + Pentominoes.symmetric_pieces)
    asymmetric_pieces = (
        Polyominoes1234.asymmetric_pieces + Pentominoes.asymmetric_pieces)
    piece_colors = copy.deepcopy(Polyominoes1234.piece_colors)
    piece_colors.update(Pentominoes.piece_colors)


class OneSidedPolyominoes12345(OneSidedLowercaseMixin, Polyominoes12345):

    pass


class Polyominoes2345(Polyominoes12345):

    piece_data = copy.deepcopy(Polyominoes12345.piece_data)
    del piece_data['O1']
    symmetric_pieces = Polyominoes12345.symmetric_pieces[1:]
    piece_colors = copy.deepcopy(Polyominoes12345.piece_colors)
    del piece_colors['O1']


class Polyominoes45(Polyominoes):

    piece_data = copy.deepcopy(Tetrominoes.piece_data)
    piece_data.update(copy.deepcopy(Pentominoes.piece_data))
    symmetric_pieces = (
        Tetrominoes.symmetric_pieces + Pentominoes.symmetric_pieces)
    asymmetric_pieces = (
        Tetrominoes.asymmetric_pieces + Pentominoes.asymmetric_pieces)
    piece_colors = copy.deepcopy(Tetrominoes.piece_colors)
    piece_colors.update(Pentominoes.piece_colors)
