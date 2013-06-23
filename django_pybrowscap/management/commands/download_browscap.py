import sys
import logging
from optparse import make_option

from django.core.management.base import BaseCommand

from pybrowscap.loader.csv import URL

import requests
from requests import ConnectionError,  HTTPError, Timeout, TooManyRedirects

from ... import settings


log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Download browscap file.'
    option_list = BaseCommand.option_list + (
        make_option('-u', '--url', action='store', type='string', dest='url', default=None,
                    help='URL to download from. Defaults to {0}'.format(URL)),
        make_option('-f', '--file-path', action='store', type='string', dest='file_path', default=None,
                    help='path to save downloaded CSV-file to. File will  be downloaded to '
                         ' settings.PYBROWSCAP_FILE_PATH or --file-path.'),
    )

    def handle(self, *args, **options):
        self.proxies = settings.PYBROWSCAP_PROXIES
        self.timeout = settings.PYBROWSCAP_HTTP_TIMEOUT
        self.url = str(URL)
        file_path = settings.PYBROWSCAP_FILE_PATH
        if options['url'] is not None:
            self.url = options['url']
        if options['file_path'] is not None:
            file_path = options['file_path']
        log.info('Downloading browscap file to %s', file_path)
        response = self._get_response(stream=True)
        try:
            with open(file_path, 'w') as new_file:
                # Reads 512KB at a time into memory.
                for chunk in response.iter_content(chunk_size=(512 * 1024)):
                    # Filter out keep-alive new chunks.
                    if chunk:
                        new_file.write(chunk)
        except IOError:
            log.exception('Could not open file %s for writing!', file_path)
            raise
        finally:
            try:
                response.close()
            except Exception:
                pass

    def _get_response(self, stream=False):
        log.info('Downloading browscap file from %s', self.url)
        try:
            response = requests.get(self.url, stream=stream, proxies=self.proxies, timeout=self.timeout)
            response.raise_for_status()
        except (ConnectionError,  HTTPError, Timeout, TooManyRedirects):
            log.exception('Could not download file from location %s', self.url)
            raise
        return response
