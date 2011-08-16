import os
import sqlite3
import logging
import couchdb

from pyramid.events import subscriber
from pyramid.events import NewRequest
from pyramid.events import ApplicationCreated

logging.basicConfig()
log = logging.getLogger(__file__)
here = os.path.dirname(os.path.abspath(__file__))

@subscriber(NewRequest)
def add_couchdb_to_request(event):
    request = event.request
    settings = request.registry.settings
    db = settings['db_server'][settings['db_name']]
    event.request.db = db

#@subscriber(ApplicationCreated)
#def application_created_subscriber(event):
#    log.warn('Initializing database...')
#    f = open(os.path.join(here, 'schema.sql'), 'r')
#    stmt = f.read()
#    settings = event.app.registry.settings
#    db = sqlite3.connect(settings['db'])
#    db.executescript(stmt)
#    db.commit()
#    f.close()

