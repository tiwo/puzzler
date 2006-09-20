# $Id$

"""
==================
 Polyform Puzzler
==================

"Polyform Puzzler" is a Python library (``puzzler``) and a set of front-end
applications (solvers) for exploring & solving polyform puzzles.
"""

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2006 by David J. Goodger
# License: 
#     This program is free software; you can redistribute it and/or modify
#     it under the terms of the GNU General Public License version 2
#     as published by the Free Software Foundation.
#
#     This program is distributed in the hope that it will be useful, but
#     WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#     General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program; if not, refer to
#     http://puzzler.sourceforge.net/GPL2.txt or write to the Free Software
#     Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA, USA  02111-1307

import sys
import os
import copy
import optparse
import cPickle as pickle
from datetime import datetime, timedelta
from puzzler import exact_cover


def run(puzzle_class, output_stream=sys.stdout, settings=None):
    """
    Given a `puzzler.puzzles.Puzzle` subclass, process the command line and
    either find all solutions or process the solution supplied.
    """
    if settings is None:
        settings = process_command_line()
    if settings.read_solution:
        read_solution(puzzle_class, settings)
    else:
        state = SessionState.restore(settings.save_search_state)
        solve(puzzle_class, state, output_stream, settings)

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
        '-S', '--save-search-state', metavar='FILE',
        help='Automatically save & restore the search state to/from FILE.')
    parser.add_option(
        '-h', '--help', help='Show this help message and exit.', action='help')
    settings, args = parser.parse_args()
    if args:
        print >>sys.stderr, (
            '%s takes no command-line arguments; "%s" ignored.'
            % (sys.argv[0], ' '.join(args)))
    return settings

def read_solution(puzzle_class, settings):
    """A solution record was supplied; just read & process it."""
    puzzle = puzzle_class.components()[0](init_puzzle=False)
    s_matrix = puzzle.read_solution(settings.read_solution)
    if settings.svg:
        puzzle.write_svg(settings.svg, s_matrix=copy.deepcopy(s_matrix))
    if settings.x3d:
        puzzle.write_x3d(settings.x3d, s_matrix=copy.deepcopy(s_matrix))

def solve(puzzle_class, state, output_stream, settings):
    """Find and record all solutions to a puzzle.  Report on `output_stream`."""
    start = datetime.now()
    matrices = []
    stats = []
    puzzles = []
    for component in puzzle_class.components():
        if component.__name__ not in state.completed_components:
            puzzles.append(component())
    for puzzle in puzzles:
        matrices.append(
            exact_cover.convert_matrix(puzzle.matrix, puzzle.secondary_columns))
    solver = exact_cover.ExactCover(state=state)
    last_solutions = state.last_solutions
    last_searches = state.last_searches
    for i, puzzle in enumerate(puzzles):
        print >>output_stream, 'solving %s:\n' % puzzle.__class__.__name__
        solver.root = matrices[i]
        try:
            for solution in solver.solve():
                state.store(solver)
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
        except KeyboardInterrupt:
            state.store(solver)
            state.close()
            sys.exit(1)
        stats.append((solver.num_solutions - last_solutions,
                      solver.num_searches - last_searches))
        if ( settings.stop_after
             and solver.num_solutions == settings.stop_after):
            break
        state.last_solutions = last_solutions = solver.num_solutions
        state.last_searches = last_searches = solver.num_searches
        state.completed_components.add(puzzle.__class__.__name__)
    end = datetime.now()
    duration = end - start
    print >>output_stream, (
        '%s solutions, %s searches, duration %s'
        % (solver.num_solutions, solver.num_searches, duration))
    if len(puzzles) > 1:
        for i, (solutions, searches) in enumerate(stats):
            print >>output_stream, (
                '(%s: %s solutions, %s searches)'
                % (puzzles[i].__class__.__name__, solutions, searches))


class SessionState(object):

    """Stores & restores the state of the session."""

    store_interval = timedelta(seconds=60)

    def __init__(self, path=None):
        if path:
            self.state_file = open(path, 'wb')
        else:
            self.state_file = None
        self.solution = []
        self.num_solutions = 0
        self.num_searches = 0
        self.last_solutions = 0
        self.last_searches = 0
        self.completed_components = set()
        self.last_stored = datetime.min

    def __getstate__(self):
        # copy the dict since we change it:
        odict = self.__dict__.copy()
        # remove file entry:
        del odict['state_file']
        return odict

    def store(self, solver):
        self.num_solutions = solver.num_solutions
        self.num_searches = solver.num_searches
        self.last_stored = datetime.now()
        if self.state_file:
            self.state_file.seek(0)
            pickle.dump(self, self.state_file, 2)
            self.state_file.flush()

    def store_periodically(self, solver):
        now = datetime.now()
        if now - self.last_stored > self.store_interval:
            self.store(solver)

    def close(self):
        if self.state_file:
            self.state_file.close()

    @classmethod
    def restore(cls, path):
        if path:
            if os.path.exists(path):
                state_file = open(path, 'rb')
                state = pickle.load(state_file)
                state_file.close()
                state.state_file = open(path, 'wb')
                return state
        return cls(path)
