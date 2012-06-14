'''singleton logger object'''

import settings
import yelling

log = yelling.Log(settings.log_file, service_name=settings.project_name)

