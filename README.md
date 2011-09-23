dirt
====
Overview
--------
dirt is a Python and kanso (CouchDB) application for oversight and tracking of remotely-executed jobs.

Users submit groups of tasks to perform on a data set (or code revision, etc.) called a "record," those are added to a database, tasks are doled out to remote execution hosts, and results are stored in the DB and presented via a web page.

Possible uses include distributed build testing, continuous integration, and automated distributed data processing.

**Source code** is available on [github](http://github.com/mastbaum/dirt)

**Documentation** is available on [Read the Docs](http://readthedocs.org/docs/dirt)

Setting Up
----------
### Dependencies (server) ###

1. Apache CouchDB >= 1.1.0 on server (http://couchdb.apache.org)
2. kanso (http://kansojs.org)

### Dependencies (execution nodes) ###

0. Python >= 2.6
1. Anything referenced in your task module not available in the Python Standard Library

### Installation ###

First, install the dirt package:

    $ cd dirt
    $ python setup.py install

To start your dirt project, 

1. `dirt create <projectname> [database name]` (database name defaults to project name)
2. `cd <projectname>`
3. Describe your project in `README.md`
4. `cd web && kanso push <database name>`. Take a look at the URL it returns.

### Next Steps ###

See the [dirt documentation](http://readthedocs.org/docs/dirt) for a getting-started guide.

