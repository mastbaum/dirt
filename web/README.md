dirt kanso app
==============

dirt uses CouchDB as a database backend for system integration reasons -- dirt data is well-structured and well-suited for traditional SQL.

Since it is already included and eliminates further dependencies, dirt uses CouchDB as a web framework for the front-end. Since CouchApps are sort of a pain to make, I used kanso (http://http://kansojs.org/) to do the heavy lifting.

Views and whatnot
-----------------

There are three basic ways the data is presented:

1. Overview (list: index, template: index.html): history of records with a "percent awesome" bar

2. Record Summary (show: record, template: record.html): All tasks associated with a record

3. Task Summary (list: task, template: task.html): History of success/failure of a task over the records

Locations
---------
* View functions for index and tasks are in lib/views.js
* List functions for index and task are in lib/lists.js
* Show function for record summary is in lib/shows.js
* All templates are in templates/
 
