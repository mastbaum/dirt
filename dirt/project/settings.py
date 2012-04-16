# %%%project Configuration

# Project name
project_name = '%%%{project}'

## Database configuration
# URL of couchdb server
couchdb_host = 'http://localhost:5984'
# couchdb database name
couchdb_dbname = '%%%{db_name}'

## Node configuration defaults
# When adding a new node, enable it by default?
node_enable_default = True

## Logging configuration
# Log file name
log_file = '%%%{project}.log'
# Email addresses to notify if a test fails
notify_list = []
# SMTP server is required for sending email notifications
smtp_server = ''

