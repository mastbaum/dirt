# interfacing to couchdb
# mostly should be turned into views

def get_tasks(db):
    '''more persistent wrapper for couchdb changes'''
    import couchdb
    while(True):
        # should filter this for records
        last_seq = 0
        changes = db.changes(feed='continuous', since=last_seq)
        for change in changes:
            try:
                id = change['id']
                if db[id]['type'] == 'record':
                    try:
                        for task in db[id]['tasks']:
                            yield id, task['name']
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

# this should be a couchdb view
def get_nodes(db):
    nodedocs = []
    hostnames = []
    for id in db:
        try:
            if db[id]['type'] == 'slave':
                nodedocs.append(db[id])
                hostnames.append(db[id]['hostname'])
        except KeyError:
            pass
    return hostnames, nodedocs

# this should be a couchdb view
#def get_available_tasks(db):
#    tasks = []
#    for id in db:
#        try:
#            if db[id]['type'] == 'record':
#                record = db[id]
#                for task in record['tasks']:
#                    d = {}
#                    d['record_id'] = id
#                    d['task_name'] = task['name']
#                    d['task_doc'] = task
#                    tasks.append(d)
#        except KeyError:
#            pass
#    return tasks

