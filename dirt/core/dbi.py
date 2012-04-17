import sys
import time
import socket
import getpass
import couchdb

import settings
import dirt.core.yelling
from dirt.core.log import log

class DirtCouchDB():
    '''wrapper for ``couchdb`` that provides some additional dirt-specific
    functions.
    '''
    def __init__(self, host, dbname):
        couch = couchdb.Server(host)
        try:
            try:
                if couch.version() < '1.1.0':
                    log.write('Error: couchdb version >= 1.1.0 required')
                    sys.exit(1)
                self.db = couch[dbname]
            except couchdb.http.Unauthorized:
                print 'Authentication required for CouchDB database at', host + '/' + dbname
                couch.resource.credentials = (raw_input('Username: '), getpass.getpass('Password: '))
                if couch.version() < '1.1.0':
                    log.write('Error: couchdb version >= 1.1.0 required')
                    sys.exit(1)
                self.db = couch[dbname]
            log.write('Connected to db at %s/%s' % (host, dbname))
        except Exception:
            log.write('Error connecting to database')
            raise
            sys.exit(1)

    def get_tasks(self):
        '''a wrapper for couchdb changes which should never die'''
        last_seq = 0
        while(True):
            changes = self.db.changes(feed='continuous', heartbeat=30000, since=last_seq, filter=settings.project_name+'/task')
            try:
                for change in changes:
                    id = change['id']
                    if id in self.db and 'started' not in self.db[id]:
                        last_seq = change['seq']
                        yield id
            except couchdb.http.ResourceNotFound:
                # happens when no changes exist yet or
                # sometimes this happens when the feed terminates
                pass

    def push_results(self, results, id, node_id):
        '''update task document with results'''
        # node disengaged
        node = self.db[node_id]
        for alloc in range(len(node['alloc'])):
            if node['alloc'][alloc]['task'] == id:
                node['alloc'].pop(alloc)
                break
        self.db.save(node)

        try:
            # upload attachments
            doc = self.db[id]
            if 'attachments' in results:
                for attachment in results['attachments']:
                    self.db.put_attachment(doc, attachment['contents'], filename=attachment['filename'])
                    log.write('Task %s: file %s attached' % (id, attachment['filename']))

            doc = self.db[id]
            doc['results'] = results
            doc['completed'] = time.time()
            if 'attachments' in results:
                # if a link name is specified, put a link next to results on the web page
                for attachment in results['attachments']:
                    if 'link_name' in attachment:
                        doc['results'].setdefault('attach_links', []).append({
                            'id': attachment['filename'],
                            'name': attachment['link_name']
                        })
                del doc['results']['attachments']
            self.db.save(doc)
            log.write('Task %s pushed to db' % id)

            # email notification for failed test
            if results['success'] == False and len(settings.notify_list) > 0:
                doctype = 'task'
                if 'kwargs' in doc and 'testname' in doc['kwargs']:
                    doctype = doc['kwargs']['testname']
                else:
                    doctype = doc['name']
                reason = 'n/a'
                if 'reason' in results:
                    reason = results['reason']
                message = '''An automated build test run by the %s server on host %s failed.\n\nType: %s\nRecord ID: %s\nDocument ID: %s\nNode: %s\nReason: %s\n\nThis is an automated email. Please do not reply.''' % (settings.project_name, socket.getfqdn(), doctype, doc['record_id'], id, node['fqdn'], reason)
                dirt.core.yelling.email(settings.notify_list, '[%s] task failure' % settings.project_name, message)

        except couchdb.ResourceNotFound:
            log.write('Cannot push results to db, document %s not found.' % id)
        except KeyError as key:
            log.write('Cannot push results to db, %s key missing in document %s' % (key, id))
            raise
        except IndexError:
            log.write('Cannot push results to db, invalid task id %i for document %s' % (taskid, id))

    def get_nodes(self):
        '''query db to get node data'''
        nodes = {}
        try:
            for row in self.db.view('_design/%s/_view/nodes_by_hostname' % settings.project_name):
                nodes[row.key] = row.value
        except couchdb.http.ResourceNotFound:
            # no nodes
            pass
        return nodes

    def disable_node(self, fqdn):
        '''set a node's ``enabled`` flag to false'''
        for row in self.db.view('_design/%s/_view/nodes_by_hostname' % settings.project_name, key=fqdn):
            log.write('Disabling node %s' % fqdn)
            try:
                node = self.db[row.id]
                node['enabled'] = False
                self.db.save(node)
            except couchdb.http.ResourceNotFound:
                # already gone?
                pass

    def __getitem__(self, id):
        '''get item from the db by id'''
        return self.db[id]

    def save(self, doc):
        '''save a document in the db'''
        self.db.save(doc)

