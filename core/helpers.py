# these should be popped to different modules eventually

import settings

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
                print 'dirt: Task', taskname, 'not found'
                return None
        else:
            print 'dirt: Error connecting with host', hostname
            return None
    except execnet.gateway.HostNotFound:
        print 'dirt: Host', hostname, 'not responding'
        return None

def node_recon(nodes, db, interactive=True):
    import execnet
    from tasks import system_info
    hostnames, nodedocs = db.get_nodes()
    for node in nodes:
        try:
            gw = execnet.makegateway('ssh=%s' % node)
        except execnet.HostNotFound:
            print 'dirt: host not found:', node
            continue
        print 'dirt: connected to host', node
        ch = gw.remote_exec(system_info)
        sys_info = ch.receive()

        # update the db
        if sys_info['hostname'] in hostnames:
            d = nodedocs[hostnames.index(sys_info['hostname'])]
            d['sys_info'] = sys_info
        else:
            d = {'type': 'slave', 'hostname': sys_info['hostname'], 'sys_info': sys_info}
            if interactive:
                print 'adding new node %s to database' % d['hostname']
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

