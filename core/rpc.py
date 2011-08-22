# xml-rpc functions so hosts behind firewalls can join the party
# stub

import xmlrpclib
import pickle

def register_hidden():
    pass

def task_pull():
    pass

def task_push():
    pass

if __name__ == '__main__':
    # for testing, serve from here
    from SimpleXMLRPCServer import SimpleXMLRPCServer
    server = SimpleXMLRPCServer(("localhost", 8000))
    print "Listening on port 8000..."
    server.register_function(task_pull, "task_pull")
    server.serve_forever()

