# these should be popped to different modules eventually

import settings
from log import log

def remote_execute(db, node, id, taskid, taskname):
    import execnet
    import dbi
    # have to import * due to execnet introspection :(
    from tasks import *
    hostname = node['hostname']
    try:
        # first, check if node is alive
        gw = execnet.makegateway('ssh=%s' % hostname)
        ch = gw.remote_exec(heartbeat)
        if ch.receive():
            try:
                # boy, dynamic importing sure is complicated.
                task_module = __import__('tasks.%s' % taskname, fromlist=['tasks'])
                ch = gw.remote_exec(task_module)
                push_args = {'id': id, 'taskid': taskid}
                ch.setcallback(db.push_results, kwargs=push_args)
            except ImportError:
                log.write('Task %s not found' % taskname)
                return None
        else:
            log.write('Error connecting with host %s' % hostname)
            return None
    except execnet.gateway.HostNotFound:
        log.write('Host %s not responding' % hostname)
        return None

def node_recon(nodes, db, interactive=True):
    import execnet
    from tasks import system_info
    hostnames, nodedocs = db.get_nodes()
    for node in nodes:
        try:
            gw = execnet.makegateway('ssh=%s' % node)
        except execnet.HostNotFound:
            log.write('Host not found: %s' % node)
            continue
        log.write('Connected to host' % node)
        ch = gw.remote_exec(system_info)
        sys_info = ch.receive()

        # update the db
        if sys_info['hostname'] in hostnames:
            d = nodedocs[hostnames.index(sys_info['hostname'])]
            d['sys_info'] = sys_info
        else:
            d = {'type': 'slave', 'hostname': sys_info['hostname'], 'sys_info': sys_info}
            if interactive:
                log.write('Adding new node %s to database' % d['hostname'])
                enable = raw_input('Enable node? [True|False] ')
                if enable == 'True':
                    d['enabled'] = True
                else:
                    d['enabled'] = False
                pw = raw_input('Node password? ')
                d['password'] = pw
            else:
                d['enabled'] = node_enable_default
                d['password'] = node_password_default
        db.save(d)

