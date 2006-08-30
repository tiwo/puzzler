#!/usr/bin/env python
# $Id$

"""
1795 solutions total:

* 72 solutions omitting H
* 382 omitting J
* 607 omitting L
* 530 omitting N
* 204 omitting Y

All are perfect solutions (i.e. no pieces cross).
"""

from puzzler import puzzles, core

core.solver((puzzles.Tetrasticks5x5Matrix(),))
