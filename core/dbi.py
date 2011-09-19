# interfacing to couchdb

import sys
import time
import couchdb
import settings
from log import log

class DirtCouchDB():
    '''wrapper for ``couchdb`` that provides some additional dirt-specific
    functions.
    '''
    def __init__(self, host, dbname):
        couch = couchdb.Server(host)
        try:
            if couch.version() < '1.1.0':
                log.write('Error: couchdb version >= 1.1.0 required')
                sys.exit(1)
            self.db = couch[dbname]
            log.write('Connected to db at %s/%s' % (host, dbname))
        except Exception:
            log.write('Error connecting to database')
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
            changes = self.db.changes(feed='continuous', since=last_seq, filter=settings.couchdb_dbname+'/task')
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

    def push_results(self, results, id, node):
        '''update task document with results'''
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
        for row in self.db.view('_design/'+settings.couchdb_dbname+'/_view/slaves_by_hostname'):
            nodes[row.key] = row.value
        return nodes

    def disable_node(self, fqdn):
        '''set a node's ``enabled`` flag to false'''
        for row in self.db.view('_design/'+settings.couchdb_dbname+'/_view/slaves_by_hostname', key=fqdn):
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

