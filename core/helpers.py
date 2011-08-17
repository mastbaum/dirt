# these should be popped to different modules eventually

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

# this should be a couchdb view
def get_nodes(db):
    nodedocs = []
    hostnames = []
    for id in db:
        try:
            if db[id]['type'] == 'slave':
                nodedocs.append(db[id])
                hostnames.append(db[id]['hostname'])
        except KeyError:
            pass
    return hostnames, nodedocs

def node_recon(nodes, db, interactive=True):
    import execnet
    # move to settings.py
    node_enable_default = True
    node_password_default = 'pw123'

    hostnames, nodedocs = get_nodes(db)
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

def system(cmd, wd=None):
    '''a wrapper for subprocess.call, which executes cmd in working directory
    wd in a bash shell, returning the exit code.'''
    if wd:
        cmd = ('cd %s && ' % wd) + cmd
    if debug:
        print cmd
        return 0
    return subprocess.call([cmd], executable='/bin/bash', shell=True)

