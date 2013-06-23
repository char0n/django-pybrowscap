import logging
from datetime import timedelta, datetime

from pybrowscap.loader.csv import load_file

from . import settings


__all__ = ('PybrowscapMiddleware',)


log = logging.getLogger(__name__)


class PybrowscapMiddleware(object):
    """Django middleware class for pybrowscap package."""

    def __init__(self):
        """Constructor.

        This constructor will be called only once while django initialization.

        """
        if settings.PYBROWSCAP_INITIALIZE:
            try:
                log.info('Initializing pybrowscap')
                self.browscap = load_file(settings.PYBROWSCAP_FILE_PATH)
                self.last_load = datetime.now()
                log.info('Pybrowscap initialized')
            except IOError:
                log.exception('Error while initializing pybrowscap')

    def process_request(self, request):
        if settings.PYBROWSCAP_INITIALIZE:
            # Reload mechanism.
            if (settings.PYBROWSCAP_RELOAD and self.browscap is not None and
                getattr(self, 'last_load', None) is not None and
                    (datetime.now() - self.last_load).total_seconds() > settings.PYBROWSCAP_RELOAD_INTERVAL):
                self.browscap.reload()
                self.browscap.last_load = self.browscap.reloaded_at
            try:
                for regex in settings.PYBROWSCAP_IGNORE_PATHS:
                    if regex.search(request.path_info):
                        return
            except TypeError:
                pass  # Ignore nothing.
            except AttributeError:
                log.warn('Invalid request, no path info present')
                return

            try:
                if self.browscap is not None:
                    request.browser = self.browscap.search(request.META['HTTP_USER_AGENT'])
            except AttributeError:
                log.warn('Request has no meta info, impossible to search for user agent')
            except KeyError:
                log.warn('Request has no user agent meta info, impossible to search for user agent')
            finally:
                if not hasattr(request, 'browser'):
                    request.browser = None