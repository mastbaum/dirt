tasks API
=========

Tasks to be run on remote hosts are defined as Python modules. Their structure is flexible, but when ``__name__ == '__channelexec__'``, they must return a dictionary containing at least a boolean ``'success'``.

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
        return execute()

    if __name__ == '__main__':
        print execute()

dirt itself contains a minimum of tasks -- only those needed to set up the remote execution environment. More interesting tasks are implemented in derivative projects.

tasks.heartbeat
---------------
Returns the minimal dictionary: ``{'success': True}``.

.. automodule:: tasks.heartbeat
   :members:

tasks.system_info
-----------------
Returns useful system information from os, sys, and socket.

.. automodule:: tasks.system_info
   :members:

tasks.ping
----------
A special task that does not return a dictionary, only a boolean. Used internally by dirt to confirm a node is accepting connections before sending it a task.

.. automodule:: tasks.ping
   :members:

