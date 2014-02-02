.. image:: https://travis-ci.org/nigelsmall/jsonstream.png?branch=master
   :target: https://travis-ci.org/nigelsmall/jsonstream


==========
JSONStream
==========

*JSONStream* is a JSON parser specifically designed to incrementally parse
large JSON documents in a single pass without loading the entire document into
memory.


Installation
============

JSONStream is hosted on PyPI and so to install, simply use ``pip``::

    pip install jsonstream


Quick Start
===========

::

    >>> from jsonstream import JSONStream
    >>> list(JSONStream(['["hello", "world"]']))
    [((), []), ((0,), 'hello'), ((1,), 'world')]


Further Reading
===============

...
