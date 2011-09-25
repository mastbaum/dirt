# interfacing to couchdb

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
        '''more persistent wrapper for couchdb changes. the couchdb package
        nicely provides the changes feed as a generator, but it terminates
        after some time inactive. since the changes feed drives the dirt
        event loop, we have to wrap the changes in a generator that will
        never die.
        '''
        while(True):
            last_seq = 0
            changes = self.db.changes(feed='continuous', since=last_seq, filter=settings.project_name+'/task')
            for change in changes:
                try:
                    id = change['id']
                    try:
                        if not self.db[id].has_key('started'):
                            yield id
                    except KeyError:
                        continue
                except KeyError:
                    try:
                        # sometimes the feed terminates, but tells us the last seq
                        last_seq = change['last_seq']
                    except KeyError:
                        continue
                except couchdb.http.ResourceNotFound:
                    # sometimes this happens when the feed terminates
                    continue

    def push_results(self, results, id, node_id):
        '''update task document with results'''
        node = self.db[node_id]
        node['active'] = False
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
                        if not 'attach_links' in doc['results']:
                            doc['results']['attach_links'] = []
                        doc['results']['attach_links'].append({'id': attachment['filename'], 'name': attachment['link_name']})
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
                message = '''An automated build test run by the %s server on host %s failed.\n\nType: %s\nDocument ID: %s\nNode: %s\nReason: %s\n\nThis is an automated email. Please do not reply.''' % (settings.project_name, socket.getfqdn(), doctype, id, node['fqdn'], reason)
                dirt.core.yelling.email(settings.notify_list, '[%s] task failure' % settings.project_name, message)

        except couchdb.ResourceNotFound:
            log.write('Cannot push results to db, document %s not found.' % id)
        except KeyError as key:
            log.write('Cannot push results to db, %s key missing in document %s' % (key, id))
            raise
        except IndexError:
            log.write('Cannot push results to db, invalid task id %i for document %s' % (taskid, id))

    def get_nodes(self):
        '''query db to get slave node data'''
        nodes = {}
        for row in self.db.view('_design/'+settings.project_name+'/_view/slaves_by_hostname'):
            nodes[row.key] = row.value
        return nodes

    def disable_node(self, fqdn):
        '''set a node's ``enabled`` flag to false'''
        for row in self.db.view('_design/'+settings.project_name+'/_view/slaves_by_hostname', key=fqdn):
            log.write('Disabling node %s' % fqdn)
            node = self.db[row.id]
            node['enabled'] = False
            self.db.save(node)

    def __getitem__(self, id):
        '''get item from the db by id'''
        return self.db[id]

    def save(self, doc):
        '''save a document in the db'''
        self.db.save(doc)

