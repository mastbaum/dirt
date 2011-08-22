# load balancing is implemented with generators that yield slave ("node")
# couchdb documents

def round_robin(db):
    '''generates documents of nodes available for execution in a simple
    round-robin fashion. re-gets the node list from the db each time
    around.'''
    while(True):
        hostnames, nodedocs = db.get_nodes()
        for node in nodedocs:
            if node['enabled'] and not node['active']:
                yield node

