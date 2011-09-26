def check_requirements(db, id, node):
    '''check if system requirements defined in the task document are satisfied
    by this node. some reinvention of the query language is worth it for not
    eval()-ing stuff from the database.
    '''
    if 'requires' not in db[id]:
        return True
    reqs = db[id]['requires']
    for req in reqs:
        try:
            req = req.split()
            if len(req) != 3:
                doc = db[id]
                doc['success'] = False
                doc['reason'] = 'invalid value in requires'
                return False
            if req[1] == 'is':
                if str(node['sys_info'][req[0]]) != req[2]:
                    return False
            elif req[1] == 'not':
                if str(node['sys_info'][req[0]]) == req[2]:
                    return False
            elif req[1] == 'in':
                if req['sys_info'][2] not in node[req[0]]:
                    return False
            elif req[1] == 'not_in':
                if req['sys_info'][2] in node[req[0]]:
                    return False
        except KeyError(key):
            doc = db[id]
            doc['success'] = False
            doc['reason'] = 'invalid key %s in requires' % str(key)
            return False
    return True

