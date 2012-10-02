def execute():
    '''get current system load'''
    import subprocess

    uptime = subprocess.check_output(['uptime'])
    load = float(uptime.rsplit(':',1)[-1].split(',')[0].strip())

    return {'load': load}

if __name__ == '__channelexec__':
    results = execute()
    channel.send(results)

if __name__ == '__main__':
    print execute()

