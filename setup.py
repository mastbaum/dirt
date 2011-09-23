import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "dirt",
    version = "0.5",
    author = "Andy Mastbaum",
    author_email = "amastbaum@gmail.com",
    description = ("A restful framework for oversight and tracking of remotely-executed jobs."),
    license = "BSD",
    keywords = "remote execution couchdb kanso",
    url = "http://github.com/mastbaum/dirt",
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "License :: OSI Approved :: BSD License",
    ],

    packages=['dirt'],
    scripts=['bin/dirt'],
    install_requires = ['couchdb', 'execnet'],

    include_package_data = True,
    package_data = {'project':'*'}
)

