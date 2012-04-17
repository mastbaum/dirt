core API
========

The ``dirt.core`` module contains all of dirt's internal functions.

dirt.core.create
----------------
Routine used to create the skeleton directory structure for a new project

.. automodule:: dirt.core.create
   :members:

dirt.core.dbi
-------------
dirt's interface to the CouchDB database. All db interactions happen through a shared instance of the ``DirtCouchDB`` class.

.. automodule:: dirt.core.dbi
   :members:

dirt.core.server
----------------
The main dirt server function

.. automodule:: dirt.core.server
   :members:

dirt.core.load_balance
----------------------
Load-balancing between nodes is achieved with Python generators that yield the next node on which to execute something.

.. automodule:: dirt.core.load_balance
   :members:

dirt.core.log
-------------
``dirt.core.log`` creates a singleton ``yelling.Log`` instance ``dirt.core.log.log``, used for log output throughout dirt.

.. automodule:: dirt.core.log
   :members:

dirt.core.yelling
-----------------
Logging is done with the ``yelling`` module, available at https://github.com/mastbaum/yelling.

All logging should happen through ``dirt.core.log.log``, which is a ``yelling`` Log object:

.. autoclass:: dirt.core.yelling.Log
   :members:

Other available ``yelling`` functions include:

.. automodule:: dirt.core.yelling
   :members:

