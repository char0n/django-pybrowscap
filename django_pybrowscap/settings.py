from django.conf import settings

# This setting will effectively turn the middleware off, to speed up requests/response while developing
PYBROWSCAP_INITIALIZE = getattr(settings, 'PYBROWSCAP_INITIALIZE', not settings.DEBUG)

# Path where browscap file is located on filesystem
PYBROWSCAP_FILE_PATH = getattr(settings, 'PYBROWSCAP_FILE_PATH', None)

# Proxy to use
# See: http://docs.python-requests.org/en/latest/user/advanced/#proxies
PYBROWSCAP_PROXIES = getattr(settings, 'PYBROWSCAP_PROXIES', None)

# Timeout for HTTP requets
# See: http://docs.python-requests.org/en/latest/user/quickstart/#timeouts
PYBROWSCAP_HTTP_TIMEOUT = getattr(settings, 'PYBROWSCAP_HTTP_TIMEOUT', 30)

# Tuple or regex expressions of path that are to be ignored by middleware
PYBROWSCAP_IGNORE_PATHS = getattr(settings, 'PYBROWSCAP_IGNORE_PATHS', ())
