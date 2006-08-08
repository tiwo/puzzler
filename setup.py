#!/usr/bin/env python
# $Id$
# Copyright: (C) 1998-2006 by David J. Goodger
# License: GPL 2 (see GPL2.txt)

import sys
import os
import glob
try:
    from distutils.core import setup
    from distutils.command.build_py import build_py
except ImportError:
    print 'Error: The "distutils" standard module, which is required for the '
    print 'installation of Docutils, could not be found.  You may need to '
    print 'install a package called "python-devel" (or similar) on your '
    print 'system using your package manager.'
    sys.exit(1)

# From <http://groups.google.de/groups?as_umsgid=f70e3538.0404141327.6cea58ca@posting.google.com>.
from distutils.command.install import INSTALL_SCHEMES
for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib']


def do_setup():
    if sys.hexversion < 0x02040000:    # Python 2.4
        print """\
Polyform Puzzler requires Python 2.4 or later
(Python %s installed).""" % (sys.version.split()[0],)
        sys.exit(1)
    kwargs = package_data.copy()
    dist = setup(**kwargs)
    return dist

package_data = {
    'name': 'puzzler',
    'description': 'Polyform Puzzler',
    'long_description': """\
Polyform Puzzler is a software toolkit for exploring &
solving polyform puzzles, like Pentominoes and Soma Cubes.
It consists of a set of front-end applications for specific
polyform puzzles and a Python library that does the heavy
lifting.  New polyforms and new puzzles can easily be
defined and added.  Requires Python 2.4 or higher.""", # wrap at col 60
    'url': 'http://puzzler.sourceforge.net/',
    'version': '1',
    'author': 'David Goodger',
    'author_email': 'goodger@python.org',
    'license': 'GPL 2',
    'platforms': 'OS-independent',
    'package_dir': {'puzzler': 'puzzler',},
    'packages': ['puzzler',],
    'scripts' : glob.glob('bin/*.py'),}
"""Distutils setup parameters."""

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: Console',
    'Intended Audience :: End Users/Desktop',
    'Intended Audience :: Education',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: GNU General Public License (GPL)',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Games/Entertainment :: Puzzle Games',
    'Topic :: Scientific/Engineering :: Mathematics',]
"""Trove classifiers for the Distutils "register" command."""


if __name__ == '__main__' :
    do_setup()
