def heartbeat():
    '''ensure node is alive and accepting connections'''
    return {'alive': True}

if __name__ == '__channelexec__':
    results = heartbeat()
    channel.send(results)

if __name__ == '__main__':
    print heartbeat()
    
