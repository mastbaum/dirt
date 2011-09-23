def execute(cat, dog):
    '''A simple example task that just returns True.

    Tasks can look like anything, so long as they:

    1. Are a self-contained module. Nothing but this code will be shipped to
       remote hosts. Any dependencies must be properly set up on the other end.
    2. Put results in a dictionary containing at least a key 'success' with a
       boolean value.
    3. Send the results via ``channel.send(results)`` when the program is run
       with ``__name__ == '__channelexec__'``.

    If your task requires arguments, you can provide them by adding a key
    'kwargs' with a dictionary value to your task document. For example,
    a task document for this task (arguments) should contain::

        'kwargs': {'cat': 'meow', 'dog': 'woof'}

    which are passed through a channel.send and provided to execute().
    '''
    results = {'success': True, 'cat_sound': cat, 'dog_sound': dog}
    return results

if __name__ == '__channelexec__':
    kwargs = channel.receive()
    results = execute(**kwargs)
    channel.send(results)

if __name__ == '__main__':
    print execute()

