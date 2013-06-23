import re
from StringIO import StringIO

from django.core.handlers.wsgi import WSGIRequest
from django.test import TestCase
from django.test.utils import setup_test_environment
setup_test_environment()
from django.core.urlresolvers import reverse

import mock
from pybrowscap import Browser

from ..tests import BROWSCAP_FILE, USER_AGENT
from ..middleware import PybrowscapMiddleware
from .. import settings as app_settings


__all__ = ('InitializationTest', 'BrowscapFileReloadTest', 'IgnorePathsTest', 'RequestErrorsTest')


def make_request():
    return WSGIRequest(environ={
        'wsgi.input': StringIO(),
        'REQUEST_METHOD': 'POST',
        'SERVER_NAME': 'testserver',
        'SERVER_PORT': '80',
        'CONTENT_TYPE': 'text/html',
        'ACCEPT': 'text/html',
        'USER_AGENT': USER_AGENT
    })


class InitializationTest(TestCase):

    def setUp(self):
        self.settings_patcher = mock.patch('django_pybrowscap.middleware.settings')
        self.mock_settings = self.settings_patcher.start()
        self.mock_settings.PYBROWSCAP_FILE_PATH = BROWSCAP_FILE

    def tearDown(self):
        self.settings_patcher.stop()

    def test_initialization_default(self):
        response = self.client.get(reverse('view'), **{'HTTP_USER_AGENT': USER_AGENT})
        self.assertIsInstance(response.context['browser'], Browser)

    def test_initialization_on(self):
        self.mock_settings.PYBROWSCAP_INITIALIZE = True
        response = self.client.get(reverse('view'), **{'HTTP_USER_AGENT': USER_AGENT})
        self.assertIsInstance(response.context['browser'], Browser)

    def test_initialization_off(self):
        self.mock_settings.PYBROWSCAP_INITIALIZE = False
        response = self.client.get(reverse('view'), **{'HTTP_USER_AGENT': USER_AGENT})
        self.assertIsNone(response.context['browser'])


class BrowscapFileReloadTest(TestCase):

    def setUp(self):
        self.settings_patcher = mock.patch('django_pybrowscap.middleware.settings')
        self.mock_settings = self.settings_patcher.start()
        self.mock_settings.PYBROWSCAP_FILE_PATH = BROWSCAP_FILE
        self.mock_settings.PYBROWSCAP_PROXIES = app_settings.PYBROWSCAP_PROXIES
        self.mock_settings.PYBROWSCAP_HTTP_TIMEOUT = app_settings.PYBROWSCAP_HTTP_TIMEOUT
        self.mock_settings.PYBROWSCAP_RELOAD = True
        self.mock_settings.PYBROWSCAP_RELOAD_INTERVAL = app_settings.PYBROWSCAP_HTTP_TIMEOUT

    def tearDown(self):
        self.settings_patcher.stop()

    @mock.patch('pybrowscap.loader.csv.Browscap')
    def test_reload(self, browscap):
        middleware = PybrowscapMiddleware()
        middleware.process_request(make_request())
        middleware.browscap.reload.assert_called_zero()
        self.mock_settings.PYBROWSCAP_RELOAD_INTERVAL = 0
        middleware.process_request(make_request())
        middleware.browscap.reload.assert_called_once()


class IgnorePathsTest(TestCase):

    def setUp(self):
        self.settings_patcher = mock.patch('django_pybrowscap.middleware.settings')
        self.mock_settings = self.settings_patcher.start()
        self.mock_settings.PYBROWSCAP_FILE_PATH = BROWSCAP_FILE

    def tearDown(self):
        self.settings_patcher.stop()

    def test_ignore_nothing(self):
        self.mock_settings.PYBROWSCAP_IGNORE_PATHS = None
        response = self.client.get(reverse('view'), **{'HTTP_USER_AGENT': USER_AGENT})
        self.assertIsInstance(response.context['browser'], Browser)
        response = self.client.get(reverse('robots'), **{'HTTP_USER_AGENT': USER_AGENT})
        self.assertIsInstance(response.context['browser'], Browser)

    def test_ignore_robots(self):
        self.mock_settings.PYBROWSCAP_IGNORE_PATHS = (re.compile(r'^/robots.txt$'),)
        response = self.client.get(reverse('robots'), **{'HTTP_USER_AGENT': USER_AGENT})
        self.assertIsNone(response.context['browser'])


class RequestErrorsTest(TestCase):

    def setUp(self):
        self.request = make_request()

        self.settings_patcher = mock.patch('django_pybrowscap.middleware.settings')
        self.mock_settings = self.settings_patcher.start()
        self.mock_settings.PYBROWSCAP_FILE_PATH = BROWSCAP_FILE

    def tearDown(self):
        self.settings_patcher.stop()

    def test_no_meta(self):
        middleware = PybrowscapMiddleware()
        delattr(self.request, 'META')
        middleware.process_request(self.request)
        self.assertIsNone(self.request.browser)

    def test_no_meta_user_agent(self):
        del self.request.META['USER_AGENT']
        middleware = PybrowscapMiddleware()
        middleware.process_request(self.request)
        self.assertIsNone(self.request.browser)