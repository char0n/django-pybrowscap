import urllib2
import logging
from datetime import datetime

from django_pybrowscap import settings
from pybrowscap.loader.csv import load_file, URL
from pybrowscap.loader import Downloader


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
            except IOError:
                log.exception('Error while initializing pybrowscap')
                self.browscap = None
            else:
                log.info('Pybrowscap initialized')

    def process_request(self, request):
        if settings.PYBROWSCAP_INITIALIZE:
            try:
                for regex in settings.PYBROWSCAP_IGNORE_PATHS:
                    if regex.search(request.path_info):
                        return
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

            if settings.PYBROWSCAP_UPDATE:
                try:
                    last_reloaded = self.browscap.reloaded_at or self.browscap.loaded_at
                    if (datetime.now() - last_reloaded).total_seconds() > settings.PYBROWSCAP_UPDATE_INTERVAL:
                        try:
                            log.info('Reloading pybrowscap with new data')
                            Downloader(URL).get(settings.PYBROWSCAP_FILE_PATH)
                            self.browscap.reload(settings.PYBROWSCAP_FILE_PATH)
                        except (ValueError, urllib2.HTTPError, urllib2.URLError, IOError):
                            log.exception('Error while reloading pybrowscap')
                        else:
                            log.info('Pybrowscap successfully reloaded')
                except AttributeError:
                    log.warn('Error while reloading uninitialized pybrowscap')