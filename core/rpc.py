# xml-rpc functions so hosts behind firewalls can join the party

import xmlrpclib
import pickle

from SimpleXMLRPCServer import SimpleXMLRPCServer


server = SimpleXMLRPCServer(("localhost", 8000))
print "Listening on port 8000..."
server.register_function(gimme, "gimme")

server.serve_forever()

def register_hidden():
    pass

def task_pull():
    from tasks import *
    # get next task as taskname
    task_module = __import__('tasks.%s' % taskname, fromlist=['tasks'])

    pf = pickle.dumps(task_module.execute)
    return pf

def task_push():
    pass

