#!/usr/bin/env python
# $Id$

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2006 by David J. Goodger
# License: GPL 2 (see __init__.py)

"""
Core coordination for Polyform Puzzler.
"""

import sys
import copy
import datetime
import optparse
from puzzler import exact_cover


def process_command_line():
    """Process command-line options & return a settings object."""
    parser = optparse.OptionParser(
        formatter=optparse.TitledHelpFormatter(width=78),
        add_help_option=None)
    parser.add_option(
        '-n', '--stop-after', type='int', metavar='N',
        help='Stop processing after generating N solutions.')
    parser.add_option(
        '-r', '--read-solution', metavar='FILE',
        help='Read a solution record from FILE for further processing.')
    parser.add_option(
        '-s', '--svg', metavar='FILE',
        help='Format the first solution found (or supplied via -r) as SVG '
        'and write it to FILE.')
    parser.add_option(
        '-x', '--x3d', metavar='FILE',
        help='Format the first solution found (or supplied via -r) as X3D '
        'and write it to FILE.')
    parser.add_option(
        '-h', '--help', help='Show this help message and exit.', action='help')
    settings, args = parser.parse_args()
    if args:
        print >>sys.stderr, (
            '%s takes no command-line arguments; "%s" ignored.'
            % (sys.argv[0], ' '.join(args)))
    return settings

def read_solution(puzzle_class, settings):
    """Solution record supplied; read & process it."""
    puzzle = puzzle_class.components()[0](init_puzzle=False)
    s_matrix = puzzle.read_solution(settings.read_solution)
    if settings.svg:
        puzzle.write_svg(settings.svg, s_matrix=copy.deepcopy(s_matrix))
    if settings.x3d:
        puzzle.write_x3d(settings.x3d, s_matrix=copy.deepcopy(s_matrix))

def solver(puzzle_class, output_stream=sys.stdout, settings=None):
    """
    Given a `puzzler.puzzles.Puzzle` subclass, find all solutions and report
    on `output_stream`.
    """
    start = datetime.datetime.now()
    if settings is None:
        settings = process_command_line()
    if settings.read_solution:
        read_solution(puzzle_class, settings)
        return
    matrices = []
    stats = []
    puzzles = [component() for component in puzzle_class.components()]
    for puzzle in puzzles:
        matrices.append(
            exact_cover.convert_matrix(puzzle.matrix, puzzle.secondary_columns))
    solver = exact_cover.ExactCover()
    last_solutions = 0
    last_searches = 0
    for i, puzzle in enumerate(puzzles):
        print >>output_stream, 'solving %s:\n' % puzzle.__class__.__name__
        solver.root = matrices[i]
        for solution in solver.solve():
            puzzle.record_solution(solution, solver, stream=output_stream)
            if settings.svg:
                puzzle.write_svg(settings.svg, solution)
                settings.svg = False
            if settings.x3d:
                puzzle.write_x3d(settings.x3d, solution)
                settings.x3d = False
            if ( settings.stop_after
                 and solver.num_solutions == settings.stop_after):
                break
        stats.append((solver.num_solutions - last_solutions,
                      solver.num_searches - last_searches))
        if ( settings.stop_after
             and solver.num_solutions == settings.stop_after):
            break
        last_solutions = solver.num_solutions
        last_searches = solver.num_searches
    end = datetime.datetime.now()
    duration = end - start
    print >>output_stream, (
        '%s solutions, %s searches, duration %s'
        % (solver.num_solutions, solver.num_searches, duration))
    if len(puzzles) > 1:
        for i, (solutions, searches) in enumerate(stats):
            print >>output_stream, (
                '(%s: %s solutions, %s searches)'
                % (puzzles[i].__class__.__name__, solutions, searches))
