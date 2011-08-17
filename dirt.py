#/usr/bin/env python

# DIRT.
#
# Andy Mastbaum (amastbaum@gmail.com), August 2011

import sys

def serve_forever():
    print 'dirt is running...'
    # do things forever

def help():
    print \
'''
usage:
'''

if __name__ == '__main__':
    if len(sys.argv) < 2:
        help()
        sys.exit(1)

    if sys.argv[1] == 'serve':
        serve_forever()
    elif sys.argv[1] == 'updatenodes':
        import core.helpers
        nodes = sys.argv[2:]
        if len(nodes) == 0:
            help()
            sys.exit(1)
        core.helpers.node_recon(nodes, core.helpers.connect_to_db())

