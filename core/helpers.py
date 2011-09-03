# these should be popped to different modules eventually

import settings
from log import log

def remote_execute(db, node, id, taskid, taskname):
    import execnet
    hostname = node['hostname']
    try:
        # first, check if node is alive
        heartbeat_module = __import__('tasks.heartbeat', fromlist=['tasks'])
        gw = execnet.makegateway('ssh=%s' % hostname)
        ch = gw.remote_exec(heartbeat_module)
        if ch.receive():
            try:
                task_module = __import__('tasks.%s' % taskname, fromlist=['tasks'])
                ch = gw.remote_exec(task_module)
                # use lambda to provide arguments to callback
                push_args = {'id': id, 'taskid': taskid}
                ch.setcallback(callback = lambda(results): db.push_results(results, **push_args))
            except ImportError:
                log.write('Task %s not found' % taskname)
                return False
        else:
            log.write('Error connecting with host %s' % hostname)
            db.disable_node(hostname)
            return None
    except execnet.gateway.HostNotFound:
        log.write('Host %s not responding' % hostname)
        db.disable_node(hostname)
        return False
    return True

def node_recon(nodelist, db, interactive=True):
    '''grab system information from a list of hosts and create or update
    slave nodes' db entries.
    '''
    import execnet
    from tasks import system_info
    nodes = db.get_nodes()
    for node in nodelist:
        log.write('Connecting to host %s' % node)
        try:
            gw = execnet.makegateway('ssh=%s' % node)
        except execnet.HostNotFound:
            log.write('Host not found: %s' % node)
            continue
        log.write('Connected to host %s' % node)

        ch = gw.remote_exec(system_info)
        sys_info = ch.receive()

        # update the db
        if sys_info['hostname'] in nodes:
            d = nodes[sys_info['hostname']]
            d['sys_info'] = sys_info
            d['enabled'] = True
        else:
            d = {'type': 'slave', 'hostname': sys_info['hostname'], 'sys_info': sys_info}
            log.write('Adding new node %(hostname)s to database' % d)
            if interactive:
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

