import settings
from dirt.core import yelling

# singleton logger object
log = yelling.Log(settings.log_file, service_name=settings.project_name)

