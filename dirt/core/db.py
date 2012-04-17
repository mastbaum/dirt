import settings
from dirt.core import dbi

# shared db singleton, so we only have to authenticate once
db = dbi.DirtCouchDB(settings.couchdb_host, settings.couchdb_dbname)

