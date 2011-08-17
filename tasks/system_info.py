# no need to wrap these in classes, since we call the module as
# __channelexec__ anyway.

class SystemInfoTask():
    '''get some basic system information'''
    def __init__(self, name):
        self.name = name
        self.results = {}
    def execute(self):
        import sys
        import os
        import socket
        self.results['platform'] = sys.platform
        self.results['version_info'] = sys.version_info
        self.results['pythonpath'] = sys.path
        self.results['path'] = os.getenv('PATH')
        self.results['hostname'] = socket.gethostname()
        self.results['fqdn'] = socket.getfqdn()
        self.results['ip'] = socket.gethostbyname(socket.getfqdn())
        return self.results

if __name__ == '__channelexec__':
    sysinfo = SystemInfoTask('sysinfo')
    results = sysinfo.execute()
    channel.send(results)

if __name__ == '__main__':
    sysinfo = SystemInfoTask('sysinfo')
    results = sysinfo.execute()
    print results

