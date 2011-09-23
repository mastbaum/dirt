Basic Usage
===========

Command-line usage
------------------

dirt can be run with one of three subcommands.

Start a new dirt project::

    $ dirt create projectname [database name]

The database name is the same as the project name by default.

Update stored system information on each host, adding the host to the database if necessary::

    $ dirt updatenodes [host1.example.com] [host2.othersite.org] ...

Run the dirt remote execution server, which will dole out unfinished tasks in the database to available execution hosts::

    $ dirt serve

Using dirt as a module
----------------------

dirt and its submodules can also be used in Python.

To get a list of nodes::

    >>> from dirt.core import dbi
    >>> db = dbi.DirtCouchDB('http://localhost:5984', 'dirt')
    Sep 04 03:17:44 neutralino dirt : Connected to db at http://localhost:5984/dirt
    >>> for fqdn in db.get_nodes():
    ..:    print fqdn
    node1.example.com
    node2.othersite.org

Use ``execnet`` to run a task on a node::

    >>> host = 'localhost'
    >>> import execnet
    >>> from tasks.examples import simple
    >>> gw = execnet.makegateway('ssh=%s' % host)
    >>> ch = gw.remote_exec(simple)
    >>> ch.receive()
    {'success': True}    

