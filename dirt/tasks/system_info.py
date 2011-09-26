def execute():
    '''get some basic system information'''
    import sys
    import os
    import socket
    import platform
    import multiprocessing
    results = {}
    results['success'] = True
    results['cpu_count'] = multiprocessing.cpu_count()
    results['platform'] = platform.platform()
    results['architecture'] = platform.machine()
    results['environ'] = os.environ.data
    results['path'] = os.environ['PATH'].split(os.path.pathsep)
    results['version_info'] = sys.version_info
    results['pythonpath'] = sys.path
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

