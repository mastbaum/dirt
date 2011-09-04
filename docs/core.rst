core API
========

The ``core`` module contains all of dirt's internal functions.

core.dbi
--------
dirt's interface to the CouchDB database. All db interactions happen through a shared instance of the ``DirtCouchDB`` class.

.. automodule:: core.dbi
   :members:

core.helpers
------------
Various helper functions

.. automodule:: core.helpers
   :members:

core.load_balance
-----------------
Load-balancing between nodes is achieved with Python generators that yield the next node on which to execute something.

.. automodule:: core.load_balance
   :members:

core.log
--------
``core.log`` creates a singleton ``yelling.Log`` instance ``core.log.log``, used for log output throughout dirt.

.. automodule:: core.log
   :members:

core.yelling
------------
Logging is done with the ``yelling`` module, available at https://github.com/mastbaum/yelling.

All logging should happen through ``core.log.log``, which is a ``yelling`` Log object:

.. autoclass:: core.yelling.Log
   :members:

Other available ``yelling`` functions include:

.. automodule:: core.yelling
   :members:
