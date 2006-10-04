#!/usr/bin/env python
# $Id$

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2006 by David J. Goodger
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

    def flip0(self):
        """Flip on last dimension, about origin"""
        return self.__class__(self.coords[:-1] + (-self.coords[-1],))

    def flip(self, pivot):
        """Flip about pivot"""
        temp = self - pivot
        return temp.flip0() + pivot


class Cartesian2D(Cartesian1D):

    """2D coordinate system: (x, y)"""

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


class CartesianCoordSet1D(CoordinateSet):

    """1 dimensional unit-cell coordinate set"""

    coord_class = Cartesian1D


class CartesianCoordSet2D(CoordinateSet):

    """2 dimensional square-cell coordinate set"""

    coord_class = Cartesian2D

    def orient2D(self, rotation=0, flip=0, pivot=(0,0)):
        """
        Transform (rotate, flip) the coordinate set according to parameters.
        """
        if not (rotation == 0 and flip == 0):
            newSet = []
            for c in self:
                if flip:
                    c = c.flip(pivot)
                newSet.append(c.rotate(rotation, pivot))
            self.clear()
            self.update(newSet)


class CartesianCoordSet3D(CoordinateSet):

    """3 dimensional cube-cell coordinate set"""

    coord_class = Cartesian3D

    def orient3D(self, rotation=0, axis=0, flip=0, pivot=(0,0,0)):
        """
        Transform (rotate, flip) the coordinate set according to parameters.
        """
        if not (rotation == 0 and flip == 0):
            newSet = []
            for c in self:
                if flip:
                    c = c.flip((axis + 1) % 3, pivot)
                newSet.append(c.rotate(rotation, axis, pivot))
            self.clear()
            self.update(newSet)


class CartesianView2D(CartesianCoordSet2D):

    """
    2 dimensional (+,+)-quadrant square-cell coordinate set with offset,
    bounds, and pivot
    """

    def __init__(self, coord_list, rotation=0, flip=0):
        CartesianCoordSet2D.__init__(self, coord_list)
        # first coords in coordsList is assumed to be pivot:
        pivot = self.coord_class(coord_list[0])
        # transform self under aspect:
        self.orient2D(rotation, flip, pivot)
        self.offset, self.bounds = self.calculate_offset_and_bounds()
        self.pivot = pivot - self.offset
        # move coordSet to top-left at (0,0)
        self._itranslate(-self.offset)

    def __hash__(self):
        return hash(tuple(sorted(self)))

    def calculate_offset_and_bounds(self):
        rowvals = [c[0] for c in self]
        colvals = [c[1] for c in self]
        offset = self.coord_class((min(rowvals), min(colvals)))
        maxvals = self.coord_class((max(rowvals), max(colvals)))
        bounds = maxvals - offset
        return offset, bounds


class CartesianView3D(CartesianCoordSet3D):

    """
    3 dimensional (+,+,+)-quadrant square-cell coordinate set with offset,
    bounds, and pivot
    """

    def __init__(self, coord_list, rotation=0, axis=0, flip=0):
        CartesianCoordSet3D.__init__(self, coord_list)
        # first coords in coordsList is assumed to be pivot:
        pivot = self.coord_class(coord_list[0])
        # transform self under aspect:
        self.orient3D(rotation, axis, flip, pivot)
        self.offset, self.bounds = self.calculate_offset_and_bounds()
        self.pivot = pivot - self.offset
        # move coordSet to top-left at (0,0,0)
        self._itranslate(-self.offset)

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

class CartesianViewPseudo3D(CartesianView3D):

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


class CartesianPath2D:

    """
    2 dimensional path along a square-cell grid's lines.
    """

    segments = None
    """List of path segments (start- and end-points), each a
    `CartesianCoordSet2D`."""

    intersections = None
    """A `CartesianCoordSet2D` of covered internal intersection coordinates."""

    bounds = None
    """"""

    def __init__(self, segments):
        self.segments = []
        self.intersections = CartesianCoordSet2D(())
        x_coords = set()
        y_coords = set()
        for segment in segments:
            if isinstance(segment, tuple):
                self.segments.append(CartesianCoordSet2D(segment))
                start, end = [Cartesian2D(endpoint) for endpoint in segment]
            else:
                self.segments.append(segment)
                start, end = segment
            increment = increment_2D(start, end)
            intersection = start + increment
            while intersection != end:
                self.intersections.add(intersection)
                intersection += increment
            x_coords.add(start[0])
            y_coords.add(start[1])
            x_coords.add(end[0])
            y_coords.add(end[1])
        self.bounds = Cartesian2D((max(x_coords), max(y_coords)))

    def oriented(self, rotation=0, flip=0, pivot=(0,0), normalized=False):
        """
        Transform (rotate, flip) the coordinate set according to parameters.
        """
        if rotation == 0 and flip == 0:
            segments = self.segments
        else:
            segments = []
            for s in self.segments:
                if flip:
                    s = s.flip(pivot)
                segments.append(s.rotate(rotation, pivot))
        if normalized:
            min_x = min(min(start.coords[0], end.coords[0])
                        for (start, end) in segments)
            min_y = min(min(start.coords[1], end.coords[1])
                        for (start, end) in segments)
            for coords in segments:
                coords._itranslate((-min_x, -min_y))
        return self.__class__((start.coords, end.coords)
                              for (start, end) in segments)

    def translate(self, offset, moduli=None):
        """Move by offset"""
        offset = Cartesian2D(offset)
        segments = [segment.translate(offset, moduli)
                    for segment in self.segments]
        new = self.__class__(segments)
        return new

    def labels(self, widths):
        for segment in self.segments:
            start, end = segment
            if start > end:
                start, end = end, start
            increment = increment_2D(start, end)
            suffix = 'vh'[increment[0]]
            intersection = start + increment
            while start != end:
                yield '%0*i,%0*i%s' % (widths[0], start[0],
                                       widths[1], start[1], suffix)
                start += increment
            while intersection != end:
                yield '%0*i,%0*ii' % (widths[0], intersection[0],
                                      widths[1], intersection[1])
                intersection += increment

    def labels3d(self, widths):
        for segment in self.segments:
            start, end = segment
            if start > end:
                start, end = end, start
            increment = increment_2D(start, end)
            suffix = '10'[increment[0]]
            intersection = start + increment
            while start != end:
                yield '%0*i,%0*i,%s' % (widths[0], start[0],
                                       widths[1], start[1], suffix)
                start += increment
            while intersection != end:
                yield '%0*i,%0*ii' % (widths[0], intersection[0],
                                      widths[1], intersection[1])
                intersection += increment

    def __iter__(self):
        return self._segment_generator()

    def __str__(self):
        return ('CartesianPath2D(\n    segments=%s,\n    intersections=%s)'
                % (self.segments, self.intersections))

    def __hash__(self):
        return hash(self._segments())

    def __eq__(self, other):
        return (self.bounds == other.bounds
                and self._segments() == other._segments())

    def __ne__(self, other):
        return (self.bounds != other.bounds
                or self._segments() != other._segments())

    def _segments(self):
        return tuple(sorted(self._segment_generator()))

    def _segment_generator(self):
        for segment in self.segments:
            yield tuple(sorted(segment))


class SquareGrid3D(Cartesian3D):

    """
    Pseudo-3D (2D + orientation) square coordinate system for gridlines: (x,
    y, z).  The Z dimension is for orientation: z==0 for horizontal line
    segments (from (x,y) to (x+1,y)), and z==1 for vertical line segments
    (from (x,y) to (x,y+1)).  The Z value indicates the index of the dimension
    to increment.
    """

    def flip0(self, axis=None):
        """
        Flip about y-axis::

            x_new = -x + z - 1
            y_new = y
            z_new = z

        The `axis` parameter is ignored.
        """
        return self.__class__(
            ((-self.coords[0] + self.coords[2] + 1),
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


class SquareGridCoordSet3D(CartesianCoordSet3D):

    """Pseudo-3-dimensional square grid coordinate set."""

    coord_class = SquareGrid3D


class SquareGridView3D(CartesianViewPseudo3D):

    """
    Pseudo-3-dimensional (+x,+y)-quadrant square grid coordinate set with
    offset, bounds, and pivot.
    """

    coord_class = SquareGrid3D


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


class HexagonalCoordSet2D(CartesianCoordSet2D):

    """2 dimensional hex coordinate set"""

    coord_class = Hexagonal2D


class HexagonalView2D(CartesianView2D):

    """
    2 dimensional (+,+)-quadrant hex-cell coordinate set with offset,
    bounds, and pivot
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


class TriangularCoordSet3D(CartesianCoordSet3D):

    """Pseudo-3-dimensional triangular coordinate set."""

    coord_class = Triangular3D


class TriangularView3D(CartesianViewPseudo3D):

    """
    Pseudo-3-dimensional (+x,+y)-quadrant triangle-cell coordinate set with
    offset, bounds, and pivot.
    """

    coord_class = Triangular3D


def sign(num):
    return cmp(num, 0)

def increment_2D(start, end):
    """
    Given a `start`- and `end`-point which differ in only one dimension,
    return a unit vector increment which if repeatedly added to the
    start-point will eventually result in the end-point.
    """
    return Cartesian2D((sign(end[0] - start[0]), sign(end[1] - start[1])))
