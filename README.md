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

Installation
------------
**Dependencies**

1. Apache CouchDB >= 1.1.0 (http://couchdb.apache.org)
2. kanso (http://kansojs.org)
3. execnet (Python module)
4. jsonrpclib (Python module)

**To install,**

1. Modify settings in web/kanso.json to match your environment
2. Push kanso CouchApp to the server:

    $ cd web && kanso push dirt

3. Install passphrase-less SSH keys on slave nodes
4. Add slave nodes to database:

    $ ./dirt updatenodes host1.example.com host2.otherplace.net (...)

5. Start dirt server:

    $ ./dirt serve

6. Add records to the database via JSON-RPC or `kanso pushdata`, with task names matching Python modules in the tasks directory:

<pre>
$ curl -X PUT -d @foo.json server:port/add_record
</pre>

With `foo.json`:
<pre>
[
    {
        "_id": "r123",
        "type": "record",
        "description": "this is revision one two three",
        "created": 1315347385
    },
    {
        "_id": "2e3dabbff38ca7f6fa05c5a0cbbc95a4",
        "type": "task",
        "record_id": "r123",
        "name": "system_info",
        "platform": "linux",
        "created": 1315347385
    },
    {
        "_id": "2e3dabbff38ca7f6fa05c5a0cbbc9858",
        "type": "task",
        "record_id": "r123",
        "name": "heartbeat",
        "platform": "linux",
        "created": 1315347385
    }
]
</pre>

Then, check the results in your web browser at the URL provided by `kanso push`.
