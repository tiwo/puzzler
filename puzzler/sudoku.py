#!/usr/bin/env python
# -*- coding: utf-8 -*-
# $Id$

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2010 by David J. Goodger
# License: GPL 2 (see __init__.py)

"""
Sudoku solver with support for front end applications.
"""

import sys
import math
import optparse
from datetime import datetime
import puzzler


usage = '%prog [options] [<puzzle-file>]'

description = """\
9x9 Sudoku puzzle solver.  Supply a Sudoku starting position: either provide
the name of the file containing the position (as <puzzle-file> above), or type
in the starting position at the prompt.  Use periods (".") or zeros ("0") to
represent empty squares in starting positions.  Starting positions must be
either 9 lines of 9 columns, or all on one line, with or without spaces
between digits.  See the README.txt file for details
(http://puzzler.sourceforge.net/README.html#sudoku).
"""

cmdline_problem_text = """\
%s takes one optional command-line argument, the file name of
the starting position.  Omit the command-line argument or use "-" to read
the starting position from standard input."""

stdin_prompt = """
Enter a 9x9 Sudoku starting position: either 9 lines of 9 columns
or 1 big line, "." or "0" for empty squares, spaces optional.
Ctrl-D (on Linux/Mac), Ctrl-Z + Enter (on Windows) to end:
"""


def run(puzzle_class, start_position=None, output_stream=sys.stdout,
        settings=None):
    """Given a `Puzzle` subclass instance, find all solutions."""
    if settings is None:
        settings = Settings(start_position=start_position)
    elif start_position:
        settings.start_position = start_position
    solve(puzzle_class, output_stream, settings)

def run_from_command_line(puzzle_class, output_stream=sys.stdout,
                          settings=None):
    """
    Given a `Puzzle` subclass instance, process the command line and find all
    solutions.
    """
    if settings is None:
        settings = process_command_line()
    solve(puzzle_class, output_stream, settings)

def process_command_line_options():
    """Process command-line options & return a settings object & args."""
    parser = optparse.OptionParser(
        formatter=optparse.TitledHelpFormatter(width=78),
        add_help_option=None, description=description, usage=usage)
    choices = ('x2', 'dlx',)
    parser.add_option(
        '-a', '--algorithm', metavar='NAME', choices=choices,
        default=choices[0],
        help=('Choice of exact cover algorithm.  Choices: %s.'
              % ('"%s" (default), "%s"'
                 % (choices[0], '", "'.join(choices[1:])))))
    parser.add_option(
        '-n', '--stop-after', type='int', metavar='N',
        help='Stop processing after generating N solutions.')
    parser.add_option(
        '-h', '--help', help='Show this help message and exit.', action='help')
    settings, args = parser.parse_args()
    return settings, args

def process_command_line():
    settings, args = process_command_line_options()
    if not args:
        settings.start_position = read_start_position_from_stdin()
    elif len(args) == 1:
        if args[0] == '-':
            settings.start_position = read_start_position_from_stdin()
        else:
            settings.start_position = read_start_position_from_file(args[0])
    else:
        print >>sys.stderr, cmdline_problem_text % (sys.argv[0])
        sys.exit(1)
    return settings

def read_start_position_from_stdin():
    print >>sys.stderr, stdin_prompt
    data = sys.stdin.read()
    return data

def read_start_position_from_file(name):
    try:
        f = open(name)
    except IOError:
        print >>sys.stderr, 'Unable to open file "%s".' % name
        sys.exit(1)
    try:
        try:
            data = f.read()
        except Exception, error:
            print >>sys.stderr, 'Problem reading data from file "%s":' % name
            print >>sys.stderr, '%s: %s' % (error.__class__.__name__, error)
            sys.exit(1)
    finally:
        f.close()
    return data

def solve(puzzle_class, output_stream, settings):
    """Find and record all solutions to a puzzle.  Report on `output_stream`."""
    start = datetime.now()
    puzzle = puzzle_class(settings.start_position)
    solver = puzzler.exact_cover_modules[settings.algorithm].ExactCover(
        puzzle.matrix)
    try:
        try:
            print >>output_stream, ('solving %s:\n'
                                    % puzzle.__class__.__name__)
            print >>output_stream, puzzle.start_position, '\n'
            for solution in solver.solve():
                puzzle.record_solution(
                    solution, solver, stream=output_stream)
                if ( settings.stop_after
                     and solver.num_solutions == settings.stop_after):
                    break
        except KeyboardInterrupt:
            print >>output_stream, 'Session interrupted by user.'
            sys.exit(1)
    finally:
        end = datetime.now()
        duration = end - start
        print >>output_stream, (
            '%s solution%s, %s searches, duration %s'
            % (solver.num_solutions, ('s', '')[solver.num_solutions == 1],
               solver.num_searches, duration))


class DataError(RuntimeError): pass


class Settings(object):

    algorithm = 'x2'
    stop_after = 0
    start_position = ''

    def __init__(self, **keywordargs):
        self.__dict__.update(keywordargs)


class Puzzle(object):

    empties = set(['.', '0'])

    def __init__(self, start_position, init_puzzle=True):
        self.start_position = start_position
        """Text specification of the Sudoku puzzle start position, a
        multi-line string.  For example, in a 4x4 puzzle, the start position
        might look like this::

            1 . . 4
            . 4 . 2
            2 3 . 1
            . . 2 .

        The number of lines must equal the order of the puzzle, including
        blank lines.  The number of space-separated text columns must also
        equal the order of the puzzle.  Empty cells must contain a period (".")
        or a zero ("0").
        """

        self.coordinate_blocks = {}
        """Mapping of (x,y) coordinates to puzzle block."""

        self.matrix = []
        """A list of lists; see ExactCover.load_matrix()."""

        self.matrix_columns = {}
        """Mapping of `self.matrix` column names to indices."""

        if init_puzzle:
            self.init_puzzle()

    def init_puzzle(self):
        """Initialize the puzzle matrix and data attributes."""
        self.build_matrix_header()
        self.init_coordinate_blocks()
        try:
            self.build_matrix()
        except DataError, error:
            print 'Problem with start position: %s.' % (error,)
            sys.exit(1)
        except ValueError, error:
            print 'Non-integer found in start position: %s.' % (error,)
            sys.exit(1)

    def build_matrix_header(self):
        """
        Create and populate the first row of `self.matrix`, a list of column
        names.  Also populate the `self.matrix_columns` mapping.
        """
        headers = ['%ib%i' % (i, b) for b in range(self.order)
                   for i in range(1, self.order + 1)]
        headers.extend('%ic%i' % (i, x) for x in range(self.order)
                       for i in range(1, self.order + 1))
        headers.extend('%ir%i' % (i, y) for y in range(self.order)
                       for i in range(1, self.order + 1))
        headers.extend('+%i,%i' % (x, y) for x in range(self.order)
                       for y in range(self.order))
        if len(headers) != self.order ** 2 * 4:
            raise RuntimeError(
                'Problem with matrix columns: expecting %s columns, %s created'
                % (self.order ** 2 * 4, len(headers)))
        self.matrix_columns = dict((name, i)
                                   for (i, name) in enumerate(headers))
        self.matrix.append(headers)

    def init_coordinate_blocks(self):
        """Populate the `self.coordinate_blocks` mapping."""
        block_size = math.sqrt(self.order)
        # reimplement in subclasses if not a whole square:
        if int(block_size) != block_size:
            raise RuntimeError('self.order (== %i) must be a whole square'
                               % self.order)
        block_size = int(block_size)
        for x in range(self.order):
            for y in range(self.order):
                block_id = x / block_size + block_size * (y / block_size)
                self.coordinate_blocks[(x,y)] = block_id

    def build_matrix(self):
        """
        Create and populate the data rows of `self.matrix`, lists of 0's and
        1's (or other true values).
        """
        filled = self.build_matrix_rows_for_givens()
        self.build_matrix_rows_for_unknowns(filled)

    def build_matrix_rows_for_givens(self):
        """
        Append rows to `self.matrix` from cells in starting position.

        Return a set of IDs for the givens.
        """
        num_cols_in_matrix = len(self.matrix[0])
        filled = set()
        self.normalize_start_position()
        lines = self.start_position.splitlines()
        for y, line in enumerate(lines):
            cells = line.split()
            for x, cell in enumerate(cells):
                if cell in self.empties:
                    continue
                row = [0] * num_cols_in_matrix
                value = int(cell)
                block_id = '%ib%i' % (value, self.coordinate_blocks[(x,y)])
                filled.add(block_id)
                row[self.matrix_columns[block_id]] = 1
                column_id = '%ic%i' % (value, x)
                filled.add(column_id)
                row[self.matrix_columns[column_id]] = 1
                row_id = '%ir%i' % (value, y)
                filled.add(row_id)
                row[self.matrix_columns[row_id]] = 1
                coord_id = '+%i,%i' % (x, y)
                row[self.matrix_columns[coord_id]] = 1
                filled.add(coord_id)
                self.matrix.append(row)
        return filled

    def build_matrix_rows_for_unknowns(self, filled):
        """
        Append rows to `self.matrix` for cells not in starting position.

        `filled` is a set of IDs for the givens.
        """
        num_cols_in_matrix = len(self.matrix[0])
        for block in range(self.order):
            for x in range(self.order):
                for y in range(self.order):
                    if self.coordinate_blocks[(x,y)] != block:
                        continue
                    coord_id = '+%i,%i' % (x, y)
                    if coord_id in filled:
                        continue
                    for value in range(1, self.order + 1):
                        block_id = '%ib%i' % (value,
                                              self.coordinate_blocks[(x,y)])
                        if block_id in filled:
                            continue
                        column_id = '%ic%i' % (value, x)
                        if column_id in filled:
                            continue
                        row_id = '%ir%i' % (value, y)
                        if row_id in filled:
                            continue
                        row = [0] * num_cols_in_matrix
                        row[self.matrix_columns[block_id]] = 1
                        row[self.matrix_columns[column_id]] = 1
                        row[self.matrix_columns[row_id]] = 1
                        row[self.matrix_columns[coord_id]] = 1
                        self.matrix.append(row)

    def normalize_start_position(self):
        pos = self.start_position
        pos = pos.replace('-', '').replace('|', '').replace('+', '')
        pos = pos.replace('0', '.')
        lines = [line for line in pos.splitlines() if line]
        if len(lines) == 1:
            line = lines[0].strip()
            cells = line.split()
            cells = list(''.join(cells))
            if len(cells) != self.order ** 2:
                raise DataError(
                    '1-line starting position: %i numbers found, %i expected'
                    % (len(lines), self.order ** 2))
            self.start_position = (
                '\n'.join(' '.join(cells[n:n+self.order])
                          for n in range(0, self.order ** 2, self.order)))
        elif len(lines) == self.order:
            new_lines = []
            for i, line in enumerate(lines):
                cells = line.split()
                if len(cells) != self.order:
                    cells = list(''.join(cells))
                if len(cells) == self.order:
                    new_lines.append(' '.join(cells))
                else:
                    raise DataError('%i columns found (in row %i), %i expected'
                                    % (len(cells), i + 1, self.order))
            self.start_position = '\n'.join(new_lines)
        else:
            raise DataError('%i rows found, 1 or %i expected'
                            % (len(lines), self.order))

    def record_solution(self, solution, solver, stream=sys.stdout, dated=False):
        formatted = self.format_solution(solution)
        solver.num_solutions += 1
        if dated:
            print >>stream, 'at %s,' % datetime.datetime.now(),
        print >>stream, formatted
        print >>stream

    def format_solution(self, solution):
        matrix = [[0] * self.order for i in range(self.order)]
        for row in solution:
            coord_id, block_id, column_id, row_id = row
            x, y = [int(part) for part in coord_id[1:].split(',')]
            value = int(block_id.split('b')[0])
            matrix[y][x] = value
        return '\n'.join([' '.join([str(cell) for cell in row])
                          for row in matrix])


class Sudoku4x4(Puzzle):

    order = 4


class Sudoku9x9(Puzzle):

    order = 9


class SudokuTest(object):

    start_positions_9x9 = [
"""\
5 3 . . 7 . . . .
6 . . 1 9 5 . . .
. 9 8 . . . . 6 .
8 . . . 6 . . . 3
4 . . 8 . 3 . . 1
7 . . . 2 . . . 6
. 6 . . . . 2 8 .
. . . 4 1 9 . . 5
. . . . 8 . . 7 9
""",
"""\
. . . . . . . . .
. . . . . 3 . 8 5
. . 1 . 2 . . . .
. . . 5 . 7 . . .
. . 4 . . . 1 . .
. 9 . . . . . . .
5 . . . . . . 7 3
. . 2 . 1 . . . .
. . . . 4 . . . 9
""",
# http://en.wikipedia.org/wiki/Algorithmics_of_Sudoku
# "Exceptionally difficult Sudokus (Hardest Sudokus)":
"""\
1.. ... ..2
.9. 4.. .5.
..6 ... 7..

.5. 9.3 ...
... .7. ...
... 85. .4.

7.. ... 6..
.3. ..9 .8.
..2 ... ..1
""",
"""\
. . 1 | . . 4 | . . .
. . . | . 6 . | 3 . 5
. . . | 9 . . | . . .
------+-------+------
8 . . | . . . | 7 . 3
. . . | . . . | . 2 8
5 . . | . 7 . | 6 . .
------+-------+------
3 . . | . 8 . | . . 6
. . 9 | 2 . . | . . .
. 4 . | . . 1 | . . .
""",
"""\
. . . . . . . 3 9
. . . . . 1 . . 5
. . 3 . 5 . 8 . .
. . 8 . 9 . . . 6
. 7 . . . 2 . . .
1 . . 4 . . . . .
. . 9 . 8 . . 5 .
. 2 . . . . 6 . .
4 . . 7 . . . . .
""",
"""\
. 2 . 4 . 3 7 . .
. . . . . . . 3 2
. . . . . . . . 4
. 4 . 2 . . . 7 .
8 . . . 5 . . . .
. . . . . 1 . . .
5 . . . . . 9 . .
. 3 . 9 . . . . 7
. . 1 . . 8 6 . .
""",
# http://en.wikipedia.org/wiki/Algorithmics_of_Sudoku
# "Algorithmic Search for Symmetrical Sudokus with Few Givens":
"""\
. . . . 2 5 . . .
. . . . . 7 3 . .
. . . . . . 4 8 .
. . . . . . . 5 9
7 . . . . . . . 2
3 8 . . . . . . .
. 9 5 . . . . . .
. . 1 6 . . . . .
. . . 8 3 . . . .
""",
# http://magictour.free.fr/top95, first & last puzzles:
"""\
4 . . . . . 8 . 5
. 3 . . . . . . .
. . . 7 . . . . .
. 2 . . . . . 6 .
. . . . 8 . 4 . .
. . . . 1 . . . .
. . . 6 . 3 . 7 .
5 . . 2 . . . . .
1 . 4 . . . . . .
""",
"""\
3 . . . 8 . . . .
. . . 7 . . . . 5
1 . . . . . . . .
. . . . . . 3 6 .
. . 2 . . 4 . . .
. 7 . . . . . . .
. . . . 6 . 1 3 .
. 4 5 2 . . . . .
. . . . . . 8 . .
""",
# http://www.usatoday.com/news/offbeat/2006-11-06-sudoku_x.htm
# "Mathematician claims to have penned hardest sudoku":
"""\
8 5 . . . 2 4 . .
7 2 . . . . . . 9
. . 4 . . . . . .
. . . 1 . 7 . . 2
3 . 5 . . . 9 . .
. 4 . . . . . . .
. . . . 8 . . 7 .
. 1 7 . . . . . .
. . . . 3 6 . 4 .
""",
]

    # http://magictour.free.fr/top95
    magictour = """\
4.....8.5 .3....... ...7..... .2.....6. ....8.4.. ....1.... ...6.3.7. 5..2..... 1.4......
52...6.........7.13...........4..8..6......5...........418.........3..2...87.....
6.....8.3.4.7.................5.4.7.3..2.....1.6.......2.....5.....8.6......1....
48.3............71.2.......7.5....6....2..8.............1.76...3.....4......5....
....14....3....2...7..........9...3.6.1.............8.2.....1.4....5.6.....7.8...
......52..8.4......3...9...5.1...6..2..7........3.....6...1..........7.4.......3.
6.2.5.........3.4..........43...8....1....2........7..5..27...........81...6.....
.524.........7.1..............8.2...3.....6...9.5.....1.6.3...........897........
6.2.5.........4.3..........43...8....1....2........7..5..27...........81...6.....
.923.........8.1...........1.7.4...........658.........6.5.2...4.....7.....9.....
6..3.2....5.....1..........7.26............543.........8.15........4.2........7..
.6.5.1.9.1...9..539....7....4.8...7.......5.8.817.5.3.....5.2............76..8...
..5...987.4..5...1..7......2...48....9.1.....6..2.....3..6..2.......9.7.......5..
3.6.7...........518.........1.4.5...7.....6.....2......2.....4.....8.3.....5.....
1.....3.8.7.4..............2.3.1...........958.........5.6...7.....8.2...4.......
6..3.2....4.....1..........7.26............543.........8.15........4.2........7..
....3..9....2....1.5.9..............1.2.8.4.6.8.5...2..75......4.1..6..3.....4.6.
45.....3....8.1....9...........5..9.2..7.....8.........1..4..........7.2...6..8..
.237....68...6.59.9.....7......4.97.3.7.96..2.........5..47.........2....8.......
..84...3....3.....9....157479...8........7..514.....2...9.6...2.5....4......9..56
.98.1....2......6.............3.2.5..84.........6.........4.8.93..5...........1..
..247..58..............1.4.....2...9528.9.4....9...1.........3.3....75..685..2...
4.....8.5.3..........7......2.....6.....5.4......1.......6.3.7.5..2.....1.9......
.2.3......63.....58.......15....9.3....7........1....8.879..26......6.7...6..7..4
1.....7.9.4...72..8.........7..1..6.3.......5.6..4..2.........8..53...7.7.2....46
4.....3.....8.2......7........1...8734.......6........5...6........1.4...82......
.......71.2.8........4.3...7...6..5....2..3..9........6...7.....8....4......5....
6..3.2....4.....8..........7.26............543.........8.15........8.2........7..
.47.8...1............6..7..6....357......5....1..6....28..4.....9.1...4.....2.69.
......8.17..2........5.6......7...5..1....3...8.......5......2..4..8....6...3....
38.6.......9.......2..3.51......5....3..1..6....4......17.5..8.......9.......7.32
...5...........5.697.....2...48.2...25.1...3..8..3.........4.7..13.5..9..2...31..
.2.......3.5.62..9.68...3...5..........64.8.2..47..9....3.....1.....6...17.43....
.8..4....3......1........2...5...4.69..1..8..2...........3.9....6....5.....2.....
..8.9.1...6.5...2......6....3.1.7.5.........9..4...3...5....2...7...3.8.2..7....4
4.....5.8.3..........7......2.....6.....5.8......1.......6.3.7.5..2.....1.8......
1.....3.8.6.4..............2.3.1...........958.........5.6...7.....8.2...4.......
1....6.8..64..........4...7....9.6...7.4..5..5...7.1...5....32.3....8...4........
249.6...3.3....2..8.......5.....6......2......1..4.82..9.5..7....4.....1.7...3...
...8....9.873...4.6..7.......85..97...........43..75.......3....3...145.4....2..1
...5.1....9....8...6.......4.1..........7..9........3.8.....1.5...2..4.....36....
......8.16..2........7.5......6...2..1....3...8.......2......7..3..8....5...4....
.476...5.8.3.....2.....9......8.5..6...1.....6.24......78...51...6....4..9...4..7
.....7.95.....1...86..2.....2..73..85......6...3..49..3.5...41724................
.4.5.....8...9..3..76.2.....146..........9..7.....36....1..4.5..6......3..71..2..
.834.........7..5...........4.1.8..........27...3.....2.6.5....5.....8........1..
..9.....3.....9...7.....5.6..65..4.....3......28......3..75.6..6...........12.3.8
.26.39......6....19.....7.......4..9.5....2....85.....3..2..9..4....762.........4
2.3.8....8..7...........1...6.5.7...4......3....1............82.5....6...1.......
6..3.2....1.....5..........7.26............843.........8.15........8.2........7..
1.....9...64..1.7..7..4.......3.....3.89..5....7....2.....6.7.9.....4.1....129.3.
.........9......84.623...5....6...453...1...6...9...7....1.....4.5..2....3.8....9
.2....5938..5..46.94..6...8..2.3.....6..8.73.7..2.........4.38..7....6..........5
9.4..5...25.6..1..31......8.7...9...4..26......147....7.......2...3..8.6.4.....9.
...52.....9...3..4......7...1.....4..8..453..6...1...87.2........8....32.4..8..1.
53..2.9...24.3..5...9..........1.827...7.........981.............64....91.2.5.43.
1....786...7..8.1.8..2....9........24...1......9..5...6.8..........5.9.......93.4
....5...11......7..6.....8......4.....9.1.3.....596.2..8..62..7..7......3.5.7.2..
.47.2....8....1....3....9.2.....5...6..81..5.....4.....7....3.4...9...1.4..27.8..
......94.....9...53....5.7..8.4..1..463...........7.8.8..7.....7......28.5.26....
.2......6....41.....78....1......7....37.....6..412....1..74..5..8.5..7......39..
1.....3.8.6.4..............2.3.1...........758.........7.5...6.....8.2...4.......
2....1.9..1..3.7..9..8...2.......85..6.4.........7...3.2.3...6....5.....1.9...2.5
..7..8.....6.2.3...3......9.1..5..6.....1.....7.9....2........4.83..4...26....51.
...36....85.......9.4..8........68.........17..9..45...1.5...6.4....9..2.....3...
34.6.......7.......2..8.57......5....7..1..2....4......36.2..1.......9.......7.82
......4.18..2........6.7......8...6..4....3...1.......6......2..5..1....7...3....
.4..5..67...1...4....2.....1..8..3........2...6...........4..5.3.....8..2........
.......4...2..4..1.7..5..9...3..7....4..6....6..1..8...2....1..85.9...6.....8...3
8..7....4.5....6............3.97...8....43..5....2.9....6......2...6...7.71..83.2
.8...4.5....7..3............1..85...6.....2......4....3.26............417........
....7..8...6...5...2...3.61.1...7..2..8..534.2..9.......2......58...6.3.4...1....
......8.16..2........7.5......6...2..1....3...8.......2......7..4..8....5...3....
.2..........6....3.74.8.........3..2.8..4..1.6..5.........1.78.5....9..........4.
.52..68.......7.2.......6....48..9..2..41......1.....8..61..38.....9...63..6..1.9
....1.78.5....9..........4..2..........6....3.74.8.........3..2.8..4..1.6..5.....
1.......3.6.3..7...7...5..121.7...9...7........8.1..2....8.64....9.2..6....4.....
4...7.1....19.46.5.....1......7....2..2.3....847..6....14...8.6.2....3..6...9....
......8.17..2........5.6......7...5..1....3...8.......5......2..3..8....6...4....
963......1....8......2.5....4.8......1....7......3..257......3...9.2.4.7......9..
15.3......7..4.2....4.72.....8.........9..1.8.1..8.79......38...........6....7423
..........5724...98....947...9..3...5..9..12...3.1.9...6....25....56.....7......6
....75....1..2.....4...3...5.....3.2...8...1.......6.....1..48.2........7........
6.....7.3.4.8.................5.4.8.7..2.....1.3.......2.....5.....7.9......1....
....6...4..6.3....1..4..5.77.....8.5...8.....6.8....9...2.9....4....32....97..1..
.32.....58..3.....9.428...1...4...39...6...5.....1.....2...67.8.....4....95....6.
...5.3.......6.7..5.8....1636..2.......4.1.......3...567....2.8..4.7.......2..5..
.5.3.7.4.1.........3.......5.8.3.61....8..5.9.6..1........4...6...6927....2...9..
..5..8..18......9.......78....4.....64....9......53..2.6.........138..5....9.714.
..........72.6.1....51...82.8...13..4.........37.9..1.....238..5.4..9.........79.
...658.....4......12............96.7...3..5....2.8...3..19..8..3.6.....4....473..
.2.3.......6..8.9.83.5........2...8.7.9..5........6..4.......1...1...4.22..7..8.9
.5..9....1.....6.....3.8.....8.4...9514.......3....2..........4.8...6..77..15..6.
.....2.......7...17..3...9.8..7......2.89.6...13..6....9..5.824.....891..........
3...8.......7....51..............36...2..4....7...........6.13..452...........8..
"""

    blank_start = """\
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
"""

    start4x4 = """\
1 . . 4
. 4 . 2
2 3 . 1
. . 2 .
"""

    @classmethod
    def run9x9(cls, settings):
        for i, pos in enumerate(cls.start_positions_9x9):
            print 'SudokuTest.start_positions_9x9[%i]:\n' % i
            run(Sudoku9x9, start_position=pos, settings=settings)
            print

    @classmethod
    def run_magictour(cls, settings):
        for i, pos in enumerate(cls.magictour.splitlines()):
            print 'SudokuTest.magictour line %i:\n' % (i + 1)
            run(Sudoku9x9, start_position=pos, settings=settings)
            print


if __name__ == '__main__':
    settings, args = process_command_line_options()
    if args:
        print 'Command line arguments ignored: %r' % args
    SudokuTest.run9x9(settings)
    SudokuTest.run_magictour(settings)
