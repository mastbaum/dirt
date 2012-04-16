import os
import tarfile
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

# tar up project template directory since setuptools doesn't like dirs
if os.path.exists('dirt/project.tar.gz'):
    os.remove('dirt/project.tar.gz')
tar = tarfile.open('dirt/project.tar.gz','w:gz')
tar.add('dirt/project')
tar.close()

setup(
    name = "dirt",
    version = "0.6",
    author = "Andy Mastbaum",
    author_email = "amastbaum@gmail.com",
    description = ("A framework for oversight and tracking of remotely-executed jobs."),
    license = "BSD",
    keywords = "remote execution couchdb kanso",
    url = "http://github.com/mastbaum/dirt",
    long_description = read('README.md'),
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "License :: OSI Approved :: BSD License",
    ],
    packages = ['dirt','dirt.core','dirt.tasks'],
    scripts = ['bin/dirt'],
    install_requires = ['couchdb', 'execnet'],

    include_package_data = True,
    package_data = {'dirt': ['project.tar.gz']})

