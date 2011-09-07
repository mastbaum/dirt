def execute():
    '''An example task that returns an attachment.

    Tasks can look like anything, so long as they:

    1. Are a self-contained module. Nothing but this code will be shipped to
       remote hosts. Any dependencies must be properly set up on the other end.
    2. Put results in a dictionary containing at least a key 'success' with a
       boolean value.
    3. Send the results via ``channel.send(results)`` when the program is run
       with ``__name__ == '__channelexec__'``.

    In addition to 'success', there is a special key 'attachments' which must
    have the following form if used::

        'attachments': [
            {'filename': <local filename>, 'contents': <stringified contents of file>, 'link_name': <name to appear on web page>},
            {...},
            {...},
            ...
        ]

    If link_name is specified, a link is provided to that attachment on the results page.
    '''
    import os
    results = {'success': True, 'attachments': []}
    try:
        # attach /etc/hosts. this file must exist on the remote system, or
        # the test will fail
        with open('/etc/hosts') as f:
            file_attachment = {'filename': os.path.basename(f.name), 'contents': f.read(), 'link_name': 'Hosts file'}
            results['attachments'].append(file_attachment)
    except Exception:
        results['success'] = False

    return results

if __name__ == '__channelexec__':
    results = execute()
    channel.send(results)

if __name__ == '__main__':
    print execute()
    
