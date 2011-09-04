def execute():
    '''ensure node is alive and accepting connections'''
    return {'success': True}

if __name__ == '__channelexec__':
    results = execute()
    channel.send(results)

if __name__ == '__main__':
    print execute()
    
