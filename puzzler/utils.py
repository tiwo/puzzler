#!/usr/bin/env python
# $Id$

# Author: David Goodger <goodger@python.org>
# Copyright: (C) 1998-2012 by David J. Goodger
# License: GPL 2 (see __init__.py)

"""
Common utility functions.
"""

import locale


def thousands(number):
    return locale.format('%d', number, grouping=True)
