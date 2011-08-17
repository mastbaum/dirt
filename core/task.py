class Task:
    def __init__(self, name):
        self.name = name
        self.results = {}
    def execute(self):
        '''system calls to run this task. this should be overridden in
        subclasses of Task.'''
        pass

