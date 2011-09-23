.. dirt documentation master file, created by
   sphinx-quickstart on Sun Sep  4 01:57:36 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Introduction
============
dirt is a Python and `kanso <http://kansojs.org/>`_ (CouchApp) application for oversight and tracking of remotely-executed jobs.

Source code is available at http://github.com/mastbaum/dirt.

Quick Start Guide
-----------------
Want to see dirt in action, fast?

First, set up a passphrase-less ssh key to localhost. Then do this::

    $ cd dirt && python setup.py install
    $ dirt create myproject
    $ cd myproject/web && kanso push myproject && kanso pushdata http://localhost:5984/myproject test_data.json && cd ..
    $ dirt updatenodes localhost
    $ dirt serve

Visit the URL ``kanso push`` gave you and watch the results roll in.

Installation
------------
``dirt`` is packaged for easy installation with ``setuptools``::

    $ git clone git://github.com/mastbaum/dirt.git
    $ cd dirt
    $ python setup.py install

Documentation
=============

.. toctree::
   :maxdepth: 2

   intro
   basic
   getting_started
   core
   core_tasks

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

