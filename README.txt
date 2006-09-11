===============================
 README |---| Polyform Puzzler
===============================

:Author: David Goodger <goodger@python.org>
:Date: $Date$
:Web site: http://puzzler.sourceforge.net/
:Copyright: |c| 1998-2006 by David J. Goodger
:License: `GPL 2 <COPYING.html>`__

**Polyform Puzzler** is a software toolkit for exploring & solving
polyform puzzles, like Pentominoes and Soma Cubes.  It consists of a
set of front-end applications for specific polyform puzzles and a
Python library that does the heavy lifting.  New polyforms and new
puzzles can easily be defined and added.

.. contents::


Quick-Start
===========

This section is for those who want to get up & running quickly.  Read on for
complete details.

1. Get and install the latest release of Python, available from

       http://www.python.org/

   Python 2.4 or later; Python 2.4.2 or later is recommended.

2. Use the latest Polyform Puzzler code.  Get the code from Subversion
   or from the snapshot:

       http://puzzler.sourceforge.net/puzzler-snapshot.tgz

   See Snapshots_ below for details.

3. In a shell, unpack the snapshot tarball in a temporary directory
   (**not** directly in Python's ``site-packages``) and move into it.
   For example::

       tar xzf puzzler-snapshot.tgz
       cd puzzler

There are two ways to proceed from here: `install it`_, or `just run
it`_:


Install It
----------

This option installs the Polyform Puzzler library into Python's
system-wide standard library.

4. Run ``install.py`` with admin rights.  On Windows systems it may be
   sufficient to double-click ``install.py``.  On Unix, GNU/Linux, or
   Mac OS X, type::

        su
        (enter admin password)
        ./install.py

   See Installation_ below for details.

5. Use a front-end application from the "bin" subdirectory.  For
   example::

       cd bin
       ./pentominoes3x20.py            (Unix/Mac)
       python pentominoes3x20.py       (Windows)

   See Usage_ below for details.


Just Run It
-----------

This option allows you to use the "puzzler" package without installing
it permanently.

4. In the top-level directory (containing the "puzzler", "docs", and
   "bin" directories), run the front-end::

       bin/pentominoes6x10.py          (Unix/Mac)
       python bin\pentominoes6x10.py   (Windows)

   Because Python searches the current working directory for modules &
   packages, it will find the "puzzler" package directory.

   (For Windows users:) If the the Python executable is not on your
   ``PATH``, you will have to specify its location::

       C:\Python24\python bin\pentominoes6x10.py

Note that you will only be able to use the "puzzler" package from that
one location (not from arbitrary locations on your system), unless you
`install it`_, or you set your ``PYTHONPATH`` environment variable.


Snapshots
=========

We recommend that you always use the current snapshot, which is
usually updated within an hour of changes being committed to the
repository:

    http://puzzler.sourceforge.net/puzzler-snapshot.tgz

To keep up to date on the latest developments, either download fresh
copies of the snapshots regularly, or use the `Subversion
repository`_:

    svn co https://svn.sourceforge.net/svnroot/puzzler/trunk/puzzler

.. _Subversion repository: https://sourceforge.net/svn/?group_id=7049


Project Files & Directories
===========================

* README.txt: You're reading it.

* COPYING.txt: Copyright and license details.

* GPL2.txt: The GNU General Public License, version 2.

* setup.py: Installation script.  See "Installation" below.

* install.py: Quick & dirty installation script.  Just run it.  For
  any kind of customization or help though, setup.py must be used.

* puzzler: The project source directory, installed as a Python
  package.

* bin: Polyform puzzler front-end applications directory.

* docs: The project documentation directory.  All project
  documentation is in reStructuredText_ format, and can be converted
  to HTML and other formats using Docutils_.

  - FAQ.txt: Frequently Asked Questions (with answers!).
  - puzzles.txt: list of puzzles implemented and counts of solutions
  - history.txt: Detailed log of changes.
  - todo.txt: To do list.

.. _reStructuredText: http://docutils.sourceforge.net/rst.html
.. _Docutils: http://docutils.sourceforge.net


Installation
============

OS-specific installation instructions follow.  For non-standard
installations (i.e. installing to non-standard places, like your home
directory), please see `Installing Python Modules
<http://docs.python.org/inst/inst.html>`_.


GNU/Linux, BSDs, Unix, Mac OS X, etc.
-------------------------------------

1. Open a shell (terminal).

2. Expand the ``.tgz`` archive into a temporary directory (**not**
   directly into Python's ``site-packages``)::

       tar xzf puzzler-snapshot.tgz

   (The archive file name may not be exactly as shown above.)

3. Go to the directory created by expanding the archive::

       cd <archive_directory_path>

   It contains a distutils setup file "setup.py".

4. Install the package::

       python setup.py install

   If the Python executable isn't on your ``PATH``, you'll have to
   specify the complete path, such as /usr/local/bin/python.  You may
   need root permissions to complete this step.

   You can also just run install.py; it does the same thing.


Windows
-------

1. Double-click on the ``.tgz`` archive; this should open the archive
   in WinZip.  (If you don't have WinZip or equivalent installed,
   please download and install it.)  Extract the archive's contents
   into a temporary directory (**not** directly into Python's
   ``site-packages``).

       tar xzf puzzler-snapshot.tgz

   (The archive file name may not be exactly as shown above.)

2. The extracted folder contains distutils setup files ``setup.py``
   and ``install.py``.  Just double-click ``install.py`` and you're
   done.

   If you have any trouble, try the following:

3. Open a DOS Box (Command Shell, MS-DOS Prompt, or whatever they're
   calling it these days).

4. Go to the directory created by expanding the archive::

       cd <archive_directory_path>

5. Install the package::

       <path_to_python.exe>\python setup.py install


Usage
=====

GNU/Linux, BSDs, Unix, Mac OS X, etc.
-------------------------------------

After unpacking and installing the Polyform Puzzler package, the
applications in the ``bin`` directory can be used to solve puzzles.
For example, type the following commands (in a shell) to solve the
3x20 pentominoes puzzle::

    cd <archive_directory_path>
    bin/pentominoes-3x20.py


Windows
-------

For example, type the following commands (in a command prompt window)
to solve the 3x20 pentominoes puzzle::

    cd <archive_directory_path>
    python bin\pentominoes3x20.py

Alternatively, right-click on the puzzle application file, choose
"Edit with IDLE", then choose "Run script" from the "Edit" menu (or
hit Ctrl+F5).

(If you just double-click on the puzzle application, it will run, but
the output window will disappear as soon as the puzzle finishes.)


Getting Help
============

If you have questions or need assistance with Polyform Puzzler, please
post a message to the Puzzler-Users mailing list
(puzzler-users@lists.sourceforge.net).  Please subscribe_ if possible;
messages from non-subscribers will be held for approval.

`Bug reports`_, patches_, and other contributions are welcome!

.. _subscribe:
   https://lists.sourceforge.net/lists/listinfo/puzzler-users
.. _Bug reports:
   http://sourceforge.net/tracker/?group_id=7049&atid=107049
.. _patches:
   http://sourceforge.net/tracker/?group_id=7049&atid=307049

.. |---| unicode:: U+2014  .. em dash
   :trim:
.. |c| unicode:: U+00A9 .. copyright sign
.. |x| unicode:: U+00D7 .. multiplication sign
   :trim:


..
   Local Variables:
   mode: indented-text
   indent-tabs-mode: nil
   sentence-end-double-space: t
   fill-column: 70
   End:
