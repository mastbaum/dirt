Getting Started
===============

Stories
-------

1. You want to run a series of compilation and unit tests on each revision of your software. You'd like to store the results in a database, and easily see things like all the tests on revision X or the history of unit test Y through the revisions.

2. Your science experiment regularly produces data files as output. You need to perform some analyses on each file, and store the results.

dirt is designed to make such tasks trivial. Basically, you have a fundamental data set -- a code revision, a data file, etc., called a "record" -- and a number of functions that you want to operate on this data set. With dirt, you simply:

1. Express your tasks as Python modules
2. Add a record to the database
3. Add tasks associated with that record to the database

and dirt will automatically run them and put results in a database, doling out tasks to as many computers as you make available to it.

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

The ``name`` field is simply the name of a Python module in the ``tasks`` directory. ``example.py`` is included with new projects.

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

Attachments
```````````
Tasks can also return attachments. Simply include in the "results" dictionary another special key "attachments," which contains a list like this::

    'attachments': [
        {'filename': <local filename>, 'contents': <stringified contents of file>, 'link_name': <name to appear on web page>},
        {...},
        {...},
        ...
    ]

If ``link_name`` is specified, a link is provided to that attachment on the results page.

Arguments
`````````
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

Starting your project: an example
---------------------------------
For an example, let's build a minimal build testing system.

To see a complete CI system implemented with dirt, check out `pytunia <http://github.com/mastbaum/pytunia>`_.

Starting the project
````````````````````

Use ``dirt create`` to start a project::

    $ dirt create builder
    dirt v0.1
    Created new dirt project in builder
    $ cd builder
    $ ls
    README.md  settings.py  tasks  web

Describe your project in ``README.md``, and tweak settings as necessary in ``settings.py``::

    $ vim README.md
    $ vim settings.py
 
Push the web application to your CouchDB server::

    $ cd web && kanso push builder

If you're not running the server on localhost, replace "builder" with the full database URL.

Visit the URL it prints, and you should see your project's empty Overview page.

Adding remote execution nodes
`````````````````````````````

You'll now want to give the builder a list of computers it can run on. Currently, these must be accessible to the server via SSH (work is in progress for ways of getting around firewalls). You'll want to set up passphrase-less SSH keys so that the user running the server can log into each node without a password. Once that is done, add the nodes by their full hostname using ``dirt updatenodes host1 host2 ...``. For this example, let's just use the server as a node::

    $ dirt updatenodes localhost

Adding tasks
````````````

To test compilation, we'll need to express the build process in a Python module. For this example, we'll grab and compile a C++ "hello, world" from github. Consider the following Python module::

    import os
    import subprocess

    def system(cmd, wd=None):
        '''a wrapper for subprocess.call, which executes cmd in working directory
        wd in a bash shell, returning the exit code.'''
        if wd:
            cmd = ('cd %s && ' % wd) + cmd
        return subprocess.call([cmd], executable='/bin/bash', shell=True)

    def execute():
        results = {'success': True, 'attachments': []}

        # work in some directory
        wd = 'builder_stuff'
        if not os.path.exists(wd):
            os.mkdir(wd)

        # construct command and check out with git
        url = 'https://github.com/leachim6/hello-world.git'
        cmd = 'git clone ' + url
        ret = system(cmd, wd)

        # if something has gone wrong, we can return a reason
        if ret != 0:
            results['success'] = False
            results['reason'] = 'git clone failed'
            return results

        cmd = 'cd hello-world/c && g++ -v -o hello c++.cpp &> build.log'
        ret = system(cmd, wd)

        if ret != 0:
            results['success'] = False
            results['reason'] = 'g++ failed'
            return results

        # attach build log
        logfile = {}
        with open(wd + '/hello-world/c/build.log','r') as f:
            logfile = {'filename': 'build.log', 'contents': f.read(), 'link_name': 'Build log'}

        results['attachments'].append(logfile)

        return results

    if __name__ == '__channelexec__':
        results = execute()
        channel.send(results)

    if __name__ == '__main__':
        print execute()

This will try to clone a git repository and compile some c++ code. If it works, you get the build log as an attachment. If it fails, your results tell you which step failed.

Put this file (or your version of it) in the ``tasks`` subdirectory, called ``compile_hello.py``.

Starting the server
```````````````````

From your project directory, just run::

    $ dirt serve

It is now listening for new tasks.

Adding records and tasks to the database
````````````````````````````````````````

Records and the tasks that go with them are added directly to the CouchDB database. There are lots of ways of pushing data to couch, including ``curl -X PUT ...``, ``kanso pushdata ...``, any language's couchdb module, etc.

For a real build tester, the record and task documents for each revision should be constructed and posted to the server by some kind of post-commit hook in your version control system. For this example, we will just construct the JSON documents manually. Save the following as r123.json (pretending this code has something to do with revision 123)::

    {
        "docs": [
            {
                "_id": "r123",
                "type": "record",
                "description": "this is revision one two three",
                "created": 1315347385
            },
            {
                "_id": "2e3dabbff38ca7f6fa05c5a0cbbc95a5",
                "type": "task",
                "record_id": "r123",
                "name": "compile_hello",
                "platform": "linux",
                "created": 1315347385
            }
        ]
    }

This tells dirt to execute the ``compile_hello`` module (associated with r123) on the next available node (localhost, for us).

To put this in the database::

    curl -X POST -H "Content-Type: application/json" -d @r123.json http://localhost:5984/builder/_bulk_docs

(assuming we're using the couchdb server on localhost).

Watch the magic
```````````````

The running dirt program should send the ``compile_hello`` task off to localhost, with output like this::

    $ dirt serve
    dirt v0.1
    Sep 07 12:57:20 neutralino myproject : dirt is running...
    Sep 07 12:57:20 neutralino myproject : Connected to db at http://localhost:5984/myproject
    Sep 07 12:57:20 neutralino myproject : 2e3dabbff38ca7f6fa05c5a0cbbc95a5 -> localhost.localdomain
    Sep 07 12:57:22 neutralino myproject : Task 2e3dabbff38ca7f6fa05c5a0cbbc95a5 pushed to db
    Sep 07 12:57:22 neutralino myproject : Task 2e3dabbff38ca7f6fa05c5a0cbbc95a5: file build.log attached

Now, go the URL ``kanso push`` gave you (e.g. http://localhost:5984/myproject/_design/myproject/_rewrite), and see the results in the web interface. Clicking on r123 brings you to the record summary page. You can see the build log and raw results dictionary from the "Results" links. Clicking the task name brings you to the task history page -- the outcome of all ``compile_hello`` tasks ever run.

Moving on
`````````

Now, experiment with writing your own task modules. Consider writing code to generate and POST the record and task JSON, as would be called in a post-commit hook. Tinker with the web interface either cosmetically (CSS is in web/static/css) or by writing your own CouchDB views and lists to do special things with the results dictionary.

If you find a bug or have a suggestion for dirt, post an issue on the [github page](http://github.com/mastbaum/dirt).

