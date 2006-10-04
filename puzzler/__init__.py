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
import threading
import copy
import optparse
import time
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
        solve(puzzle_class, output_stream, settings)

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

def solve(puzzle_class, output_stream, settings):
    """Find and record all solutions to a puzzle.  Report on `output_stream`."""
    start = datetime.now()
    try:
        try:
            state = SessionState.restore(settings.save_search_state)
            solver = exact_cover.ExactCover(state=state)
            if state.num_searches:
                print >>output_stream, (
                    '\nResuming session (%s solutions, %s searches).\n'
                    % (state.num_solutions, state.num_searches))
            matrices = []
            stats = []
            puzzles = []
            for component in puzzle_class.components():
                if component.__name__ not in state.completed_components:
                    puzzles.append(component())
            for puzzle in puzzles:
                matrices.append(
                    exact_cover.convert_matrix(puzzle.matrix,
                                               puzzle.secondary_columns))
            state.init_periodic_save(solver)
            last_solutions = state.last_solutions
            last_searches = state.last_searches
            for i, puzzle in enumerate(puzzles):
                print >>output_stream, ('solving %s:\n'
                                        % puzzle.__class__.__name__)
                solver.root = matrices[i]
                for solution in solver.solve():
                    state.save(solver)
                    puzzle.record_solution(
                        solution, solver, stream=output_stream)
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
                state.last_solutions = last_solutions = solver.num_solutions
                state.last_searches = last_searches = solver.num_searches
                state.completed_components.add(puzzle.__class__.__name__)
        except KeyboardInterrupt:
            print >>output_stream, 'Session interrupted by user.'
            state.save(solver)
            state.close()
            sys.exit(1)
    finally:
        end = datetime.now()
        duration = end - start
        print >>output_stream, (
            '%s solutions, %s searches, duration %s'
            % (solver.num_solutions, solver.num_searches, duration))
        if len(stats) > 1:
            for i, (solutions, searches) in enumerate(stats):
                print >>output_stream, (
                    '(%s: %s solutions, %s searches)'
                    % (puzzles[i].__class__.__name__, solutions, searches))
    state.cleanup()


class SessionState(object):

    """Saves & restores the state of the session."""

    save_interval = 60                 # seconds, for thread

    def __init__(self, path=None):
        self.init_runtime(path)
        self.solution = []
        self.num_solutions = 0
        self.num_searches = 0
        self.last_solutions = 0
        self.last_searches = 0
        self.completed_components = set()

    def init_runtime(self, path):
        if path:
            self.state_file = open(path, 'wb')
        else:
            self.state_file = None
        self.lock = threading.Lock()

    def init_periodic_save(self, solver):
        if self.state_file:
            t = threading.Thread(target=self.save_periodically, args=(solver,))
            t.setDaemon(True)
            t.start()

    def __getstate__(self):
        # copy the dict since we change it:
        odict = self.__dict__.copy()
        # remove runtime state:
        del odict['state_file'], odict['lock']
        return odict

    def save(self, solver):
        if self.state_file and self.lock.acquire(False):
            self.num_solutions = solver.num_solutions
            self.num_searches = solver.num_searches
            self.state_file.seek(0)
            pickle.dump(self, self.state_file, 2)
            self.state_file.flush()
            self.lock.release()

    def save_periodically(self, solver):
        """This method is run as a daemon thread."""
        while True:
            time.sleep(self.save_interval)
            self.save(solver)

    def close(self):
        if self.state_file:
            self.state_file.close()

    def cleanup(self):
        if self.state_file:
            path = self.state_file.name
            self.state_file.close()
            os.unlink(path)

    @classmethod
    def restore(cls, path):
        """
        Return either the saved session state or a new `SessionState` object.
        (A factory function.)
        """
        if path:
            if os.path.exists(path):
                state_file = open(path, 'rb')
                state = pickle.load(state_file)
                state_file.close()
                state.init_runtime(path)
                return state
        return cls(path)
