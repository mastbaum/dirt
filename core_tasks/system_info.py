def execute():
    '''get some basic system information'''
    import sys
    import os
    import socket
    results = {}
    results['success'] = True
    results['platform'] = sys.platform
    results['version_info'] = sys.version_info
    results['pythonpath'] = sys.path
    results['path'] = os.getenv('PATH')
    results['hostname'] = socket.gethostname()
    try:
        results['fqdn'] = socket.getfqdn()
        results['ip'] = socket.gethostbyname(socket.getfqdn())
    except socket.gaierror:
        results['fqdn'] = 'unknown'
        results['success'] = False
    return results

if __name__ == '__channelexec__':
    results = execute()
    channel.send(results)

if __name__ == '__main__':
    print execute()

