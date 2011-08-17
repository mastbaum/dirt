dirt
====
Overview
--------
dirt is a Python and kanso (CouchDB) application for oversight and tracking of remotely-executed jobs.

Users submit groups of tasks to perform on a data set (or whatever), those are added to a database, tasks are doled out to remote execution hosts, and results are stored in the DB and presented via a web page.

Possible uses include distributed build testing and automated distributed data processing.

Database Backend
----------------
dirt uses CouchDB for its database. Couch was chosen for interoperability with various other systems, but the dirt data model is easily normalized and trivially reimplemented in traditional SQL.

Web Frontend
------------
Since Couch is used for the DB, it made sense to write the frontend using CouchDB views. The frontend of dirt is written as a kanso application, which provides some extra magic on top of the more typical couchapp.

Remote Execution
----------------
For security reasons, the code that actually gets executed by remote hosts is stored in actual Python files on the master server. Having it in the database would be cool, but more prone to evil.

Tasks are registered by name, and doled out to remote hosts for execution as their names appear attached to records in the database. For example, a build testing system might look like this:

* record: rev1234
  * task: build(linux) -> Python code for "build" is run on a host with platform "linux"
  * task: build(osx)   -> Python code for "build" is run on a host with platform "osx"
  * task: cxxtest      -> Python code for cxxtest is run on some host

Tasks are run on remote hosts in one of two ways:

1. execnet: Task code is shipped over and executed on the remote host using a secure SSH pipe provided by the execnet package. Clients take no action, and need only an SSH key, a Python interpreter, and any dependencies not included with the task code.

2. JSON-RPC: A client script on the host pings the master server to request a task to process. This is useful for hosts behind firewalls, proxies, etc., which execnet cannot SSH to over the internet.

Customization
-------------
For now, hack it. Evetually config scripts will make this easy.

