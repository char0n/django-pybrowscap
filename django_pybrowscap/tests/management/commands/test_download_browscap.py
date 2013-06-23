import os

from django.core.management import call_command
from django.test import TestCase

import mock
from pybrowscap.loader.csv import URL, load_file
from requests import HTTPError
from requests.models import Response

from ....tests import DOWNLOAD_URL, BROWSCAP_FILE
from .... import settings as app_settings


__all__ = ('DownloadBrowscapCommandTest', 'DownloadBrowscapCommandIntegrationTest')


class DownloadBrowscapCommandTest(TestCase):

    def setUp(self):
        self.browscap_file_contents = open(BROWSCAP_FILE).read()

        self.settings_patcher = mock.patch('django_pybrowscap.management.commands.download_browscap.settings')
        self.mock_settings = self.settings_patcher.start()
        self.mock_settings.PYBROWSCAP_PROXIES = app_settings.PYBROWSCAP_PROXIES
        self.mock_settings.PYBROWSCAP_HTTP_TIMEOUT = app_settings.PYBROWSCAP_HTTP_TIMEOUT
        self.mock_settings.PYBROWSCAP_FILE_PATH = 'test.csv'

        self.requests_patcher = mock.patch('django_pybrowscap.management.commands.download_browscap.requests')
        self.mock_requests = self.requests_patcher.start()
        self.mock_response = mock.MagicMock(spec=Response)
        self.mock_response.status_code = 200
        self.mock_response.iter_content.return_value = [self.browscap_file_contents]
        self.mock_requests.get.return_value = self.mock_response

    def tearDown(self):
        self.settings_patcher.stop()
        try:
            os.remove('test.csv')
            os.remove('custom_file_path.csv')
        except OSError:
            pass

    def test_download_defaults(self):
        call_command('download_browscap')
        self.mock_requests.get.assert_called_once_with(URL, proxies=None, stream=True, timeout=30)
        self.assertEqual(self.browscap_file_contents, open('test.csv').read())

    def test_download_custom_url(self):
        call_command('download_browscap', url=DOWNLOAD_URL)
        self.mock_requests.get.assert_called_once_with(DOWNLOAD_URL, proxies=None, stream=True, timeout=30)
        self.assertEqual(self.browscap_file_contents, open('test.csv').read())

    def test_download_custom_file_path(self):
        call_command('download_browscap', file_path='custom_file_path.csv')
        self.mock_requests.get.assert_called_once_with(URL, proxies=None, stream=True, timeout=30)
        self.assertEqual(self.browscap_file_contents, open('custom_file_path.csv').read())


class DownloadBrowscapCommandIntegrationTest(TestCase):

    def setUp(self):
        self.browscap_file_contents = open(BROWSCAP_FILE).read()

        self.settings_patcher = mock.patch('django_pybrowscap.management.commands.download_browscap.settings')
        self.mock_settings = self.settings_patcher.start()
        self.mock_settings.PYBROWSCAP_PROXIES = app_settings.PYBROWSCAP_PROXIES
        self.mock_settings.PYBROWSCAP_HTTP_TIMEOUT = app_settings.PYBROWSCAP_HTTP_TIMEOUT
        self.mock_settings.PYBROWSCAP_FILE_PATH = 'test.csv'

    def tearDown(self):
        self.settings_patcher.stop()
        try:
            os.remove('test.csv')
        except OSError:
            pass

    def test_download(self):
        call_command('download_browscap', url=DOWNLOAD_URL)
        browscap = load_file('test.csv')
        self.assertEqual(5003, browscap.version)

    def test_download_error(self):
        with self.assertRaises(HTTPError):
            call_command('download_browscap', url=DOWNLOAD_URL + 'e')