# $Id$

"""
==================
 Polyform Puzzler
==================

"Polyform Puzzler" is a Python library (``puzzler``) and a set of front-end
applications (solvers) for exploring & solving polyform puzzles and Sudoku
puzzles.
"""

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2012 by David J. Goodger
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
from puzzler import exact_cover_dlx
from puzzler import exact_cover_x2
from puzzler import info
from puzzler.utils import thousands

try:
    import locale
    locale.setlocale(locale.LC_ALL, '')
except:
    pass


__version__ = '1+SVN'

version_template = (
    '%%prog\nPolyform Puzzler version %s [%s], Python %s, on %s'
    % (__version__, info.revision,
       sys.version.split()[0], sys.platform))

exact_cover_modules = {
    'dlx': exact_cover_dlx,
    'x2': exact_cover_x2,}

algorithm_choices = ('x2', 'dlx',)

try:
    from puzzler import exact_cover_c
    exact_cover_modules['c'] = exact_cover_c
    algorithm_choices = ('c',) + algorithm_choices
except ImportError:
    pass


def run(puzzle_class, output_stream=sys.stdout, settings=None):
    """
    Given a `puzzler.puzzles.Puzzle` subclass, process the command line and
    dispatch accordingly.
    """
    if settings is None:
        settings = process_command_line()
    if settings.read_solution:
        read_solution(puzzle_class, settings)
    elif settings.report_search_state:
        report_search_state(puzzle_class, output_stream, settings)
    else:
        return solve(puzzle_class, output_stream, settings)

def process_command_line():
    """Process command-line options & return a settings object."""
    parser = optparse.OptionParser(
        formatter=optparse.TitledHelpFormatter(width=78),
        add_help_option=None)
    parser.add_option(
        '-a', '--algorithm', metavar='NAME', choices=algorithm_choices,
        default=algorithm_choices[0],
        help=('Choice of exact cover algorithm.  Choices: %s.'
              % ('"%s" (default), "%s"'
                 % (algorithm_choices[0], '", "'.join(algorithm_choices[1:])))))
    parser.add_option(
        '-n', '--stop-after', type='int', metavar='N',
        help='Stop processing after generating N solution(s). '
        'Or, combined with -r/--read-solution, read solution number N.')
    parser.add_option(
        '-r', '--read-solution', metavar='FILE',
        help='Read a solution record from FILE for further processing '
        ' ("-" for STDIN).')
    parser.add_option(
        '-s', '--svg', metavar='FILE',
        help='Format the first solution found (or supplied via -r) as SVG '
        'and write it to FILE ("-" for STDOUT).')
    parser.add_option(
        '-x', '--x3d', metavar='FILE',
        help='Format the first solution found (or supplied via -r) as X3D '
        'and write it to FILE ("-" for STDOUT).')
    default = search_state_default()
    parser.add_option(
        '-S', '--search-state-file', metavar='FILE', default=default,
        help=('Use FILE for automatic search state save & restore.  '
              'Default: "%s".' % default))
    parser.add_option(
        '-N', '--no-search-state', dest='search_state_file',
        action='store_const', const=None,
        help='Disable automatic search state save & restore.')
    parser.add_option(
        '-R', '--report-search-state', action='store_true',
        help=('Report on the current search state (partial solution), '
              'useful for long-running puzzles. Use -S/--search-state-file '
              'to read a search state file other than the default.'))
    parser.add_option(
        '-V', '--version',
        help="Show Polyform Puzzler's version information and exit.",
        action='version')
    parser.version = version_template
    parser.add_option(
        '-h', '--help', help='Show this help message and exit.', action='help')
    settings, args = parser.parse_args()
    if args:
        print >>sys.stderr, (
            '%s takes no command-line arguments; "%s" ignored.'
            % (sys.argv[0], ' '.join(args)))
    return settings

def search_state_default():
    """Return the default name for the search state file."""
    prog = os.path.basename(sys.argv[0])
    if prog.endswith('.py') or prog.endswith('.pyw') or prog.endswith('.pyc'):
        prog = prog[:prog.rfind('.py')]
    return '%s.state' % prog

def read_solution(puzzle_class, settings):
    """A solution record was supplied; just read & process it."""
    puzzle = puzzle_class.components()[0](init_puzzle=False)
    s_matrix = puzzle.read_solution(
        settings.read_solution, solution_number=settings.stop_after)
    if settings.svg:
        puzzle.write_svg(settings.svg, s_matrix=copy.deepcopy(s_matrix))
    if settings.x3d:
        puzzle.write_x3d(settings.x3d, s_matrix=copy.deepcopy(s_matrix))

def report_search_state(puzzle_class, output_stream, settings):
    state = SessionState.restore(settings.search_state_file, read_only=True)
    solver = exact_cover_modules[settings.algorithm].ExactCover(state=state)
    puzzle = puzzle_class.components()[0]()
    solver.load_matrix(puzzle.matrix, puzzle.secondary_columns)
    solution = solver.full_solution()
    if state.num_searches:
        print >>output_stream, (
            '\nSession report: %s solution%s, %s searches.\n'
            % (thousands(state.num_solutions),
               ('' if state.num_solutions == 1 else 's'),
               thousands(state.num_searches)))
        output_stream.flush()
    puzzle.record_solution(
        solution, solver, stream=output_stream)
    if settings.svg:
        puzzle.write_svg(settings.svg, solution)
    if settings.x3d:
        puzzle.write_x3d(settings.x3d, solution)

def solve(puzzle_class, output_stream, settings):
    """Find and record all solutions to a puzzle.  Report on `output_stream`."""
    start = datetime.now()
    try:
        state = SessionState.restore(settings.search_state_file)
    except IOError, error:
        print >>sys.stderr, 'Unable to initialize the search state file:'
        print >>sys.stderr, '%s: %s' % (error.__class__.__name__, error)
        sys.exit(1)
    solver = exact_cover_modules[settings.algorithm].ExactCover(state=state)
    if state.num_searches:
        print >>output_stream, (
            '\nResuming session (%s solution%s, %s searches).\n'
            % (thousands(state.num_solutions),
               ('' if state.num_solutions == 1 else 's'),
               thousands(state.num_searches)))
        output_stream.flush()
    starting_solutions = state.num_solutions
    matrices = []
    stats = []
    puzzles = []
    try:
        try:
            for component in puzzle_class.components():
                if component.__name__ not in state.completed_components:
                    # !!! instantiate inside the loop instead?
                    # will save time initially with multi-part puzzles
                    puzzles.append(component())
            for puzzle in puzzles:
                matrices.append((puzzle.matrix, puzzle.secondary_columns))
            state.init_periodic_save(solver)
            last_solutions = state.last_solutions
            last_searches = state.last_searches
            for i, puzzle in enumerate(puzzles):
                print >>output_stream, ('solving %s:\n'
                                        % puzzle.__class__.__name__)
                output_stream.flush()
                solver.load_matrix(*matrices[i])
                for solution in solver.solve():
                    state.save(solver)
                    if not puzzle.record_solution(solution, solver,
                                                  stream=output_stream):
                        continue
                    if settings.svg:
                        puzzle.write_svg(settings.svg, solution)
                        settings.svg = False
                    if settings.x3d:
                        puzzle.write_x3d(settings.x3d, solution)
                        settings.x3d = False
                    if ( settings.stop_after
                         and ((solver.num_solutions - starting_solutions)
                              >= settings.stop_after)):
                        break
                stats.append((solver.num_solutions - last_solutions,
                              solver.num_searches - last_searches))
                if ( settings.stop_after
                     and solver.num_solutions == settings.stop_after):
                    print >>output_stream, (
                        'User-requested solution limit reached.')
                    break
                state.last_solutions = last_solutions = solver.num_solutions
                state.last_searches = last_searches = solver.num_searches
                state.completed_components.add(puzzle.__class__.__name__)
        except KeyboardInterrupt:
            print >>output_stream, 'Session interrupted by user.'
            state.save(solver, final=True)
            state.close()
            sys.exit(1)
    finally:
        end = datetime.now()
        duration = end - start
        print >>output_stream, (
            '%s solution%s, %s searches, duration %s'
            % (thousands(solver.num_solutions),
               ('' if solver.num_solutions == 1 else 's'),
               thousands(solver.num_searches),
               duration))
        if len(stats) > 1:
            for i, (solutions, searches) in enumerate(stats):
                print >>output_stream, (
                    '(%s: %s solution%s, %s searches)'
                    % (puzzles[i].__class__.__name__,
                       thousands(solutions),
                       ('' if solutions == 1 else 's'),
                       thousands(searches)))
        output_stream.flush()
    state.cleanup()
    return solver.num_solutions


class SessionState(object):

    """Saves & restores the state of the session."""

    save_interval = 60                 # seconds, for thread

    def __init__(self, path=None):
        self.solution = []
        self.num_solutions = 0
        self.num_searches = 0
        self.last_solutions = 0
        self.last_searches = 0
        self.completed_components = set()
        self.lock = threading.Lock()
        self.state_file = None
        self.init_state_file(path)

    def init_state_file(self, path):
        if path:
            if os.path.exists(path):
                self.state_file = open(path, 'r+b')
            else:
                self.state_file = open(path, 'wb')
        else:
            self.state_file = None

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

    def save(self, solver, final=False):
        if self.state_file and self.lock.acquire(final):
            self.num_solutions = solver.num_solutions
            self.num_searches = solver.num_searches
            self.state_file.seek(0)
            pickle.dump(self, self.state_file, 2)
            self.state_file.flush()
            self.state_file.truncate()
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
    def restore(cls, path, read_only=False):
        """
        Return either the saved session state or a new `SessionState` object.
        (A factory function.)
        """
        if path:
            if os.path.exists(path):
                state_file = open(path, 'rb')
                state = pickle.load(state_file)
                state_file.close()
                if not read_only:
                    state.init_state_file(path)
                return state
            elif read_only:
                print >>sys.stderr, (
                    'The search state file "%s" does not exist; exiting.'
                    % path)
                sys.exit(1)
        return cls(path)
