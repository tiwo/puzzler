.. -*- coding: utf-8 -*-

=====================================================
 Polyform Puzzler, New Polyforms, and Recent Results
=====================================================
----------------------------------------------------------------
 A Talk from G4G10: The 10th Gathering for Gardner (2012-03-31)
----------------------------------------------------------------

:Author: David Goodger <goodger@python.org>
:Date: $Date$
:Revision: $Revision$
:Web site: http://puzzler.sourceforge.net/
:Copyright: © 1998-2015 by David J. Goodger
:License: `GPL 2 <../COPYING.html>`__


.. image:: images/puzzler.png
   :align: center


.. sidebar:: Also see:

   * `X’s from G4G10: Gathering for Gardner 10 <g4gX.html>`_
   * `Polyform Puzzler: Puzzles & Solutions <puzzles.html>`_
   * `Polyform Puzzler FAQ <FAQ.html>`_

   Off-site:

   * `My account of G4G10 (blog article)
     <http://www.artima.com/weblogs/viewpost.jsp?thread=341893>`_

.. contents::


I presented this as a whirlwind 5 minute introduction to the Polyform
Puzzler software project at the `10th Gathering for Gardner (G4G10)`_,
Atlanta, Georgia, USA, 2012-03-31.  This version is updated and
contains some extra content that had to be omitted from the talk for
time.

.. _10th Gathering for Gardner (G4G10): http://gathering4gardner.org/

(To get a feel for what the Gatherings are all about `watch this
episode of “The Nature of Things” about Martin Gardner with footage
from Gathering for Gardner 2 in 1996 <http://vimeo.com/7176521>`__.)


Introduction
============

This is my first time at a Gathering for Gardner. I’m grateful and
honoured to have been invited. In order to justify my presence here,
I’d like to tell you about my little project.

Polyform Puzzler is a Free Software project, first published on the
Internet in 2006.  It currently supports 7 different families of
polyforms, several orders of each, and solves several hundred
individual puzzles.  It generates attractive graphics for puzzle
solutions, and even produces 3-D output.


History
=======

.. image:: images/g4g10/imperial-earth.jpg

I first discovered Pentominoes in Arthur C. Clarke’s novel `Imperial
Earth`, probably around the time I was 11 or 12 years old.  I bought a
set of plastic pentominoes at a local hobby store and spent many happy
hours discovering solutions.

The novel’s afterword led me to the work of two of the great thinkers
in the field, Martin Gardner and Solomon W. Golomb.

  .. list-table::
     :class: borderless

     * - .. figure:: images/g4g10/martin-gardner.jpg

            Martin Gardner

       - .. figure:: images/g4g10/solomon-golomb.jpg

            Solomon W. Golomb

*[Omitted from the talk due to time constraints:]*

As a teenager I read some of Martin Gardner’s books, and later, thanks
to my university’s library archives, I was able to read many of his
original `Scientific American` articles.  What a font of knowledge!
The world is a richer place for Martin Gardner having been in it.

Eventually I got my hands on a copy of Golomb’s `Polyominoes`, which
was hard to find in the pre-Amazon.com days.  I now have both
editions.  I was delighted to have been able to meet Professor Golomb
at G4G10.


Early Attempts
==============

.. image:: images/g4g10/pentominoes.png

As a teenager I became interested in computer programming so I
naturally tried to write a pentominoes solver.  I tried to get the
computer to solve puzzles the same way I did – but it didn’t work
well. It was the wrong approach. It’s not just that computers don’t
think the same way people do, it’s that computers *don’t think* at
all.  They’re just fast calculators.

10 or 12 years later I re-implemented my pentominoes solver as a toy
project to learn the Python programming language.  It worked, but it
was *incredibly* slow, and I didn’t take it any further.


Knuth Opened My Eyes
====================

.. image:: images/g4g10/dancing-links.png

.. image:: images/g4g10/matrix.png

Then in the summer of 2006 I learned of a new approach for solving
polyform puzzles, in Donald Knuth’s “Dancing Links” paper. This
approach re-frames puzzles as “exact cover” problems, represented by a
sparse matrix of 0s and 1s and solvable by Knuth’s “Algorithm X”.
Much more suited to solution by computer. My old itch resurfaced.


Success!
========

.. image:: images/ominoes/pentominoes-6x10.png

Using the Python programming language I implemented an Exact Cover
problem solver in a general way, and Polyform Puzzler started
producing results.  Success!


Familiar Polyforms
==================

I implemented the rest of the familiar regular polygon and polyhedron
unit shape polyforms: the polyiamonds, the polyhexes, and the
polycubes.  Prof. Knuth’s paper also discussed polysticks, which
piqued my interest so I implemented those too.  And since Sudoku
puzzles can also be framed as exact cover problems, I also implemented
a Sudoku solver.

.. figure:: images/iamonds/heptiamonds-snowflake-2.png

   heptiamonds snowflake

.. figure:: images/hexes/pentahexes-triangle-1.png

   pentahexes triangle

.. figure:: images/cubes/solid-pentominoes-3x4x5.png

   solid pentominoes 3×4×5

.. figure:: images/sticks/one-sided-tetrasticks-5x5-diamond-lattice.png

   one-sided tetrasticks 5×5 diamond lattice

.. figure:: images/g4g10/sudoku.png

   sudoku


Correspondence
==============

Polyform Puzzler went live on the Internet in 2006, and since then
several puzzle enthusiasts around the world have shared their ideas
with me.

.. list-table::
   :class: borderless

   * - .. image:: images/cubes/pentacubes-corner-crystal.png

     - .. figure:: images/cubes/pentacubes-corner-crystal-small.jpg
          :target: images/cubes/pentacubes-corner-crystal.jpg

          Built with `Kadon's Super Deluxe Quintillions`_.
          Click for the full-size image.

.. _Kadon's Super Deluxe Quintillions:
   http://gamepuzzles.com/polycube.htm#SQd

For example, Nick Maeder of New Zealand devised the pentacubes puzzle
above, “corner crystal”, around 1984.  He had tried to solve it
manually off and on for *22 years*, coming within *one piece* of a
solution.  Polyform Puzzler was able to find a solution after only a
few hours of computer time – now down to just a few minutes, with
faster computers and a much more efficient core solving engine.


Itch: Scratched?
================

.. image:: images/g4g10/dog-scratching.jpg

Finally I had implemented all the existing polyforms that interested
me – I’m biased toward regular unit shapes & symmetrical puzzles.  I
had scratched my own itch, and I didn’t give the project much
attention for a while.

But does this kind of itch ever really go away? Apparently not. About
a year ago I started experiencing flare-ups, so I devised some new
polyforms to explore.


Polytrigs
=========

.. image:: images/trigs/one-sided-tritrigs-hex-4x1.png

First I implemented triangular-grid polysticks, or “polytrigs” as I
called them.  I found only a few references; this form doesn’t seem to
have been explored much before this.  *[Above is the one-sided
tritrigs 4×1 semi-regular hexagon.]*

Recently I heard from Les Shader, who shared the results of his
unpublished work on triangular-grid polysticks from the early 1990s.
Below is his “tritrigs heart” design.  I have Les to thank for my
invitation to this Gathering.

.. image:: images/trigs/tritrigs-heart-1.png


Polytrigs Challenge
===================

The polytrigs were a challenge because the pieces can overlap if we’re
not careful.  With physical puzzles, it’s not a problem: either the
piece fits, or it doesn’t.  With virtual polysticks, we have to keep
track of the intersections.

Square-grid polysticks have simple intersections: either an
intersection is occupied or not.

.. image:: images/g4g10/one-sided-tritrigs-chevron-8x1.png

The triangular-grid polysticks have more complex intersections:
multiple pieces can occupy an intersection simultaneously, as you can
see in two different ways above.  I had to devise a way to keep track
of which pieces can and can’t use an intersection together.

This is at least part the subject of the paper I’m writing as my
contribution to the gift exchange book.


Polytwigs
=========

.. image:: images/twigs/hexatwigs-triangle.png

After polytrigs, I considered the hexagonal-grid polysticks, which I
named “polytwigs” (because individually the pieces look like little
branching twigs). They were much easier to implement than the
triangular-grid polytrigs, lacking any intersection constraints at
all.  *[Above is the hexatwigs triangle.]*

The hexagonal-grid polytwigs are actually a restricted subset of the
triangular-grid polytrigs (both sets will fit on the triangular grid).

I couldn’t find any prior mention of hexagonal-grid polysticks.  But
it turns out that even they have been explored.  I received email from
Colin F. Brown, a puzzle enthusiast from England, who shared his work
from the 1970s on hexagonal-grid polysticks, including the
quasi-connected form.  In fact, he did some very early work on
square-, triangular-, and hexagonal-grid polysticks in general.
Unfortunately he never published before now.

*[Below is Mr. Brown’s pentatwigs trefoil design.  Note that it is
composed of 3 congruent shapes.]*

.. image:: images/twigs/pentatwigs-trefoil.png

*[Omitted from the talk due to time constraints:]*

Mr. Brown was also greatly influenced by Martin Gardner’s `Scientific
American` columns and books.  He eloquently wrote,

    Martin Gardner served up the starter, the main course and the
    dessert, and, ten times out of ten, something to nibble at later.
    For me, he will always be the father of recreational mathematics.


Evolving Algorithms
===================

*[Omitted from the talk due to time constraints:]*

The great thing about the Python programming language is that it makes
turning ideas into working computer programs easy and quick.
Python’s only downside is that the resulting programs are slow to run,
which really hurts when solving larger puzzles.  But last month I
discovered an Exact Cover solver backend written as a C extension to
Python, which I’ve been adapting to Polyform Puzzler, soon to be
published.  This means that Polyform Puzzler will solve puzzles at
lightning speed!  It will be the best of both worlds.


X!
====

In preparation for this 10th Gathering, I designed and solved some new
puzzles that match the “X” theme.  `All of these and more are now
available on the Polyform Puzzler site. <g4gX.html>`_

Here’s an X formed from the polyominoes of order 2 through 5:

.. image:: images/ominoes/polyominoes-2345-x-1.png

The one-sided polyiamonds of order 1 through 5 (looks a bit like a
“Primrose X”):

.. image:: images/iamonds/one-sided-polyiamonds-12345-x-1.png

The one-sided polyhexes of order 1 through 4:

.. image:: images/hexes/one-sided-polyhexes-1234-x-1.png

The polycubes of order 1 through 5 (featuring a script “x” on the
face):

.. list-table::
   :class: borderless

   * - .. image:: images/cubes/polycubes-12345-x-5.png

     - .. figure:: images/cubes/polycubes-12345-x-5-small.jpg
          :target: images/cubes/polycubes-12345-x-5.jpg

          Built with `Kadon's Super Deluxe Quintillions`_ and `Poly-4
          Supplement`_.  Click for the full-size image.

.. _Poly-4 Supplement: http://www.gamepuzzles.com/poly4.htm

The one-sided tetrasticks:

.. image:: images/sticks/one-sided-tetrasticks-x-1.png

The hexatwigs:

.. image:: images/twigs/hexatwigs-x-6.png

And finally, the one-sided polytrigs of order 1 through 3:

.. image:: images/trigs/one-sided-polytrigs-123-x-1.png


Conclusion
==========

I would love to have more correspondents!  If you have polyform puzzle
ideas you’d like to share with the world, `please write to me
<mailto:goodger@python.org>`__.

Thanks for reading about one of my obsessions.

| David Goodger
| goodger@python.org
