import os
import shutil
from string import Template

class MyTemplate(Template):
    delimiter = '%%%'

exts = ['.html','.py','.js','.md','.json']
exclude_dirs = ['js']

def create(project, db_name):
    '''creates the directory structure for a new dirt project'''
    subs = {'project': project, 'db_name': db_name}
    cwd = os.path.dirname(os.path.abspath(__file__))
    shutil.copytree(cwd + '/../project', project)
    for root, dirs, files in os.walk(project, topdown=False):
        for name in files:
            fname = os.path.join(root, name)
            if os.path.splitext(name)[-1] in exts and not os.path.split(root)[-1] in exclude_dirs:
                contents = ''
                with open(fname,'r') as f:
                    contents = f.read()
                contents = MyTemplate(contents).substitute(subs)
                with open(fname,'w') as f:
                    f.write(contents)

    print 'Created new dirt project in', project

