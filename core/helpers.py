# these should be popped to different modules eventually

# make me asynchronous!
def remote_execute(node, id, task_name):
    import execnet
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
                task_module = __import__('tasks.%s' % task_name, fromlist=['tasks'])
                ch = gw.remote_exec(task_module)
                return ch.receive()
            except ImportError:
                print 'dirt: Task', task_name, 'not found'
                return None
        else:
            print 'dirt: Error connecting with host', hostname
            return None
    except execnet.gateway.HostNotFound:
        print 'dirt: Host', hostname, 'not responding'
        return None

# put in config file
couchdb_host = 'http://localhost:5984'
couchdb_dbname = 'dirt-kanso'

def connect_to_db(host=couchdb_host, dbname=couchdb_dbname):
    import couchdb
    couch = couchdb.Server(couchdb_host)
    try:
        if couch.version() < '1.1.0':
            print 'dirt: couchdb version >= 1.1.0 required'
            sys.exit(1)
        db = couch[couchdb_dbname]
    except Exception:
        print 'dirt: error connecting to database'
        sys.exit(1)
    print 'dirt: connected to db at %s/%s' % (couchdb_host, couchdb_dbname)
    return db

def node_recon(nodes, db, interactive=True):
    import execnet
    import dbi
    # move to settings.py
    node_enable_default = True
    node_password_default = 'pw123'

    hostnames, nodedocs = dbi.get_nodes(db)
    from tasks import system_info
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

