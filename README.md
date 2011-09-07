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

0. Python 2.7
1. Apache CouchDB >= 1.1.0 (http://couchdb.apache.org)
2. kanso (http://kansojs.org)
3. execnet (Python module)
4. jsonrpclib (Python module)

### Dependencies (execution nodes) ###

0. Python 2.7
1. Anything referenced in your task module not available in the Python Standard Library

### Installation ###

Before starting, ensure that the path containing the dirt package in in your `$PYTHONPATH` and the dirt directory in in your `$PATH`.

1. `cd` to directory where project should live
2. `dirt create <projectname> [database name]` (database name defaults to project name)
3. `cd <projectname>`
4. Describe your project in `README.md`
5. `cd web && kanso push <database name>`. Take a look at the URL it returns.

### Next Steps ###

See the [dirt documentation](http://readthedocs.org/docs/dirt) for a getting-started guide.

About
-----
### Database Backend ###
dirt uses CouchDB for its database. Couch was chosen for interoperability with various other systems, but the dirt data model is easily normalized and trivially reimplemented in traditional SQL.

### Web Frontend ###
Since Couch is used for the DB, it made sense to write the frontend using CouchDB views. The frontend of dirt is written as a kanso application, which provides some extra magic on top of the more typical couchapp.

### Remote Execution ###
For security reasons, the code that actually gets executed by remote hosts is stored in actual Python files on the master server. Having it in the database would be cool, but more prone to evil.

Tasks are registered by name, and doled out to remote hosts for execution as their names appear attached to records in the database. For example, a build testing system might look like this:

* record: rev1234
  * task: build(linux) -> Python code for "build" is run on a host with platform "linux"
  * task: build(osx)   -> Python code for "build" is run on a host with platform "osx"
  * task: cxxtest      -> Python code for cxxtest is run on some host

Tasks are run on remote hosts via execnet. Task code is shipped over and executed on the remote host using a secure SSH pipe provided by the execnet package. Clients take no action, and need only an SSH key, a Python interpreter, and any dependencies not included with the task code.

