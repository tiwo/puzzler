#!/usr/bin/env python
# $Id$

"""
Concrete Soma cube puzzles.
"""

from puzzler.puzzles import Puzzle3D
from puzzler.puzzles.polycubes import SomaCubes


class Soma3x3x3(SomaCubes):

    """
    240 solutions
    symmetry: T fixed (at edge, in XY plane, leg at right);
    restrict p to 4 aspects (one leg down)
    """

    height = 3
    width = 3
    depth = 3

    def customize_piece_data(self):
        self.piece_data['T'][-1]['flips'] = None
        self.piece_data['T'][-1]['axes'] = None
        self.piece_data['T'][-1]['rotations'] = None
        self.piece_data['p'][-1]['flips'] = None
        self.piece_data['p'][-1]['axes'] = (1,)

    def build_matrix(self):
        keys = sorted(self.pieces.keys())
        assert len(self.pieces['T']) == 1
        t_coords, t_aspect = self.pieces['T'][0]
        self.build_matrix_row('T', t_aspect)
        keys.remove('T')
        self.build_regular_matrix(keys)


class SomaCrystal(SomaCubes):

    """2800 solutions."""

    height = 3
    width = 3
    depth = 5

    # no duplicate_conditions, due to chiral nature of a & b

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if x + y <= z:
                        yield (x, y, z)

    def transform_solution_matrix(self, s_matrix):
        return [[[s_matrix[z][y][x]
                  for y in range(self.height)]
                 for z in range(self.depth - 1, -1, -1)]
                for x in range(self.width)]


class SomaLongWall(SomaCubes):

    """104 solutions."""

    height = 6
    width = 6
    depth = 2

    # no duplicate_conditions, due to chiral nature of a & b

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if 4 <= x + y <= 6 - z:
                        yield (x, y, z)

    transform_solution_matrix = Puzzle3D.cycle_xyz_transform


class SomaHighWall(SomaCubes):

    """46 solutions."""

    height = 5
    width = 5
    depth = 3

    check_for_duplicates = True
    duplicate_conditions = ({'z_reversed': True, 'xy_swapped': True},)

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if 3 <= x + y <= 4:
                        yield (x, y, z)

    transform_solution_matrix = Puzzle3D.cycle_xyz_transform


class SomaBench(SomaCubes):

    """0 solutions."""

    height = 2
    width = 9
    depth = 2

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if y + z < 2:
                        yield (x, y, z)


class SomaSteps(SomaCubes):

    """164 solutions."""

    height = 3
    width = 5
    depth = 3

    check_for_duplicates = True
    duplicate_conditions = ({'x_reversed': True, 'y_reversed': True},)

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if z <= x <= 4 - z:
                        yield (x, y, z)

    transform_solution_matrix = Puzzle3D.swap_yz_transform


class SomaBathtub(SomaCubes):

    """158 solutions."""

    height = 3
    width = 5
    depth = 2

    check_for_duplicates = True
    duplicate_conditions = ({'x_reversed': True, 'y_reversed': True},)

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if z != 1 or x == 0 or x == 4 or y == 0 or y == 2:
                        yield (x, y, z)


class SomaCurvedWall(SomaCubes):

    """66 solutions."""

    height = 3
    width = 5
    depth = 3

    check_for_duplicates = True
    duplicate_conditions = ({'x_reversed': True, 'z_reversed': True},)

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if   ((y == 2 and (1 <= x <= 3))
                          or (y == 1 and x != 2)
                          or (y == 0 and (x == 0 or x == 4))):
                        yield (x, y, z)

    def transform_solution_matrix(self, s_matrix):
        return [[[s_matrix[z][y][x] for x in range(self.width)]
                 for z in range(self.depth)]
                for y in range(self.height - 1, -1, -1)]


class SomaSquareWall(SomaCubes):

    """0 solutions."""

    height = 3
    width = 5
    depth = 3

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if y == 2 or x == 0 or x == 4:
                        yield (x, y, z)


class SomaSofa(SomaCubes):

    """32 solutions."""

    height = 3
    width = 5
    depth = 3

    check_for_duplicates = True
    duplicate_conditions = ({'yz_swapped': True, 'x_reversed': True},)

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if z == 0 or y == 0 or ((x == 0 or x == 4) and z == y == 1):
                        yield (x, y, z)


class SomaCornerstone(SomaCubes):

    """10 solutions."""

    height = 5
    width = 5
    depth = 5

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if   ((z == 0 and x + y <= 4)
                          or (x == 0 and z + y <= 4)
                          or (z == x == 1 and y <= 1)):
                        yield (x, y, z)


class Soma_W(SomaCubes):

    """0 solutions."""

    height = 5
    width = 5
    depth = 3

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if   ((x == 0 or x == 2 or y == 0 or y == 2)
                          and (2 <= x + y <= 4)):
                        yield (x, y, z)


class SomaSkew1(SomaCubes):

    """244 solutions."""

    height = 3
    width = 5
    depth = 3

    check_for_duplicates = True
    duplicate_conditions = ({'x_reversed': True, 'y_reversed': True},)

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if 2 <= x + y <= 4:
                        yield (x, y, z)

    transform_solution_matrix = Puzzle3D.swap_yz_transform


class SomaSkew2(SomaCubes):

    """14 solutions."""

    height = 3
    width = 7
    depth = 3

    check_for_duplicates = True
    duplicate_conditions = ({'x_reversed': True, 'y_reversed': True},)

    def coordinates(self):
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    if 4 <= x + 2 * y <= 6:
                        yield (x, y, z)

    transform_solution_matrix = Puzzle3D.swap_yz_transform


class SomaSteamer(SomaCubes):

    """152 solutions."""

    height = 5
    width = 5
    depth = 3

    check_for_duplicates = True
    duplicate_conditions = ({'x_reversed': True, 'y_reversed': True},)

    def coordinates(self):
        for z in range(self.depth):
            for y in range(z, self.height - z):
                for x in range(z, self.width - z):
                    if 2 + 2 * z <= x + y + z <= 6:
                        yield (x, y, z)

    transform_solution_matrix = Puzzle3D.cycle_xyz_transform


class SomaTunnel(SomaCubes):

    """26 solutions."""

    height = 3
    width = 5
    depth = 3

    check_for_duplicates = True
    duplicate_conditions = ({'x_reversed': True, 'z_reversed': True},)

    def coordinates(self):
        for (x, y) in ((0,0), (1,0), (1,1), (1,2), (2,2),
                       (3,2), (3,1), (3,0), (4,0)):
            for z in range(self.depth):
                yield (x, y, z)


class SomaScrew(SomaCubes):

    """14 solutions."""

    height = 5
    width = 3
    depth = 3

    def coordinates(self):
        holes = set(((0,0,1), (0,0,2), (1,0,2), (1,1,2), (2,1,2), (2,1,1),
                     (2,2,1), (2,2,0), (1,2,0), (1,3,0), (0,3,0), (0,3,1)))
        top = ((2,4,2), (2,4,1), (1,4,1))
        for z in range(self.depth):
            for y in range(self.height - 1):
                for x in range(self.width):
                    if (x,y,z) not in holes:
                        yield (x, y, z)
        for (x,y,z) in top:
            yield (x, y, z)


class SomaClip(SomaCubes):

    """20 solutions."""

    height = 4
    width = 4
    depth = 3

    check_for_duplicates = True
    duplicate_conditions = ({'z_reversed': True, 'xy_swapped': True},)

    def coordinates(self):
        for x in range(self.width):
            for y in range(self.height):
                if   ((y == 0) or (x == 0)
                      or (x == 3 and y == 1) or (y == 3 and x == 1)):
                    for z in range(self.depth):
                        yield (x, y, z)

    transform_solution_matrix = Puzzle3D.cycle_xyz_transform
