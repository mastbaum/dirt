#!/usr/bin/env python

import sys
import xmlrpclib
import pickle

def help():
    print 'Usage: %s http://hostname:port' % sys.argv[0]

def main(server):
    proxy = xmlrpclib.ServerProxy(server)

    fs = proxy.task_pull()
    fcn = pickle.loads(fs)

    results = fcn()

    proxy.task_push(results)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        help()
        sys.exit(0)
    else:
        main(sys.argv[1])
    

