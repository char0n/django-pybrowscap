from django.conf import settings

# This setting will effectively turn the middleware off, to speed up requests/response while developing
PYBROWSCAP_INITIALIZE = getattr(settings, 'PYBROWSCAP_INITIALIZE', not settings.DEBUG)

# Path where browscap file is located on filesystem
PYBROWSCAP_FILE_PATH = getattr(settings, 'PYBROWSCAP_FILE_PATH', '')

# Whether to perform automatic updates of browscap file
PYBROWSCAP_UPDATE = getattr(settings, 'PYBROWSCAP_UPDATE', False)

# Interval of automatic browscap file updates
PYBROWSCAP_UPDATE_INTERVAL = getattr(settings, 'PYBROWSCAP_UPDATE_INTERVAL', 604800) # default one week on seconds

# Tuple or regex expressions of path that are to be ignored by middleware
PYBROWSCAP_IGNORE_PATHS = getattr(settings, 'PYBROWSCAP_IGNORE_PATHS', ())