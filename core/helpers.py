def system(cmd, wd=None):
    '''a wrapper for subprocess.call, which executes cmd in working directory
    wd in a bash shell, returning the exit code.'''
    if wd:
        cmd = ('cd %s && ' % wd) + cmd
    if debug:
        print cmd
        return 0
    return subprocess.call([cmd], executable='/bin/bash', shell=True)

