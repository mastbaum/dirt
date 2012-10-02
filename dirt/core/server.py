import sys
import socket
import signal

import settings

from dirt.core import dbi
from dirt.core import remote
from dirt.core import load_balance

from dirt.core.db import db
from dirt.core.log import log

def signal_handler(signal, frame):
    '''handle SIGINTs gracefully, clearing running tasks from the db'''
    log.write('Caught SIGINT (Ctrl-C), Exiting.')

    # clear any currently-running tasks from db
    log.write('Clearing running tasks from database')
    nodes = db.get_nodes()
    for node in nodes:
        if 'alloc' in nodes[node]:
            for i in range(len(nodes[node]['alloc'])):
                # only clear tasks from this master
                alloc = nodes[node]['alloc'][i]
                if alloc['master'] == socket.getfqdn():
                    doc = db[alloc['task']]
                    if 'started' in doc:
                        del doc['started']
                    if 'node' in doc:
                        del doc['node']
                    db.save(doc)
                    node_doc = db[nodes[node]['_id']]
                    node_doc['alloc'].pop(i)
                    db.save(node_doc)
    sys.exit(0)

def serve_forever():
    '''when new tasks show up in the database, pair them up with the next
    available node for execution.
    '''
    signal.signal(signal.SIGINT, signal_handler)
    log.write('dirt is running...')

    nodes = settings.load_balancer(db)
    tasks = db.get_tasks()

    for id in tasks:
        task_status = 'new'
        while task_status == 'new' or task_status == 'retry':
            node = nodes.next()
            if dbi.check_requirements(db, id, node):
                log.write('%s -> %s' % (id, node['fqdn']))
                task_status = remote.remote_execute(db, node, id)
                if task_status == 'abort':
                    log.write('Task %s aborted' % id)
            else:
                doc = db[id]
                if 'nodes_tried' in doc:
                    doc['nodes_tried'].append(node['fqdn'])
                else:
                    doc['nodes_tried'] = [node['fqdn']]
                db.save(doc)
                task_status = 'abort'

