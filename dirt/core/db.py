# shared db singleton, so we only have to authenticate once

import settings
from dirt.core import dbi

db = dbi.DirtCouchDB(settings.couchdb_host, settings.couchdb_dbname)

