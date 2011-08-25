# interfacing to couchdb

import sys
import couchdb
from log import log

class DirtCouchDB():
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
    def push_results(self, results, id, taskid):
        '''update record document with task results'''
        # todo: key by name, not id
        try:
            doc = self.db[id]
            doc['tasks'][taskid]['results'] = results
            self.db.save(doc)
            log.write('Task %s:%s pushed to db' % (id, taskid))
        except couchdb.ResourceNotFound:
            log.write('Cannot push results to db, document %s not found.' % id)
        except KeyError as key:
            log.write('Cannot push results to db, %s key missing in document %s', (key, id))
        except IndexError:
            log.write('Cannot push results to db, invalid task id %i for document %s' (taskid, id))

    def get_tasks(self):
        '''more persistent wrapper for couchdb changes'''
        import couchdb
        while(True):
            # should filter this for records
            last_seq = 0
            changes = self.db.changes(feed='continuous', since=last_seq)
            for change in changes:
                try:
                    id = change['id']
                    if self.db[id]['type'] == 'record':
                        try:
                            for taskid in range(len(self.db[id]['tasks'])):
                                if not self.db[id]['tasks'][taskid].has_key('results'):
                                    yield id, self.db[id]['tasks'][taskid]['name'], taskid
                        except KeyError:
                            continue
                except KeyError:
                    try:
                        # sometimes the feed terminates, but tells us the last seq
                        last_seq = change['last_seq']
                    except KeyError:
                        continue
                except couchdb.http.ResourceNotFound:
                    continue
    # should be turned into a view
    def get_nodes(self):
        nodedocs = []
        hostnames = []
        for id in self.db:
            try:
                if self.db[id]['type'] == 'slave':
                    nodedocs.append(self.db[id])
                    hostnames.append(self.db[id]['hostname'])
            except KeyError:
                pass
        return hostnames, nodedocs

