#!/usr/bin/env python
# $Id$

"""
Concrete hexiamonds puzzles.
"""

from puzzler.puzzles.polyiamonds import Hexiamonds, OneSidedHexiamonds


class Hexiamonds3x12(Hexiamonds):

    """0 solutions"""

    height = 3
    width = 12

    duplicate_conditions = ({'rotate_180': True},)


class Hexiamonds4x9(Hexiamonds):

    """74 solutions"""

    height = 4
    width = 9

    duplicate_conditions = ({'rotate_180': True},)


class Hexiamonds6x6(Hexiamonds):

    """156 solutions"""

    height = 6
    width = 6

    duplicate_conditions = ({'rotate_180': True},
                            {'xy_swapped': True},
                            {'rotate_180': True, 'xy_swapped': True},)


class Hexiamonds4x11Trapezium(Hexiamonds):

    """76 solutions"""

    height = 4
    width = 11

    check_for_duplicates = False

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if x + y + z < self.width:
                        yield (x, y, z)

    def customize_piece_data(self):
        self.piece_data['I6'][-1]['flips'] = None


class Hexiamonds6x9Trapezium(Hexiamonds4x11Trapezium):

    """0 solutions (impossible due to parity)"""

    height = 6
    width = 9


class Hexiamonds4x10LongHexagon(Hexiamonds):

    """856 solutions"""

    height = 4
    width = 10

    duplicate_conditions = ({'rotate_180': True},)

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if 1 < x + y + z <= self.width + 1:
                        yield (x, y, z)

    def customize_piece_data(self):
        self.piece_data['I6'][-1]['flips'] = None


class Hexiamonds5x8StackedLongHexagons(Hexiamonds):

    """378 solutions"""

    height = 8
    width = 8

    duplicate_conditions = ({'rotate_180': True},)

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if 7 <= (2 * x + y + z) <= 15:
                        yield (x, y, z)

    def customize_piece_data(self):
        self.piece_data['I6'][-1]['flips'] = None


class Hexiamonds4x12StackedHexagons(Hexiamonds):

    """51 solutions"""

    height = 12
    width = 8

    duplicate_conditions = ({'rotate_180': True},)

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    total = x + y + z
                    if (  (y < 4 and 4 <= x < 8 and 6 <= total < 10)
                          or (4 <= y < 8 and 2 <= x < 6 and 8 <= total < 12)
                          or (8 <= y and x < 4 and 10 <= total < 14)):
                        yield (x, y, z)

    def customize_piece_data(self):
        self.piece_data['I6'][-1]['flips'] = None


class Hexiamonds4x10LongButterfly(Hexiamonds):

    """0 solutions"""

    height = 4
    width = 12

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    total = x + y + z
                    if (  (total > 3 or x > 1)
                          and (total < self.width or x < 10)):
                        yield (x, y, z)


class Hexiamonds5x8StackedLongButterflies(Hexiamonds):

    """290 solutions"""

    height = 8
    width = 9

    duplicate_conditions = ({'rotate_180': True},)

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if 8 <= (2 * x + y + z) <= 16:
                        yield (x, y, z)

    def customize_piece_data(self):
        self.piece_data['I6'][-1]['flips'] = None


class Hexiamonds4x12StackedButterflies(Hexiamonds):

    """26 solutions"""

    height = 12
    width = 10

    duplicate_conditions = ({'rotate_180': True},)

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    total = x + y + z
                    if (  (y < 2 and 6 <= x and total < 10)
                          or (2 <= y < 6 and 4 <= x < 8 and 8 <= total < 12)
                          or (6 <= y < 10 and 2 <= x < 6 and 10 <= total < 14)
                          or (10 <= y and x < 4 and 12 <= total)):
                        yield (x, y, z)

    def customize_piece_data(self):
        self.piece_data['I6'][-1]['flips'] = None


class HexiamondsSnowflake(Hexiamonds):

    """55 solutions"""

    height = 8
    width = 8

    check_for_duplicates = False

    def coordinates(self):
        exceptions = ((0,3,1), (0,4,0), (0,4,1), (0,5,0), (0,7,0), (0,7,1),
                      (1,7,0), (1,7,1), (2,1,1), (3,0,1), (3,1,0), (3,7,1),
                      (4,0,0), (4,6,1), (4,7,0), (5,6,0), (6,0,0), (6,0,1),
                      (7,0,0), (7,0,1), (7,2,1), (7,3,0), (7,3,1), (7,4,0))
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if ( 3 < x + y + z < self.width + self.height - 4
                         and (x, y, z) not in exceptions):
                        yield (x, y, z)

    def customize_piece_data(self):
        self.piece_data['J6'][-1]['rotations'] = None


class HexiamondsRing(Hexiamonds):

    """
    0 solutions

    8-unit high hexagon with a central 4-unit hexagonal hole.
    """

    height = 8
    width = 8

    check_for_duplicates = False

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if ( 3 < x + y + z < 12
                         and not (1 < x < 6 and 1 < y < 6
                                  and 5 < x + y + z < 10)):
                        yield (x, y, z)


class HexiamondsRing2(Hexiamonds):

    """
    11 solutions

    8-unit high hexagon with a 4-unit hexagonal hole offset one unit from the
    center.
    """

    height = 8
    width = 8

    check_for_duplicates = False

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if ( 3 < x + y + z < 12
                         and not (2 < x < 7 and 1 < y < 6
                                  and 6 < x + y + z < 11)):
                        yield (x, y, z)

    def customize_piece_data(self):
        self.piece_data['I6'][-1]['flips'] = None


class HexiamondsHexagon3(Hexiamonds):

    """0 solutions"""

    height = 8
    width = 8

    def coordinates(self):
        hole = set()
        for z in range(self.depth):
            for y in range(2, 6):
                for x in range(2, 6):
                    if 5 < x + y + z < 10:
                        hole.add((x,y,z))
        for coord in ((1,5,1), (2,3,0), (4,1,1), (6,2,0), (5,4,1), (3,6,0)):
            hole.add(coord)
        for coord in ((2,4,0), (3,2,1), (5,2,0), (5,3,1), (4,5,0), (2,5,1)):
            hole.remove(coord)
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if 3 < x + y + z < 12 and (x,y,z) not in hole:
                        yield (x, y, z)


class HexiamondsHexagon4(Hexiamonds):

    """0 solutions"""

    height = 8
    width = 8

    def coordinates(self):
        hole = set()
        for z in range(self.depth):
            for y in range(2):
                for x in range(2):
                    for bx,by in ((1,4), (3,3), (4,1), (4,4)):
                        if 0 < x + y + z < 3:
                            hole.add((x + bx, y + by, z))
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if 3 < x + y + z < 12 and (x,y,z) not in hole:
                        yield (x, y, z)


class HexiamondsHexagon5(Hexiamonds):

    """0 solutions"""

    height = 8
    width = 8

    def coordinates(self):
        hole = set()
        for z in range(self.depth):
            for y in range(2, 6):
                for x in range(2, 6):
                    if 5 < x + y + z < 10:
                        hole.add((x,y,z))
        for coord in ((1,4,1), (1,5,0), (4,5,1), (5,5,0), (5,1,0), (5,1,1)):
            hole.add(coord)
        for coord in ((2,5,0), (2,5,1), (5,3,1), (5,4,0), (3,2,1), (4,2,0)):
            hole.remove(coord)
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if 3 < x + y + z < 12 and (x,y,z) not in hole:
                        yield (x, y, z)


class HexiamondsHexagon6(Hexiamonds):

    """0 solutions"""

    height = 8
    width = 8

    def coordinates(self):
        hole = set()
        for z in range(self.depth):
            for y in range(2, 6):
                for x in range(2, 6):
                    if 5 < x + y + z < 10:
                        hole.add((x,y,z))
        for coord in ((1,4,1), (2,3,0), (4,5,1), (3,6,0), (5,1,1), (6,2,0)):
            hole.add(coord)
        for coord in ((2,5,0), (2,5,1), (5,3,1), (5,4,0), (3,2,1), (4,2,0)):
            hole.remove(coord)
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if 3 < x + y + z < 12 and (x,y,z) not in hole:
                        yield (x, y, z)


class HexiamondsCrescent(Hexiamonds):

    """
    87 solutions

    8-unit high hexagon with a 4-unit hexagonal bite removed from one corner.
    """

    height = 8
    width = 8

    check_for_duplicates = False

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if ( 3 < x + y + z < 12
                         and not (x > 3 and 1 < y < 6 and 7 < x + y + z)):
                        yield (x, y, z)

    def customize_piece_data(self):
        self.piece_data['I6'][-1]['flips'] = None


class HexiamondsCrescent2(Hexiamonds):

    """
    2 solutions

    8-unit high hexagon with a 4-unit hexagonal bite removed from one side.
    """

    height = 8
    width = 8

    check_for_duplicates = False

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if ( 3 < x + y + z < 12
                         and not (2 < x < 7 and 2 < y < 7 and 7 < x + y + z)):
                        yield (x, y, z)

    def customize_piece_data(self):
        self.piece_data['I6'][-1]['flips'] = None


class HexiamondsTrefoil(Hexiamonds):

    """640 solutions"""

    height = 8
    width = 8

    check_for_duplicates = False

    def coordinates(self):
        for z in range(self.depth):
            for y in range(2, 6):
                for x in range(4):
                    if 3 < x + y + z <= 7:
                        yield (x, y, z)
            for y in range(4):
                for x in range(4, 8):
                    if 5 < x + y + z <= 9:
                        yield (x, y, z)
            for y in range(4, 8):
                for x in range(2, 6):
                    if 7 < x + y + z <= 11:
                        yield (x, y, z)

    def customize_piece_data(self):
        self.piece_data['I6'][-1]['rotations'] = None
        self.piece_data['I6'][-1]['flips'] = None


class Hexiamonds3Hexagons(Hexiamonds):

    """0 solutions"""

    height = 4
    width = 12

    check_for_duplicates = False

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(4):
                    if 1 < x + y + z <= 5:
                        yield (x, y, z)
                for x in range(4, 8):
                    if 5 < x + y + z <= 9:
                        yield (x, y, z)
                for x in range(8, 12):
                    if 9 < x + y + z <= 13:
                        yield (x, y, z)


class HexiamondsCoin(Hexiamonds):

    """304 solutions"""

    height = 6
    width = 8

    duplicate_conditions = ({'rotate_180': True},)

    def coordinates(self):
        hole = set(((3,2,1), (3,3,0), (3,3,1), (4,2,0), (4,2,1), (4,3,0)))
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if ( 2 < x + y + z <= 10
                         and not (x, y, z) in hole):
                        yield (x, y, z)

    def customize_piece_data(self):
        self.piece_data['I6'][-1]['flips'] = None


class HexiamondsIrregularHexagon7x8(Hexiamonds):

    """
    5885 solutions.

    Suggested by Dan Klarskov, Denmark, under the name 'hexui'.
    """

    height = 8
    width = 7

    check_for_duplicates = False

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if 1 < x + y + z < 9:
                        yield (x, y, z)

    def customize_piece_data(self):
        self.piece_data['I6'][-1]['flips'] = None


class HexiamondsStackedChevrons_6x6(Hexiamonds):

    """
    933 solutions.

    Suggested by Dan Klarskov, Denmark, under the name 'polyam2'.
    """

    height = 6
    width = 9

    check_for_duplicates = False

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if self.height <= (2 * x + y + z) < (self.width * 2):
                        yield (x, y, z)

    def customize_piece_data(self):
        self.piece_data['I6'][-1]['flips'] = None


class HexiamondsStackedChevrons_12x3_1(Hexiamonds):

    """269 solutions."""

    height = 12
    width = 9

    check_for_duplicates = False

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if 11 <= (2 * x + y + z) < 17:
                        yield (x, y, z)

    def customize_piece_data(self):
        self.piece_data['I6'][-1]['flips'] = None


class HexiamondsStackedChevrons_12x3_2(Hexiamonds):

    """114 solutions."""

    height = 12
    width = 9

    check_for_duplicates = False

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    total = x + y + z
                    if (  (y < 2 and 6 <= total < 9)
                          or (2 <= y < 4 and 4 <= x < 7)
                          or (4 <= y < 6 and 8 <= total < 11)
                          or (6 <= y < 8 and 2 <= x < 5)
                          or (8 <= y < 10 and 10 <= total < 13)
                          or (y >= 10 and x < 3)):
                        yield (x, y, z)

    def customize_piece_data(self):
        self.piece_data['I6'][-1]['flips'] = None


class HexiamondsStackedChevrons_12x3_3(Hexiamonds):

    """46 solutions."""

    height = 12
    width = 9

    check_for_duplicates = False

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    total = x + y + z
                    if (  (y < 3 and 6 <= total < 9)
                          or (3 <= y < 6 and 3 <= x < 6)
                          or (6 <= y < 9 and 9 <= total < 12)
                          or (y >= 9 and x < 3)):
                        yield (x, y, z)

    def customize_piece_data(self):
        self.piece_data['I6'][-1]['flips'] = None


class HexiamondsChevron(Hexiamonds):

    """
    Left-facing chevron.

    Width of solution space is (apparent width) + (height / 2).
    """

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if y >= self.height / 2:
                        if x < (self.width - self.height / 2):
                            # top half
                            yield (x, y, z)
                    elif (self.height / 2 - 1) < (x + y + z) < self.width:
                        # bottom half
                        yield (x, y, z)

    def customize_piece_data(self):
        self.piece_data['I6'][-1]['flips'] = None


class HexiamondsChevron_4x9(HexiamondsChevron):

    """142 solutions."""

    height = 4
    width = 11

    check_for_duplicates = False


class HexiamondsChevron_6x6(HexiamondsChevron):

    """1004 solutions."""

    height = 6
    width = 9

    check_for_duplicates = False


class HexiamondsChevron_12x3(HexiamondsChevron):

    """29 solutions."""

    height = 12
    width = 9

    check_for_duplicates = False


class HexiamondsV_9x9(Hexiamonds):

    """0 solutions"""

    height = 9
    width = 9

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    total = x + y + z
                    if (  self.width <= total
                          and not (y > 5 and x < 6 and total > 11)):
                        yield (x, y, z)


class HexiamondsTenyo(Hexiamonds):

    """
     solutions.

    This is the puzzle that is sold by Tenyo Inc., Japan, in their `"PlaPuzzle"
    line`__ (`details`__).

    __ http://www.tenyo.co.jp/pp/
    __ http://www.tenyo.co.jp/pp/pz04/index.html
    """

    height = 8
    width = 7

    check_for_duplicates = False

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    xyz = x + y + z
                    if (  ((xyz > 4) or (x > 0 and xyz > 3))
                          and ((xyz < 9) or (x < 6 and xyz < 10)
                               or (x < 5 and xyz < 11))):
                        yield (x, y, z)

    def customize_piece_data(self):
        self.piece_data['I6'][-1]['flips'] = None


class OneSidedHexiamondsOBeirnesHexagon(OneSidedHexiamonds):

    """
    124,519 solutions, agrees with Knuth.

    Split into 7 sub-puzzles by the distance of the small-hexagon piece (O6)
    from the center of the puzzle.

    O'Beirne's Hexagon consists of 19 small 6-triangle hexagons, arranged in a
    hexagon like a honeycomb (12 small hexagons around 6 around 1).
    """

    height = 10
    width = 10

    duplicate_conditions = ({'standardize': 'P6'},
                            {'standardize': 'p6'},)

    @classmethod
    def components(cls):
        return (OneSidedHexiamondsOBeirnesHexagon_A,
                OneSidedHexiamondsOBeirnesHexagon_B,
                OneSidedHexiamondsOBeirnesHexagon_C,
                OneSidedHexiamondsOBeirnesHexagon_D,
                OneSidedHexiamondsOBeirnesHexagon_E,
                OneSidedHexiamondsOBeirnesHexagon_F,
                OneSidedHexiamondsOBeirnesHexagon_G,)

    def coordinates(self):
        bumps = set((
            (0,6,1), (0,7,0), (0,7,1), (9,2,0), (9,2,1), (9,3,0),
            (6,0,1), (7,0,0), (7,0,1), (2,9,0), (2,9,1), (3,9,0),
            (2,3,0), (2,2,1), (3,2,0), (6,7,1), (7,7,0), (7,6,1)))
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if (  (5 < (x + y + z) < 14) and (0 < x < 9) and (0 < y < 9)
                          or (x,y,z) in bumps):
                        yield (x, y, z)

    def build_matrix(self):
        """"""
        keys = sorted(self.pieces.keys())
        o_coords, o_aspect = self.pieces['O6'][0]
        for coords in self.O6_offsets:
            translated = o_aspect.translate(coords)
            self.build_matrix_row('O6', translated)
        keys.remove('O6')
        self.build_regular_matrix(keys)


class OneSidedHexiamondsOBeirnesHexagon_A(OneSidedHexiamondsOBeirnesHexagon):

    """1914 solutions."""

    O6_offsets = ((4,4,0),)

    def customize_piece_data(self):
        OneSidedHexiamondsOBeirnesHexagon.customize_piece_data(self)
        # one sphinx pointing up, to eliminate duplicates & reduce searches:
        self.piece_data['P6'][-1]['rotations'] = None


class OneSidedHexiamondsOBeirnesHexagon_B(OneSidedHexiamondsOBeirnesHexagon):

    """5727 solutions."""

    O6_offsets = ((5,4,0),)


class OneSidedHexiamondsOBeirnesHexagon_C(OneSidedHexiamondsOBeirnesHexagon):

    """11447 solutions."""

    O6_offsets = ((3,6,0),)


class OneSidedHexiamondsOBeirnesHexagon_D(OneSidedHexiamondsOBeirnesHexagon):

    """7549 solutions."""

    O6_offsets = ((6,4,0),)


class OneSidedHexiamondsOBeirnesHexagon_E(OneSidedHexiamondsOBeirnesHexagon):

    """6675 solutions."""

    O6_offsets = ((3,7,0),)


class OneSidedHexiamondsOBeirnesHexagon_F(OneSidedHexiamondsOBeirnesHexagon):

    """15717 solutions."""

    O6_offsets = ((7,4,0),)


class OneSidedHexiamondsOBeirnesHexagon_G(OneSidedHexiamondsOBeirnesHexagon):

    """75490 solutions."""

    O6_offsets = ((2,8,0),)


class OneSidedHexiamonds_TestHexagon(OneSidedHexiamonds):

    """Used to test the 'standardize' duplicate condition."""

    height = 6
    width = 6

    _test_pieces = set(['I6', 'P6', 'J6', 'V6', 'C6', 'O6'])

    symmetric_pieces = 'V6 C6 O6'.split()
    """Pieces with reflexive symmetry, identical to their mirror images."""

    asymmetric_pieces = 'I6 P6 J6'.split()
    """Pieces without reflexive symmetry, different from their mirror images."""

    check_for_duplicates = True

    duplicate_conditions = ({'standardize': 'P6'},
                            {'standardize': 'p6'})

    @classmethod
    def components(cls):
        return (OneSidedHexiamonds_TestHexagon_A,
                OneSidedHexiamonds_TestHexagon_B)

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if 3 <= (x + y + z) < 9:
                        yield (x, y, z)

    def build_matrix(self):
        """"""
        keys = sorted(self.pieces.keys())
        o_coords, o_aspect = self.pieces['O6'][0]
        for coords in self.O6_offsets:
            translated = o_aspect.translate(coords)
            self.build_matrix_row('O6', translated)
        keys.remove('O6')
        self.build_regular_matrix(keys)

    def customize_piece_data(self):
        for key in self.piece_data.keys():
            if key not in self._test_pieces:
                del self.piece_data[key]
        OneSidedHexiamonds.customize_piece_data(self)


class OneSidedHexiamonds_TestHexagon_A(OneSidedHexiamonds_TestHexagon):

    O6_offsets = ((1,4,0), (2,4,0), (2,3,0),)


class OneSidedHexiamonds_TestHexagon_B(OneSidedHexiamonds_TestHexagon):

    O6_offsets = ((2,2,0),)

    def customize_piece_data(self):
        OneSidedHexiamonds_TestHexagon.customize_piece_data(self)
        # one sphinx pointing up, to eliminate duplicates & reduce searches:
        self.piece_data['P6'][-1]['rotations'] = None
#         ## doesn't work (omits valid solutions):
#         #self.piece_data['C6'][-1]['rotations'] = (0,2,4)


class OneSidedHexiamondsLongHexagon8x3(OneSidedHexiamonds):

    """Many solutions."""

    height = 6
    width = 11

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if 2 < x + y + z <= 13:
                        yield (x, y, z)


class OneSidedHexiamondsButterfly11x3(OneSidedHexiamonds):

    """Many solutions."""

    height = 6
    width = 14

    def coordinates(self):
        return self.coordinates_butterfly(11, 3)


class OneSidedHexiamonds19x3(OneSidedHexiamonds):

    """0 solutions."""

    height = 3
    width = 19
