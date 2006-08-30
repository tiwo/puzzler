#!/usr/bin/env python
# $Id$

"""
8x8 grid with 2x2 center hole.
65 solutions
"""

from puzzler import puzzles, core

core.solver((puzzles.Pentominoes8x8CenterHoleMatrixA(),
             puzzles.Pentominoes8x8CenterHoleMatrixB(),))
