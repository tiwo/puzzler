#!/usr/bin/env python
# $Id$

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2015 by David J. Goodger;
#     portions copyright 2010 by Ali Assaf
# License: GPL 2 (see __init__.py)

"""
An implementation of Donald E. Knuth's 'Algorithm X' [1]_ for the generalized
exact cover problem [2]_ using a high-level native data structure technique
devised by Ali Assaf [3]_.

.. [1] http://en.wikipedia.org/wiki/Knuth%27s_Algorithm_X
.. [2] http://en.wikipedia.org/wiki/Exact_cover
.. [3] http://www.cs.mcgill.ca/~aassaf9/python/algorithm_x.html
"""

from pprint import pprint

# optional acceleration with Psyco
try:
    import psyco
    psyco.full()
except ImportError:
    pass


class ExactCover(object):

    """
    Given a sparse matrix of 0s and 1s, find every set of rows containing
    exactly one 1 in each primary column (and at most one 1 in each secondary
    column).  See `load_matrix` for a description of the data structure.
    Uses the native approach to Knuth's Algorithm X.
    """

    def __init__(self, matrix=None, secondary=0, state=None):
        """
        Parameters:

        * `matrix` & `secondary`: see `self.load_matrix`.

        * `state`: a `puzzler.SessionState` object which stores the runtime
          state of this puzzle (we're resuming a previously interrupted
          puzzle), or None (no state, we're starting from the beginning).
        """
        self.columns = None
        """A dictionary mapping column names to sets of row indices (the index
        of each row which contains a 1/True for that column)."""

        self.secondary_columns = None
        """A set of secondary column names."""

        self.rows = None
        """A list of lists of column names.  Each list represents one row of
        the exact cover matrix: all the columns containing a 1/True."""

        self.solution = []
        self.num_solutions = 0
        self.num_searches = 0

        if state:
            self.solution = state.solution
            self.num_solutions = state.num_solutions
            self.num_searches = state.num_searches
        if matrix:
            self.load_matrix(matrix, secondary)

    def load_matrix(self, matrix, secondary=0):
        """
        Convert and store the input `matrix` into `self.columns`,
        `self.secondary_columns`, and `self.rows`.

        The input `matrix` is a two-dimensional list of lists:

        * Each row is a list of equal length.

        * The first row contains the column names: first the puzzle piece
          names, then the solution space coordinates.  For example::

              ['A', 'B', 'C', '0,0', '1,0', '0,1', '1,1']

        * The subsequent rows consist of 1 & 0 (True & False) values.  Each
          row contains a 1/True value in the column identifying the piece, and
          1/True values in each column identifying the position.  There must
          be one row for each possible position of each puzzle piece.

        The `secondary` parameter is the number of secondary (rightmost)
        columns: columns which may, but need not, participate in the solution.
        """
        matrix_iter = iter(matrix)
        column_names = matrix_iter.next()
        self.secondary_columns = set(
            column_names[(len(column_names) - secondary):])
        self.columns = dict((j, set()) for j in column_names)
        self.rows = [
            [column_names[j] for j in range(len(column_names)) if row[j]]
            for row in matrix_iter]
        for (r, row) in enumerate(self.rows):
            for c in row:
                self.columns[c].add(r)

    def solve(self, level=0):
        """A generator that produces all solutions: Algorithm X."""
        if not (set(self.columns) - self.secondary_columns):
            yield self.full_solution()
            return
        self.num_searches += 1
        _size, c = min((len(self.columns[column]), column)
                       for column in self.columns
                       if column not in self.secondary_columns)
        # Since `self.columns` is being modified, a copy must be made here.
        # `sorted()` is used instead of `list()` to get reproducible output.
        for r in sorted(self.columns[c]):
            if len(self.solution) > level:
                if self.solution[level] != r:
                    # skip rows already fully explored
                    continue
            else:
                self.solution.append(r)
            covered = self.cover(r)
            for s in self.solve(level+1):
                yield s
            self.uncover(r, covered)
            self.solution.pop()

    def cover(self, r):
        columns = self.columns
        rows = self.rows
        covered = []
        for j in rows[r]:
            for i in columns[j]:
                for k in rows[i]:
                    if k != j:
                        columns[k].remove(i)
            covered.append(self.columns.pop(j))
        return covered

    def uncover(self, r, covered):
        columns = self.columns
        rows = self.rows
        for j in reversed(rows[r]):
            columns[j] = covered.pop()
            for i in columns[j]:
                for k in rows[i]:
                    if k != j:
                        columns[k].add(i)

    def full_solution(self):
        """
        Return an expanded representation (full row details) of a solution,
        based on the internal minimal representation (row indices).
        """
        return [sorted(self.rows[r]) for r in self.solution]

    def format_solution(self):
        """Return a simple formatted string representation of the solution."""
        self.num_solutions += 1
        solution = self.full_solution()
        parts = ['solution %i:' % self.num_solutions]
        for row in solution:
            parts.append(
                ' '.join(cell for cell in row
                         # omit secondary columns (intersections):
                         if not ((',' in cell) and (cell.endswith('i')))))
        return '\n'.join(parts)


if __name__ == '__main__':
    print 'testing exact_cover_x2.py:\n'
    matrix = [
        'A  B  C  D  E  F  G'.split(),
        [0, 0, 1, 0, 1, 1, 0],
        [1, 0, 0, 1, 0, 0, 1],
        [0, 1, 1, 0, 0, 1, 0],
        [1, 0, 0, 1, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 1],
        [0, 0, 0, 1, 1, 0, 1]]
    puzzle = ExactCover(matrix)
    print 'columns ='
    pprint(puzzle.columns)
    print '\nrows ='
    pprint(puzzle.rows)
    for solution in puzzle.solve():
        print '\n', puzzle.format_solution(), '\n'
        print 'unformatted:\n', solution, '\n'
    print puzzle.num_searches, 'searches'
