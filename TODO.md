dirt To-do list
===============
to-do list
----------
* put it on github

dirt
----
* use callbacks for async core.helpers.remote_execute

tasks
-----
* instead of storing host id in the task sub-document, have the remote host stuff socket.getfqdn() into the results dictionary. to enforce, automatically, create a @dirt_task decorator

core.helpers
------------
* use callbacks for async remote_execute

core.dbi
--------
* DB superclass for abstraction of db system?
* dbi.DirtCouchDB.push_results: better exception handling
* dbi.DirtCouchDB.get_nodes: use slave_by_hostname view

web
---
* use/hack/implements kando Type.EmbedDictionary. currently tasks are {'tasks': [task1, task2, ...}. prefer {'tasks': {'task1': {task1}, 'task2': {task2}}}. maybe ditch validation on tasks field.

