#!/usr/bin/env python
# -*- coding: utf-8 -*-
# $Id$

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2012 by David J. Goodger
# License: GPL 2 (see __init__.py)

"""
Coordinates, coordinate sets, & views.
"""

import sys


class CoordinateSystem:

    """
    coordinate system services:
        vector addition & subtraction
        orientation coord transformations (rotation, flipping)
    coordinate space services:
        internal coordinate transformations (logical -> underlying storage)
        adjacency testing
        storage allocation
        assignment to & retrieval from storage
        size calculations (area/volume)
        subspace sets
    """

    def __init__(self, coords):
        self.coords = coords

    def __repr__(self):
        return repr(self.coords)

    def __len__(self):
        return len(self.coords)

    def __getitem__(self, index):
        return self.coords[index]

    def __getslice__(self, low, high):
        return self.coords[low:high]

    def __hash__(self):
        return hash(self.coords)

    def __add__(self, other):
        if not isinstance(other, tuple):
            other = other.coords
        return self.__class__(
            tuple(self.coords[i] + other[i] for i in range(len(self.coords))))

    def __neg__(self):
        return self.__class__(
            tuple(-self.coords[i] for i in range(len(self.coords))))

    def __sub__(self, other):
        if not isinstance(other, tuple):
            other = other.coords
        return self.__class__(
            tuple(self.coords[i] - other[i] for i in range(len(self.coords))))

    def __cmp__(self, other):
        if isinstance(other, tuple):
            return cmp(self.coords, other)
        else:
            return cmp(self.coords, other.coords)

    def add_modulo(self, other, moduli):
        if not isinstance(other, tuple):
            other = other.coords
        return self.__class__(
            tuple((self.coords[i] + other[i]) % (modulus or sys.maxint)
                  for i, modulus in enumerate(moduli)))


class CartesianCoordinates(CoordinateSystem):

    pass


class Cartesian1D(CartesianCoordinates):

    """1D coordinate system: (x)"""

    rotation_steps = None

    rotation_axes = None

    flippable = True

    def flip0(self):
        """Flip on last dimension, about origin"""
        return self.__class__(self.coords[:-1] + (-self.coords[-1],))

    def flip(self, pivot):
        """Flip about pivot"""
        temp = self - pivot
        return temp.flip0() + pivot


class Cartesian2D(Cartesian1D):

    """2D coordinate system: (x, y)"""

    rotation_steps = 4

    rotation_axes = None

    flippable = True

    def rotate0(self, quadrants):
        """Rotate about (0,0)"""
        x = self.coords[quadrants % 2] * (-2 * ((quadrants + 1) // 2 % 2) + 1)
        y = self.coords[(quadrants + 1) % 2] * (-2 * (quadrants // 2 % 2) + 1)
        return self.__class__((x, y))

    def rotate(self, quadrants, pivot):
        """Rotate about pivot"""
        temp = self - pivot
        return temp.rotate0(quadrants) + pivot

    def neighbors(self):
        """Return a list of adjacent cells."""
        x, y = self.coords
        # counterclockwise from right
        return (self.__class__((x + 1, y)),       # right
                self.__class__((x,     y + 1)),   # above
                self.__class__((x - 1, y)),       # left
                self.__class__((x,     y - 1)))   # below


class Cartesian3D(Cartesian2D):

    """3D coordinate system: (x, y, z)"""

    rotation_steps = 4

    rotation_axes = 3

    flippable = True

    def rotate0(self, quadrants, axis):
        """Rotate about (0,0,0); `axis` is 0/x, 1/y, 2/z."""
        rotated = Cartesian2D((self.coords[(axis + 1) % 3],
                               self.coords[(axis + 2) % 3])).rotate0(quadrants)
        result = (self.coords[axis],) + tuple(rotated)
        return self.__class__(result[-axis:] + result[:-axis])

    def rotate(self, quadrants, axis, pivot):
        """Rotate about pivot"""
        temp = self - pivot
        return temp.rotate0(quadrants, axis) + pivot

    def flip0(self, axis):
        """Flip axis (180 degree rotation), about 0"""
        return self.rotate0(2, (axis + 1) % 3)

    def flip(self, axis, pivot):
        """Flip axis (180 degree rotation about next axis) about pivot"""
        temp = self - pivot
        return temp.flip0(axis) + pivot

    def neighbors(self):
        """Return a list of adjacent cells."""
        x, y, z = self.coords
        return (self.__class__((x + 1, y,     z)),       # right
                self.__class__((x - 1, y,     z)),       # left
                self.__class__((x,     y + 1, z)),       # above
                self.__class__((x,     y - 1, z)),       # below
                self.__class__((x,     y,     z + 1)),   # in front
                self.__class__((x,     y,     z - 1)))   # behind


class CoordinateSet(set):

    """Generic set of coordinates."""

    def __init__(self, coord_list):
        converted = [self.coord_class(c) for c in coord_list]
        self.update(converted)

    def rotate0(self, *args):
        return self.__class__([coord.rotate0(*args) for coord in self])

    def rotate(self, *args):
        return self.__class__([coord.rotate(*args) for coord in self])

    def flip0(self, *args):
        return self.__class__([coord.flip0(*args) for coord in self])

    def flip(self, *args):
        return self.__class__([coord.flip(*args) for coord in self])

    def translate(self, offset, moduli=None):
        """Move coordSet by offset"""
        new = self.__class__(list(self))
        new._itranslate(offset, moduli)
        return new

    def _itranslate(self, offset, moduli=None):
        """Move coordSet by offset, in place"""
        if isinstance(offset, tuple):
            offset = self.coord_class(offset)
        if moduli:
            newset = [coord.add_modulo(offset, moduli) for coord in self]
        else:
            newset = [coord + offset for coord in self]
        self.clear()
        self.update(newset)


class Cartesian1DCoordSet(CoordinateSet):

    """1 dimensional unit-cell coordinate set"""

    coord_class = Cartesian1D


class Cartesian2DCoordSet(CoordinateSet):

    """2 dimensional square-cell coordinate set"""

    coord_class = Cartesian2D

    def orient2D(self, rotation=0, flip=0):
        """
        Transform (rotate, flip) the coordinate set according to parameters.
        """
        if not (rotation == 0 and flip == 0):
            newSet = []
            for c in self:
                if flip:
                    c = c.flip0()
                newSet.append(c.rotate0(rotation))
            self.clear()
            self.update(newSet)


class Cartesian3DCoordSet(CoordinateSet):

    """3 dimensional cube-cell coordinate set"""

    coord_class = Cartesian3D

    def orient3D(self, rotation=0, axis=0, flip=0):
        """
        Transform (rotate, flip) the coordinate set according to parameters.
        """
        if not (rotation == 0 and flip == 0):
            newSet = []
            for c in self:
                if flip:
                    c = c.flip0((axis + 1) % 3)
                newSet.append(c.rotate0(rotation, axis))
            self.clear()
            self.update(newSet)


class Cartesian2DView(Cartesian2DCoordSet):

    """
    2 dimensional (+,+)-quadrant square-cell coordinate set with bounds
    """

    def __init__(self, coord_list, rotation=0, flip=0, axis=None):
        Cartesian2DCoordSet.__init__(self, coord_list)
        # transform self under aspect:
        self.orient2D(rotation, flip)
        offset, self.bounds = self.calculate_offset_and_bounds()
        # move coordSet to top-left at (0,0)
        self._itranslate(-offset)

    def __hash__(self):
        return hash(tuple(sorted(self)))

    def calculate_offset_and_bounds(self):
        rowvals = [c[0] for c in self]
        colvals = [c[1] for c in self]
        offset = self.coord_class((min(rowvals), min(colvals)))
        maxvals = self.coord_class((max(rowvals), max(colvals)))
        bounds = maxvals - offset
        return offset, bounds


class Cartesian3DView(Cartesian3DCoordSet):

    """
    3 dimensional (+,+,+)-quadrant square-cell coordinate set with bounds
    """

    def __init__(self, coord_list, rotation=0, axis=0, flip=0):
        Cartesian3DCoordSet.__init__(self, coord_list)
        # transform self under aspect:
        self.orient3D(rotation, axis, flip)
        offset, self.bounds = self.calculate_offset_and_bounds()
        # move coordSet to top-left at (0,0,0)
        self._itranslate(-offset)

    def __hash__(self):
        return hash(tuple(sorted(self)))

    def calculate_offset_and_bounds(self):
        rows = [c[0] for c in self]
        cols = [c[1] for c in self]
        layers = [c[2] for c in self]
        offset = self.coord_class((min(rows), min(cols), min(layers)))
        maxvals = self.coord_class((max(rows), max(cols), max(layers)))
        bounds = maxvals - offset
        return offset, bounds


class CartesianPseudo3DView(Cartesian3DView):

    """The Z dimension is used for direction/orientation."""

    def calculate_offset_and_bounds(self):
        rows = [c[0] for c in self]
        cols = [c[1] for c in self]
        layers = [c[2] for c in self]
        # keep Z-offset at 0 to keep Z values unaltered:
        offset = self.coord_class((min(rows), min(cols), 0))
        maxvals = self.coord_class((max(rows), max(cols), max(layers)))
        bounds = maxvals - offset
        return offset, bounds


class SquareGrid3D(Cartesian3D):

    """
    Pseudo-3D (2D + orientation) square coordinate system for gridlines: (x,
    y, z).  The Z dimension is for orientation: z==0 for horizontal line
    segments (from (x,y) to (x+1,y)), and z==1 for vertical line segments
    (from (x,y) to (x,y+1)).  The Z value indicates the index of the dimension
    to increment.
    """

    rotation_steps = 4

    rotation_axes = None

    flippable = True

    def flip0(self, axis=None):
        """
        Flip about y-axis::

            x_new = -x + z - 1
            y_new = y
            z_new = z

        The `axis` parameter is ignored.
        """
        return self.__class__(
            ((-self.coords[0] + self.coords[2] - 1),
             self.coords[1],
             self.coords[2]))

    rotation_coefficients = {
        0: (( 1,  0,  0,  0), ( 0,  1,  0,  0), ( 0,  0,  1,  0)),
        1: (( 0, -1, -1,  0), ( 1,  0,  0,  0), ( 0,  0, -1,  1)),
        2: ((-1,  0,  1, -1), ( 0, -1, -1,  0), ( 0,  0,  1,  0)),
        3: (( 0,  1,  0,  0), (-1,  0,  1, -1), ( 0,  0, -1,  1)),}
    """Pre-computed matrix for rotation by *n* 90-degree steps.
    Mapping of rotation unit (step) to coefficients matrix:
    ((x, y, z, 1) for x, (x, y, z, 1) for y, (x, y, z, 1) for z)."""

    def rotate0(self, steps, axis=None):
        """
        Rotate about (0,0).  For each 90-degree increment (step)::

            x_new = -y - z
            y_new = x
            z_new = 1 - z

        The `self.rotation_coefficients` matrix is used rather than repeated
        applications of the above rule.  The `axis` parameter is ignored.
        """
        coeffs = self.rotation_coefficients[steps]
        x = (coeffs[0][3]
             + coeffs[0][0] * self.coords[0]
             + coeffs[0][1] * self.coords[1]
             + coeffs[0][2] * self.coords[2])
        y = (coeffs[1][3]
             + coeffs[1][0] * self.coords[0]
             + coeffs[1][1] * self.coords[1]
             + coeffs[1][2] * self.coords[2])
        z = (coeffs[2][3]
             + coeffs[2][0] * self.coords[0]
             + coeffs[2][1] * self.coords[1]
             + coeffs[2][2] * self.coords[2])
        return self.__class__((x, y, z))

    def neighbors(self):
        """Return a list of adjacent cells."""
        x, y, z = self.coords
        # counterclockwise from right
        if z == 0:
            return (self.__class__((x + 1, y,     0)), # right, 1 right
                    self.__class__((x + 1, y,     1)), # up, 1 right
                    self.__class__((x,     y,     1)), # up
                    self.__class__((x - 1, y,     0)), # left
                    self.__class__((x,     y - 1, 1)), # down
                    self.__class__((x + 1, y - 1, 1))) # down, 1 right
        else:
            return (self.__class__((x,     y,     0)), # right
                    self.__class__((x,     y + 1, 0)), # right, 1 up
                    self.__class__((x,     y + 1, 1)), # up, 1 up
                    self.__class__((x - 1, y + 1, 0)), # left, 1 up
                    self.__class__((x - 1, y,     0)), # left
                    self.__class__((x,     y - 1, 1))) # down


class SquareGrid3DCoordSetMixin:

    """
    Attributes and methods for pseudo-3-dimensional square grid coordinate set.
    """

    coord_class = SquareGrid3D
    intersection_coord_class = Cartesian2D

    def intersections(self):
        coords = set()
        for (x,y,z) in self:
            if self.coord_class((x + (z == 0), y + (z == 1), z)) in self:
                coords.add(self.intersection_coord_class(
                    (x + (z == 0), y + (z == 1))))
        return coords


class SquareGrid3DCoordSet(SquareGrid3DCoordSetMixin, Cartesian3DCoordSet):

    """Pseudo-3-dimensional square grid coordinate set."""

    pass


class SquareGrid3DView(SquareGrid3DCoordSetMixin, CartesianPseudo3DView):

    """
    Pseudo-3-dimensional (+x,+y)-quadrant square grid coordinate set with
    bounds
    """

    pass


class Hexagonal2D(Cartesian2D):

    """
    2D hexagonal coordinate system: (x, y).
    The x and y axes are not perpendicular, but separated by 60 degrees::

                        __
                     __/  \
                  __/  \__/
               __/  \__/  \
            __/  \__/  \__/
           /  \__/  \__/  \
          4\__/  \__/  \__/
           /  \__/  \__/  \
          3\__/  \__/  \__/
           /  \__/  \__/  \
          2\__/  \__/  \__/
           /  \__/  \__/ 4
          1\__/  \__/ 3
           /  \__/ 2
        y=0\__/ 1
           x=0

    The x-axis could also be considered horizontal, with the y-axis slanted up
    and to the right, but the representation above is easier to draw in ASCII.
    """

    rotation_steps = 6

    rotation_axes = None

    flippable = True

    def flip0(self):
        """
        Flip about y-axis::

            x_new = -x
            y_new = x + y
        """
        return self.__class__((-self.coords[0],
                               self.coords[1] + self.coords[0]))

    rotation_coefficients = {
        0: (( 1,  0), ( 0,  1)),
        1: (( 0, -1), ( 1,  1)),
        2: ((-1, -1), ( 1,  0)),
        3: ((-1,  0), ( 0, -1)),
        4: (( 0,  1), (-1, -1)),
        5: (( 1,  1), (-1,  0))}
    """Pre-computed matrix for rotation by *n* 60-degree steps.
    Mapping of rotation unit (step) to coefficients matrix:
    ((x, y) for x, (x, y) for y)."""

    def rotate0(self, steps):
        """
        Rotate about (0,0).  For each 60-degree increment (step)::

            x_new = -y
            y_new = x + y

        The `self.rotation_coefficients` matrix is used rather than repeated
        applications of the above rule.
        """
        coeffs = self.rotation_coefficients[steps]
        x = coeffs[0][0] * self.coords[0] + coeffs[0][1] * self.coords[1]
        y = coeffs[1][0] * self.coords[0] + coeffs[1][1] * self.coords[1]
        return self.__class__((x, y))

    def neighbors(self):
        """Return a list of adjacent cells."""
        x, y = self.coords
        # counterclockwise from right
        return (self.__class__((x + 1, y)),       # right
                self.__class__((x,     y + 1)),   # above-right
                self.__class__((x - 1, y + 1)),   # above-left
                self.__class__((x - 1, y)),       # left
                self.__class__((x,     y - 1)),   # below-left
                self.__class__((x + 1, y - 1)))   # below-right


class Hexagonal2DCoordSet(Cartesian2DCoordSet):

    """2 dimensional hex coordinate set"""

    coord_class = Hexagonal2D


class Hexagonal2DView(Cartesian2DView):

    """
    2 dimensional (+,+)-quadrant hex-cell coordinate set with bounds
    """

    coord_class = Hexagonal2D


class Triangular3D(Cartesian3D):

    """
    Pseudo-3D (2D + orientation) triangular coordinate system: (x, y, z).
    The x and y axes are not perpendicular, but separated by 60 degrees::

                     ____________________
                    /\  /\  /\  /\  /\  /
                  4/__\/__\/__\/__\/__\/
                  /\  /\  /\  /\  /\  /
                3/__\/__\/__\/__\/__\/
                /\  /\  /\  /\  /\  /
              2/__\/__\/__\/__\/__\/
              /\  /\  /\  /\  /\  /
            1/__\/__\/__\/__\/__\/            ____
            /\  /\  /\  /\  /\  /      /\     \  /
        y=0/__\/__\/__\/__\/__\/   z=0/__\  z=1\/
           x=0  1   2   3   4
    """

    rotation_steps = 6

    rotation_axes = None

    flippable = True

    def flip0(self, axis=None):
        """
        Flip about y-axis::

            x_new = -(x + y + z)
            y_new = y
            z_new = z

        The `axis` parameter is ignored.
        """
        return self.__class__(
            (-(self.coords[0] + self.coords[1] + self.coords[2]),
             self.coords[1],
             self.coords[2]))

    rotation_coefficients = {
        0: (( 1,  0,  0,  0), ( 0,  1,  0,  0), ( 0,  0,  1,  0)),
        1: (( 0, -1,  0, -1), ( 1,  1,  1,  0), ( 0,  0, -1,  1)),
        2: ((-1, -1, -1, -1), ( 1,  0,  0,  0), ( 0,  0,  1,  0)),
        3: ((-1,  0,  0, -1), ( 0, -1,  0, -1), ( 0,  0, -1,  1)),
        4: (( 0,  1,  0,  0), (-1, -1, -1, -1), ( 0,  0,  1,  0)),
        5: (( 1,  1,  1,  0), (-1,  0,  0, -1), ( 0,  0, -1,  1)),}
    """Pre-computed matrix for rotation by *n* 60-degree steps.
    Mapping of rotation unit (step) to coefficients matrix:
    ((x, y, z, 1) for x, (x, y, z, 1) for y, (x, y, z, 1) for z)."""

    def rotate0(self, steps, axis=None):
        """
        Rotate about (0,0).  For each 60-degree increment (step)::

            x_new = -y - 1
            y_new = x + y + z
            z_new = 1 - z

        The `self.rotation_coefficients` matrix is used rather than repeated
        applications of the above rule.  The `axis` parameter is ignored.
        """
        coeffs = self.rotation_coefficients[steps]
        x = (coeffs[0][3]
             + coeffs[0][0] * self.coords[0]
             + coeffs[0][1] * self.coords[1]
             + coeffs[0][2] * self.coords[2])
        y = (coeffs[1][3]
             + coeffs[1][0] * self.coords[0]
             + coeffs[1][1] * self.coords[1]
             + coeffs[1][2] * self.coords[2])
        z = (coeffs[2][3]
             + coeffs[2][0] * self.coords[0]
             + coeffs[2][1] * self.coords[1]
             + coeffs[2][2] * self.coords[2])
        return self.__class__((x, y, z))

    def neighbors(self):
        """Return a list of adjacent cells."""
        x, y, z = self.coords
        # counterclockwise from right
        if z == 0:
            return (self.__class__((x,     y,     1)), # right
                    self.__class__((x - 1, y,     1)), # left
                    self.__class__((x,     y - 1, 1))) # below
        else:
            return (self.__class__((x + 1, y,     0)), # right
                    self.__class__((x,     y + 1, 0)), # above
                    self.__class__((x,     y,     0))) # left


class Triangular3DCoordSet(Cartesian3DCoordSet):

    """Pseudo-3-dimensional triangular coordinate set."""

    coord_class = Triangular3D


class Triangular3DView(CartesianPseudo3DView):

    """
    Pseudo-3-dimensional (+x,+y)-quadrant triangle-cell coordinate set with
    bounds.
    """

    coord_class = Triangular3D


class TriangularGrid3D(Cartesian3D):

    """
    Pseudo-3D (2D + orientation) triangular coordinate system for gridlines:
    (x, y, z).  The Z dimension is for orientation:

    ==  ==========  ==============================
    z   (x, y) to   direction
    ==  ==========  ==============================
    0   (x+1, y)    0°, horizontal, to the right
    1   (x,   y+1)  60°, up & to the right
    2   (x-1, y+1)  120°, up & to the left
    ==  ==========  ==============================

    Visually::

        z=2  z=1
          \  /
           \/___ z=0
          (x,y)
    """

    rotation_steps = 6

    rotation_axes = None

    flippable = True

    def flip0(self, axis=None):
        """
        Flip about y-axis::

            x1 = -x0

            y1 = x0 + y0

            z1 = 2 - z0

        The `axis` parameter is ignored.
        """
        return self.__class__(
            (-self.coords[0],
             self.coords[0] + self.coords[1],
             2 - self.coords[2]))

    def rotate0(self, steps, axis=None):
        """
        Rotate about (0,0).  For each 60-degree increment (step)::

            x1 = -y0 - ((z0 + 1) // 3)

            y1 = x0 + y0

            z1 = (z0 + 1) % 3

        The `axis` parameter is ignored.
        """
        x1, y1, z1 = self.coords
        for i in range(steps):
            x0, y0, z0 = x1, y1, z1
            x1 = -y0 - int((z0 + 1) / 3)
            y1 = x0 + y0
            z1 = (z0 + 1) % 3
        return self.__class__((x1, y1, z1))

    def neighbors(self):
        """
        Return a list of adjacent cells, counterclockwise from segment, first
        around the origin point then around the endpoint.
        """
        x, y, z = self.coords
        if z == 0:
            return (self.__class__((x    , y,     1)),
                    self.__class__((x,     y,     2)),
                    self.__class__((x - 1, y,     0)),
                    self.__class__((x,     y - 1, 1)),
                    self.__class__((x + 1, y - 1, 2)),
                    self.__class__((x + 1, y - 1, 1)),
                    self.__class__((x + 2, y - 1, 2)),
                    self.__class__((x + 1, y,     0)),
                    self.__class__((x + 1, y,     1)),
                    self.__class__((x + 1, y,     2)))
        elif z == 1:
            return (self.__class__((x,     y,     2)),
                    self.__class__((x - 1, y,     0)),
                    self.__class__((x,     y - 1, 1)),
                    self.__class__((x + 1, y - 1, 2)),
                    self.__class__((x,     y,     0)),
                    self.__class__((x + 1, y,     2)),
                    self.__class__((x,     y + 1, 0)),
                    self.__class__((x,     y + 1, 1)),
                    self.__class__((x,     y + 1, 2)),
                    self.__class__((x - 1, y + 1, 0)))
        elif z == 2:
            return (self.__class__((x - 1, y,     0)),
                    self.__class__((x,     y - 1, 1)),
                    self.__class__((x + 1, y - 1, 2)),
                    self.__class__((x,     y,     0)),
                    self.__class__((x,     y,     1)),
                    self.__class__((x - 1, y + 1, 0)),
                    self.__class__((x - 1, y + 1, 1)),
                    self.__class__((x - 1, y + 1, 2)),
                    self.__class__((x - 2, y + 1, 0)),
                    self.__class__((x - 1, y,     1)))

    endpoint_deltas = {
        0: (+1,  0),    # 0°, horizontal, to the right
        1: ( 0, +1),    # 60°, up & to the right
        2: (-1, +1)}    # 120°, up & to the left

    def endpoint(self):
        """
        Return the coordinates of the endpoint of this segment, a segment
        sharing this segment's direction.
        """
        x, y, z = self.coords
        delta_x, delta_y = self.endpoint_deltas[z]
        return self.__class__((x + delta_x, y + delta_y, z))

    def intersection_coordinates(self):
        """
        Return a list of coordinates of the intersection segments of the
        start- and end-points of this coordinate.
        """
        intersections = []
        for coord in (self, self.endpoint()):
            x, y, z = coord
            intersections.extend(self.__class__((x, y, z)) for z in range(6))
        return intersections

    @classmethod
    def point_neighbors(cls, x, y):
        """
        Return a list of segments which adjoin point (x,y), in
        counterclockwise order from 0-degrees right.
        """
        return [cls(coords) for coords in (
            (x, y, 0), (x, y, 1), (x, y, 2),
            (x-1, y, 0), (x, y-1, 1), (x+1, y-1, 2))]


class TriangularGrid3DCoordSetMixin:

    """
    Attributes and methods for pseudo-3-dimensional triangular grid coordinate
    set.
    """

    coord_class = TriangularGrid3D
    intersection_coord_class = TriangularGrid3D

    def intersections(self):
        """
        Represent contstraints on intersections via up to 6 additional columns
        per intersection [*]_, in the form i(x,y,z) (or "x,y,zi").  The
        segment in direction "z" (below) cannot go through the intersection
        (x,y)::

              2    1
               \  /
            3___\/___0
                /\
               /  \
              4    5

        .. [*] Possibly fewer columns for intersections at the edge of a
           puzzle shape.  This represents an optimization.

           Note that since there are already 3 line segments originating at
           each intersection, the cost of intersection constraints is 2 per
           segment, which effectively multiplies the number of coordinate
           columns by 3.

        Starting at 0°, rotating counter-clockwise::

              B  / A
            ____/___     D ____    E ____    F ____
                          /          \
                C        /  D'        \

        * A: 60° (adjacent), no constraints.

        * B: 120° (one-gapper).  3 constraints: 2 legs {1,3}, plus gap {2}.

        * C: 180° (two-gapper).  4 constraints: 2 legs {3,0}, plus gaps {4,5}.

        * D: 240° (three-gapper), no constraints.  However, D' is a one-gapper
          (= B).

        * E: 300° (four-gapper), no constraints.

        * F: 360° (five-gapper), no constraints.

        Both ends of each segment must be checked, but only counter-clockwise
        (to avoid duplication).
        """
        icoords = set()
        for coord in self:
            neighbors = coord.neighbors()
            x, y, z = coord
            # start of segment: check that ccw-adjacent segment not there:
            if neighbors[0] not in self:
                if neighbors[1] in self:
                    icoords.add(self.intersection_coord_class((x, y, z)))
                    icoords.add(
                        self.intersection_coord_class((x, y, (z + 1) % 6)))
                    icoords.add(
                        self.intersection_coord_class((x, y, (z + 2) % 6)))
                elif neighbors[2] in self:
                    icoords.add(self.intersection_coord_class((x, y, z)))
                    icoords.add(
                        self.intersection_coord_class((x, y, (z + 1) % 6)))
                    icoords.add(
                        self.intersection_coord_class((x, y, (z + 2) % 6)))
                    icoords.add(
                        self.intersection_coord_class((x, y, (z + 3) % 6)))
            # end of segment: check that ccw-adjacent segment not there:
            if neighbors[5] not in self:
                # origin of end of segment:
                xo, yo, zo = neighbors[7 - z]
                if neighbors[6] in self:
                    icoords.add(self.intersection_coord_class((xo, yo, z + 3)))
                    icoords.add(
                        self.intersection_coord_class((xo, yo, (z + 4) % 6)))
                    icoords.add(
                        self.intersection_coord_class((xo, yo, (z + 5) % 6)))
                elif neighbors[7] in self:
                    icoords.add(self.intersection_coord_class((xo, yo, z + 3)))
                    icoords.add(
                        self.intersection_coord_class((xo, yo, (z + 4) % 6)))
                    icoords.add(
                        self.intersection_coord_class((xo, yo, (z + 5) % 6)))
                    icoords.add(
                        self.intersection_coord_class((xo, yo, z)))
        return icoords


class TriangularGrid3DCoordSet(TriangularGrid3DCoordSetMixin,
                               Cartesian3DCoordSet):

    """Pseudo-3-dimensional triangular grid coordinate set."""

    pass


class TriangularGrid3DView(TriangularGrid3DCoordSetMixin, CartesianPseudo3DView):

    """
    Pseudo-3-dimensional (+x,+y)-quadrant triangular grid coordinate set with
    bounds.
    """

    def calculate_offset_and_bounds(self):
        xs = [c[0] for c in self]
        # include x-coordinates of endpoints when z==2:
        xs.extend([c.endpoint()[0] for c in self if c[2] == 2])
        ys = [c[1] for c in self]
        zs = [c[2] for c in self]
        # keep Z-offset at 0 to keep Z values unaltered:
        offset = self.coord_class((min(xs), min(ys), 0))
        maxvals = self.coord_class((max(xs), max(ys), max(zs)))
        bounds = maxvals - offset
        return offset, bounds


class HexagonalGrid3D(Cartesian3D):

    """
    Pseudo-3D (2D + orientation) hexagonal coordinate system for gridlines:
    (x, y, z).  (x, y) = lower-left corner of (x, y) hexagon in polyhex grid.
    The Z dimension is for orientation:

    ==  ==========  ==============================
    z   (x, y) to   direction
    ==  ==========  ==============================
    0   (x+1, y)    0°, horizontal, to the right
    1   (x,   y+1)  120°, up & to the left
    2   (x-1, y)    240°, down & to the left
    ==  ==========  ==============================

    Visually::

        z=1
          \
           \____z=0
           /
          /
        z=2
    """

    rotation_steps = 6

    rotation_axes = None

    flippable = True

    def flip0(self, axis=None):
        """
        Flip about y-axis (stack of hexes above origin)::

        ==  ======  =========  ========
        z   x' =    y' =       z' =
        ==  ======  =========  ========
        0   -x      x + y      (-z) % 3

        1   -x + 1  ''         ''

        2   ''      x + y - 1  ''
        ==  ======  =========  ========

        The `axis` parameter is ignored.
        """
        x, y, z = self.coords
        x1 = -x + (z != 0)
        y1 = x + y - (z == 2)
        z1 = (-z) % 3
        return self.__class__((x1, y1, z1))

    def rotate0(self, steps, axis=None):
        """
        Rotate about (0,0).  For each 60-degree increment (step)::

        ==  ======  =========  ===========
        z   x' =    y' =       z' =
        ==  ======  =========  ===========
        0   -y + 1  x + y      (z - 1) % 3

        1   -y      ''         ''

        2   -y + 1  x + y - 1  ''
        ==  ======  =========  ===========

        The `axis` parameter is ignored.
        """
        x1, y1, z1 = self.coords
        for i in range(steps):
            x0, y0, z0 = x1, y1, z1
            x1 = -y0 + (z0 != 1)
            y1 = x0 + y0 - (z0 == 2)
            z1 = (z0 - 1) % 3
        return self.__class__((x1, y1, z1))

    def neighbors(self):
        """
        Return a list of adjacent cells, counterclockwise from segment, first
        around the origin point then around the endpoint.
        """
        x, y, z = self.coords
        if z == 0:
            return (self.__class__((x    , y,     1)),
                    self.__class__((x,     y,     2)),
                    self.__class__((x + 1, y - 1, 1)),
                    self.__class__((x + 1, y,     2)))
        elif z == 1:
            return (self.__class__((x,     y,     2)),
                    self.__class__((x,     y,     0)),
                    self.__class__((x,     y + 1, 2)),
                    self.__class__((x - 1, y + 1, 0)))
        elif z == 2:
            return (self.__class__((x,     y,     0)),
                    self.__class__((x,     y,     1)),
                    self.__class__((x - 1, y,     0)),
                    self.__class__((x,     y - 1, 1)))


class HexagonalGrid3DCoordSet(Cartesian3DCoordSet):

    """Pseudo-3-dimensional hexagonal grid coordinate set."""

    coord_class = HexagonalGrid3D


class HexagonalGrid3DView(CartesianPseudo3DView):

    """
    Pseudo-3-dimensional (+x,+y)-quadrant hexagonal grid coordinate set with
    bounds.
    """

    coord_class = HexagonalGrid3D

    def calculate_offset_and_bounds(self):
        xs = [c[0] for c in self]
        ys = [c[1] for c in self]
        zs = [c[2] for c in self]
        # keep Z-offset at 0 to keep Z values unaltered:
        offset = self.coord_class((min(xs), min(ys), 0))
        maxvals = self.coord_class((max(xs), max(ys), max(zs)))
        bounds = maxvals - offset
        return offset, bounds


def sign(num):
    return cmp(num, 0)

def increment_2D(start, end):
    """
    Given a `start`- and `end`-point which differ in only one dimension,
    return a unit vector increment which if repeatedly added to the
    start-point will eventually result in the end-point.
    """
    return Cartesian2D((sign(end[0] - start[0]), sign(end[1] - start[1])))
