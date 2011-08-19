# load balancing is implemented with generators that yield slave ("node")
# couchdb documents

def round_robin(db):
    '''generates documents of nodes available for execution in a simple
    round-robin fashion. re-gets the node list from the db each time
    around.'''
    import core.helpers
    import core.dbi
    while(True):
        hostnames, nodedocs = core.dbi.get_nodes(db)
        for node in nodedocs:
            if node['enabled'] and not node['active']:
                yield node

