# interfacing to couchdb

import couchdb

class DirtCouchDB():
    def __init__(self, host, dbname):
        couch = couchdb.Server(host)
        try:
            if couch.version() < '1.1.0':
                print 'dirt: couchdb version >= 1.1.0 required'
                sys.exit(1)
            self.db = couch[dbname]
            print 'dirt: connected to db at %s/%s' % (host, dbname)
        except Exception:
            print 'dirt: error connecting to database'
            sys.exit(1)
    def push_results(self, id, taskid, results):
        '''update record document with task results'''
        # todo: exiception handling
        # todo: key by name, not id
        doc = self.db[id]
        doc['tasks'][taskid]['results'] = results
        self.db.save(doc)
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

