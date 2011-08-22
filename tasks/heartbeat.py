def heartbeat():
    '''ensure node is alive and accepting connections'''
    from socket import getfqdn()
    return {'fqdn': getfqdn(), 'alive': True}

if __name__ == '__channelexec__':
    results = heartbeat()
    channel.send(results)

if __name__ == '__main__':
    print heartbeat()
    