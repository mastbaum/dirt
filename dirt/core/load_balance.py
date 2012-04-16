# load balancing is implemented with generators that yield node
# couchdb documents

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

