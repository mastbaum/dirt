#/usr/bin/env python

# DIRT.
#
# Andy Mastbaum (amastbaum@gmail.com), August 2011

import couchdb
import execnet
import sys

# put in config file
couchdb_host = 'http://localhost:5984'
couchdb_dbname = 'dirt-kanso'
nodes = ['localhost']
node_enable_default = True
node_password_default = 'pw123'
interactive = True

# this should be a couchdb view
def get_nodes(db):
    nodedocs = []
    hostnames = []
    for id in db:
        try:
            if db[id]['type'] == 'slave':
                print db[id]
                nodedocs.append(db[id])
                hostnames.append(db[id]['hostname'])
        except KeyError:
            pass
    return hostnames, nodedocs

def node_recon(nodes, db):
    hostnames, nodedocs = get_nodes(db)
    from tasks import system_info
    for node in nodes:
        gw = execnet.makegateway('ssh=%s' % node)
        ch = gw.remote_exec(system_info)
        sys_info = ch.receive()
        print '==', node, '='*30
        print sys_info
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
              

def main():
    print 'dirt is running...'

    # connect to db
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

    node_recon(nodes, db)

if __name__ == '__main__':
    # some arguments?
    main()

