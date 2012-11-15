# load balancing is implemented with generators that yield node
# couchdb documents

import execnet
import time

def round_robin(db):
    '''generates documents of nodes available for execution in a simple
    round-robin fashion. re-gets the node list from the db each time
    around.'''
    while(True):
        nodes = db.get_nodes()
        for node in nodes:
            if nodes[node]['enabled']:
                max_alloc = nodes[node]['sys_info']['cpu_count']
                if 'alloc' not in nodes[node] or len(nodes[node]['alloc']) < max_alloc:
                    yield nodes[node]
        time.sleep(1)

def load(db, margin=0.9, wait=20):
    '''round-robin using up to n cpus depending on current load'''
    def get_load(hostname):
        try:
            load_module = __import__('dirt.tasks.load', fromlist=['dirt.tasks'])
            gw = execnet.makegateway('ssh=%s' % hostname)
            ch = gw.remote_exec(load_module)
            return ch.receive()['load']
        except Exception:
            return None

    while(True):
        nodes = db.get_nodes()
        for node in nodes:
            if nodes[node]['enabled']:
                hostname = nodes[node]['fqdn']
                try:
                    ncpus = nodes[node]['sys_info']['cpu_count']
                    if get_load(hostname) < ncpus - margin:
                        if 'alloc' not in nodes[node] or len(nodes[node]['alloc']) < ncpus:
                            yield nodes[node]
                except Exception:
                    print 'Error connecting with host %s' % hostname
                    db.disable_node(hostname)
        time.sleep(wait)

