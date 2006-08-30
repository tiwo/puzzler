#!/usr/bin/env python
# $Id$

"""
? solutions (very large number)
All are perfect solutions (i.e. no pieces cross).
"""

from puzzler import puzzles, core

core.solver((puzzles.Polysticks1234_6x6MatrixA(),
             puzzles.Polysticks1234_6x6MatrixB(),
             puzzles.Polysticks1234_6x6MatrixC(),
             puzzles.Polysticks1234_6x6MatrixD()))
