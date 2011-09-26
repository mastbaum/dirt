Document Model
==============
The fundamental objects in dirt projects are "records" and "tasks." A record might be a code revision or a data set, on which you wish to perform several operations (like compiling or running some unit tests). Tasks must be associated with one and only one record.

Records and Tasks
-----------------
Records (representing a code revision, data file, etc.) and the tasks associated with them are expressed in JavaScript Object Notation (JSON). A record document (in the CouchDB sense) looks like this::

    {
        "_id": "r123",
        "type": "record",
        "description": "this is revision one two three",
        "created": 1315347385
    }

A task ("example") associated with this document ("r123") looks like this::

    {
        "_id": "2e3dabbff38ca7f6fa05c5a0cbbc95a4",
        "type": "task",
        "record_id": "r123",
        "name": "example",
        "platform": "linux",
        "created": 1315347385
    }

The ``name`` field is simply the name of a Python module in the ``tasks`` directory. A directory ``tasks/examples`` is included with new projects.

The structure of the Task modules is flexible, but when ``__name__ == '__channelexec__'``, they must return a dictionary containing at least a boolean ``'success'``.

The recommended structure is::

    def execute():
        '''docstring'''
        # do things
        success = False
        sum = 2 + 2
        if sum == 4:
            success = True
        return {'success': success, 'sum': sum}

    if __name__ == '__channelexec__':
        channel.send(execute())

    if __name__ == '__main__':
        print execute()

Getting attachments from tasks
------------------------------
Tasks can also return attachments. Simply include in the "results" dictionary another special key "attachments," which contains a list like this::

    'attachments': [
        {'filename': <local filename>, 'contents': <stringified contents of file>, 'link_name': <name to appear on web page>},
        {...},
        {...},
        ...
    ]

If ``link_name`` is specified, a link is provided to that attachment on the results page.

Passing arguments to tasks
--------------------------
It is also possible to pass keyword arguments to your task (for example, which revision number to check out). The basic syntax for the task module is::

    def execute(foo, bar):
        return {'success': True, 'foo': foo, 'bar': bar}

    if __name__ == '__channelexec__':
        kwargs = channel.receive()
        results = execute(**kwargs)
        channel.send(results)

The task document must then include all needed arguments in a special key ``'kwargs'``, e.g.::

    'kwargs': {'foo': 42, 'bar': 'baz'}

An example is given in the ``tasks/examples`` subdirectory of a new project.

Setting system requirements for tasks
-------------------------------------
Some tasks may require certain conditions on the slave node. For example, a compilation test may need to be run on several platforms. The node information stored by dirt is available to tasks through a simple query API.

To set a requirement for a task, add the special key ``requires`` to the task document. ``requires`` must be a list of strings invoking one of the following query operators::

    is
    not
    in
    not_in

Example::

    {
        "type": "task",
        "requires": ["architecture is x86_64", "G4INSTALL in environ"],
        ...
    }

Available keys
``````````````
``success`` (boolean)
  True if node was successfully added to the database

``cpu_count`` (int)
  Number of CPUs available for running dirt tasks. dirt will run up to ``cpu_count`` jobs simultaneously on a node.

  From ``multiprocessing.cpu_count``

``platform`` (string)
  Long description of the node platform, e.g. "Linux-2.6.32-33-server-x86_64-with-Ubuntu-10.04-lucid"

  From ``platform.platform()``

``architecture`` (string)
  Descriptor of node architecture, e.g. 'x86_64'

  From ``platform.machine()``

``environ`` (string-string map)
  A dictionary of environment variables on the node, e.g. {'FOO': '/bar'}

  From ``os.environ.data``

``path`` (list of strings)
  A list of all paths in the $PATH on the node, e.g. ['/bin', '/usr/bin']

  From ``os.environ['PATH'].split(os.path.pathsep)``

``version_info`` (string)
  Python version on the node, e.g. '2.6.5.final.0'

  From ``sys.version_info``

``pythonpath`` (list of strings)
  Python path on the node

  From ``sys.path``

``hostname`` (string)
  Short hostname of the system, e.g. 'node1'. Not used by dirt.

  From ``socket.gethostname()``

``fqdn`` (string)
  Fully-qualified domain name of the node, e.g. 'node1.site.org'

  From ``socket.getfqdn``

``ip`` (string)
  Reverse-mapped IP, as seen by the node, e.g. '10.20.30.40'. Not used by dirt.

  From ``socket.gethostbyname(socket.getfqdn())``

