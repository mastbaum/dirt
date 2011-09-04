Basic Usage
===========

Command-line usage
------------------

dirt can be run with one of two subcommands.

Run the dirt remote execution server, which will dole out unfinished tasks in the database to available execution hosts::

    $ ./dirt serve

Update stored system information on each host, adding the host to the database if necessary::

    $ ./dirt updatenodes [host1] [host2] ...

Using dirt as a module
----------------------

dirt and its submodules can also be used in Python.

To get a list of nodes::

    >>> from core import dbi
    >>> db = dbi.DirtCouchDB('http://localhost:5984', 'dirt')
    Sep 04 03:17:44 neutralino dirt : Connected to db at http://localhost:5984/dirt
    >>> for fqdn in db.get_nodes():
    ..:    print fqdn
    node1
    node2

Use ``execnet`` to run a task on a node::

    >>> host = 'localhost'
    >>> import execnet
    >>> from tasks import heartbeat
    >>> gw = execnet.makegateway('ssh=%s' % host)
    >>> ch = gw.remote_exec(heartbeat)
    >>> ch.receive()
    {'success': True}    

