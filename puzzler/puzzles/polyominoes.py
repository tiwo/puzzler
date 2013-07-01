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

    # for format_solution:
    piece_width = 3

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

    # for format_solution:
    piece_width = 2


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


class Hexominoes(Polyominoes):

    piece_data = {
        'A06': ((( 0,1), ( 0,2), (1, 1), (1,2), (2,2)), {}),
        'C06': ((( 0,1), ( 0,2), (0, 3), (1,0), (1,3)), {}),
        'D06': ((( 0,1), ( 0,2), (0, 3), (1,1), (1,2)), {}),
        'E06': (((-1,1), ( 0,1), (0, 2), (1,0), (1,2)), {}),
        'F06': (((-1,2), ( 0,1), (0, 2), (0,3), (1,3)), {}), # hi F
        'F16': (((-1,1), ( 0,1), (0, 2), (0,3), (1,3)), {}), # low F
        'F26': (((-2,1), (-1,1), (0, 1), (0,2), (1,2)), {}), # hi 4
        'F36': (((-1,1), ( 0,1), (0, 2), (1,2), (2,2)), {}), # low 4
        'G06': ((( 0,1), ( 0,2), (1,-1), (1,0), (1,2)), {}),
        'H06': ((( 0,1), ( 0,2), (1, 1), (2,0), (2,1)), {}),
        'I06': ((( 0,1), ( 0,2), (0, 3), (0,4), (0,5)), {}),
        'J06': ((( 0,1), ( 1,0), (2, 0), (2,1), (2,2)), {}),
        'K06': ((( 0,1), ( 1,0), (1, 1), (1,2), (2,1)), {}),
        'L06': ((( 0,1), ( 0,2), (0, 3), (0,4), (1,0)), {}),
        'M06': ((( 0,1), ( 1,1), (2, 1), (2,2), (3,2)), {}),
        'N06': ((( 0,1), ( 0,2), (1, 1), (1,2), (1,3)), {}), # short N
        'N16': ((( 0,1), ( 0,2), (0, 3), (1,3), (1,4)), {}), # long N
        'O06': ((( 0,1), ( 0,2), (1, 0), (1,1), (1,2)), {}),
        'P06': ((( 0,1), ( 0,2), (0, 3), (1,2), (1,3)), {}),
        'Q06': (((-1,1), (-1,2), (0, 1), (0,2), (1,0)), {}),
        'R06': ((( 0,1), ( 0,2), (1, 1), (1,2), (2,1)), {}),
        'S06': (((-1,2), (-1,3), (-1,4), (0,1), (0,2)), {}), # long S
        'T06': (((-1,3), ( 0,1), (0, 2), (0,3), (1,3)), {}), # long T
        'T16': (((-1,2), ( 0,1), (0, 2), (1,2), (2,2)), {}), # short T
        'U06': ((( 0,1), ( 1,0), (2, 0), (2,1), (3,0)), {}),
        'V06': ((( 1,0), ( 2,0), (2, 1), (2,2), (2,3)), {}),
        'W06': ((( 1,0), ( 1,1), (2, 1), (2,2), (2,3)), {}), # Wa
        'W16': ((( 1,0), ( 1,1), (2, 1), (2,2), (3,2)), {}), # Wb
        'W26': ((( 1,0), ( 1,1), (2, 1), (2,2), (3,1)), {}), # Wc
        'X06': (((-1,1), ( 0,1), (0, 2), (0,3), (1,1)), {}),
        'X16': (((-1,1), ( 0,1), (0, 2), (0,3), (1,2)), {}), # italic X
        'Y06': (((-1,3), ( 0,1), (0, 2), (0,3), (0,4)), {}), # hi Y
        'Y16': (((-1,2), ( 0,1), (0, 2), (0,3), (0,4)), {}), # low Y
        'Z06': (((-1,3), ( 0,1), (0, 2), (0,3), (1,0)), {}), # long Z
        'Z16': (((-1,2), ( 0,1), (0, 2), (1,0), (2,0)), {}), # short Z
        }
    """(0,0) is implied."""

    symmetric_pieces = 'A06 C06 D06 E06 I06 K06 O06 T06 X06 Y16'.split()
    """Pieces with reflexive symmetry, identical to their mirror images."""

    asymmetric_pieces = (
        'F06 F16 F26 F36 G06 H06 J06 L06 M06 N06 N16 P06 Q06 R06 S06 T16 '
        'U06 V06 W06 W16 W26 X16 Y06 Z06 Z16').split()
    """Pieces without reflexive symmetry, different from their mirror images."""

    piece_colors = {
        'A06': 'blue',
        'C06': 'red',
        'D06': 'green',
        'E06': 'lime',
        'F06': 'navy',
        'F16': 'magenta',
        'F26': 'darkorange',
        'F36': 'turquoise',
        'G06': 'blueviolet',
        'H06': 'maroon',
        'I06': 'gold',
        'J06': 'plum',
        'K06': 'blue',
        'L06': 'red',
        'M06': 'green',
        'N06': 'lime',
        'N16': 'navy',
        'O06': 'magenta',
        'P06': 'darkorange',
        'Q06': 'turquoise',
        'R06': 'blueviolet',
        'S06': 'maroon',
        'T06': 'gold',
        'T16': 'plum',
        'U06': 'blue',
        'V06': 'red',
        'W06': 'green',
        'W16': 'lime',
        'W26': 'navy',
        'X06': 'magenta',
        'X16': 'darkorange',
        'Y06': 'turquoise',
        'Y16': 'blueviolet',
        'Z06': 'maroon',
        'Z16': 'gold',
        '0': 'gray',
        '1': 'black'}

    # for format_solution:
    piece_width = 4


class OneSidedHexominoes(OneSidedLowercaseMixin, Hexominoes):

    pass


class HexominoesPlus(Hexominoes):

    """
    Also known as Kadon's 'Sextillions', these are the hexominoes with a
    second N06 piece (a.k.a. S16), total 36 pieces, allowing the construction
    of rectangles.  See http://gamepuzzles.com/polycub2.htm#SX.
    """

    piece_data = copy.deepcopy(Hexominoes.piece_data)
    piece_data['S16'] = copy.deepcopy(piece_data['N06'])
    piece_colors = copy.deepcopy(Hexominoes.piece_colors)
    piece_colors['S16'] = piece_colors['N06']
    asymmetric_pieces = Hexominoes.asymmetric_pieces + ['S16']

    def format_solution(self, solution, normalized=True,
                        x_reversed=False, y_reversed=False):
        """
        Consider N06 and S16 as the same piece for solution counting purposes.
        """
        formatted = Hexominoes.format_solution(
            self, solution, normalized, x_reversed=x_reversed,
            y_reversed=y_reversed)
        if normalized:
            return formatted.replace('S16', 'N06')
        else:
            return formatted


class Cornucopia(Hexominoes):

    """
    From the set of hexominoes,

        eliminate all pieces having reflexive or rotational symmetry and all
        those containing a 2 x 2 square because they are less desirable for
        various reasons already explained. The remaining 17 pieces are the set
        of Cornucopia pieces.

        -- `The Puzzling World of Polyhedral Dissections, by Stewart T. Coffin
           <http://www.johnrausch.com/PuzzlingWorld/chap02.htm#p6>`__
    """

    asymmetric_pieces = (
        'G06 H06 L06 N16 T16 U06 V06 W06 W26 Y06 Z16 F06 F16 F26 F36 J06 M06'
        .split())
    symmetric_pieces = []
    piece_colors = copy.deepcopy(Hexominoes.piece_colors)

Cornucopia.piece_data = dict(
    (_name, _value) for (_name, _value) in Hexominoes.piece_data.items()
    if _name in Cornucopia.asymmetric_pieces)
del _name, _value


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


class OneSidedPolyominoes234(OneSidedLowercaseMixin, Polyominoes234):

    pass


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


class OneSidedPolyominoes2345(OneSidedLowercaseMixin, Polyominoes2345):

    pass


class Polyominoes45(Polyominoes):

    piece_data = copy.deepcopy(Tetrominoes.piece_data)
    piece_data.update(copy.deepcopy(Pentominoes.piece_data))
    symmetric_pieces = (
        Tetrominoes.symmetric_pieces + Pentominoes.symmetric_pieces)
    asymmetric_pieces = (
        Tetrominoes.asymmetric_pieces + Pentominoes.asymmetric_pieces)
    piece_colors = copy.deepcopy(Tetrominoes.piece_colors)
    piece_colors.update(Pentominoes.piece_colors)


class OneSidedPolyominoes45(OneSidedLowercaseMixin, Polyominoes45):

    pass


class Polyominoes123456(Polyominoes12345):

    piece_data = copy.deepcopy(Polyominoes12345.piece_data)
    piece_data.update(copy.deepcopy(Hexominoes.piece_data))
    symmetric_pieces = (
        Polyominoes12345.symmetric_pieces + Hexominoes.symmetric_pieces)
    asymmetric_pieces = (
        Polyominoes12345.asymmetric_pieces + Hexominoes.asymmetric_pieces)
    piece_colors = copy.deepcopy(Polyominoes12345.piece_colors)
    piece_colors.update(Hexominoes.piece_colors)

    # for format_solution:
    piece_width = 4


class OneSidedPolyominoes123456(OneSidedLowercaseMixin, Polyominoes123456):

    pass
