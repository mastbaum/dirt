import os
import uuid
import shutil
import tarfile
from string import Template

class MyTemplate(Template):
    delimiter = '%%%'

exts = ['.html','.py','.js','.md','.json']
exclude_dirs = ['js']

def create(project, db_name=None):
    if db_name is None:
        db_name = project
    '''creates the directory structure for a new dirt project'''
    skel_file = os.path.join(os.path.dirname(__file__), '..', 'project.tar.gz')
    skeleton_tarball = tarfile.open(skel_file,'r:gz')
    wd = uuid.uuid4().get_hex()
    os.mkdir(wd)
    skeleton_tarball.extractall(wd)
    subs = {'project': project, 'db_name': db_name}
    cwd = os.path.dirname(os.path.abspath(__file__))
    shutil.copytree(os.path.join(wd, 'dirt', 'project'), project)
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
    shutil.rmtree(wd)

    print 'Created new dirt project in', project

