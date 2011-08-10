import os
import sqlite3
import logging

from pyramid.events import subscriber
from pyramid.events import NewRequest
from pyramid.events import ApplicationCreated

logging.basicConfig()
log = logging.getLogger(__file__)
here = os.path.dirname(os.path.abspath(__file__))

@subscriber(NewRequest)
def new_request_subscriber(event):
    request = event.request
    settings = request.registry.settings
    request.db = sqlite3.connect(settings['db'])
    request.add_finished_callback(close_db_connection)

def close_db_connection(request):
    request.db.close()

@subscriber(ApplicationCreated)
def application_created_subscriber(event):
    log.warn('Initializing database...')
    f = open(os.path.join(here, 'schema.sql'), 'r')
    stmt = f.read()
    settings = event.app.registry.settings
    db = sqlite3.connect(settings['db'])
    db.executescript(stmt)
    db.commit()
    f.close()

