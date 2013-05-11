import logging
import requests
import sys

from django.core.management.base import BaseCommand, CommandError
from django_pybrowscap import settings
from pybrowscap.loader.csv import URL
from optparse import make_option
from requests import ConnectionError,  HTTPError, Timeout, TooManyRedirects


log = logging.getLogger(__name__)
path_help = """path to save downloaded CSV-file to. Downloaded file will
be printed to stdout if not given or set in settings.PYBROWSCAP_FILE_PATH."""


class Command(BaseCommand):
    help = "Download browscap.csv"
    option_list = BaseCommand.option_list + (
        make_option('-u', '--url',
            action='store',
            type="string",
            dest='url',
            default=None,
            help='URL to download from. Defaults to %s' % URL),
        make_option('-f', '--file-path',
            action='store',
            type="string",
            dest='file_path',
            default=None,
            help=path_help),
        )

    def handle(self, *args, **options):
        self.url = URL
        file_path = settings.PYBROWSCAP_FILE_PATH
        stream = False
        if options['url']:
            self.url = options['url']
        if options['file_path']:
            file_path = options['file_path']
            stream = True
        if file_path:
            log.info("Downloading to %s" % file_path)
            response = self._get_response(stream=True)
            try:
                f = open(file_path, 'w')
            except IOError, err:
                log.exception('Could not open file for writing:')
                sys.exit()
            else:
                # Reads 512KB at a time into memory
                for chunk in response.iter_content(chunk_size = 512 * 1024):
                    # filter out keep-alive new chunks
                    if chunk:
                        f.write(chunk)
                f.close()
        else:
            log.info("Downloading to stdout")
            response = self._get_response()
            self.stdout.write(response.content, ending='')

    def _get_response(self, stream=False):
        log.info("Downloading from %s" % self.url)
        try:
            response = requests.get(self.url, stream=stream)
            try:
                status = response.raise_for_status()
            except:
                log.exception('Download not successful:')
                sys.exit()
        except (ConnectionError,  HTTPError, Timeout, TooManyRedirects), err:
            log.exception('Could not download file:')
            sys.exit()
        return response
