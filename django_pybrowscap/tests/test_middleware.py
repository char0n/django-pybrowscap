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


__all__ = ('TestInitialization', 'TestIgnorePaths', 'TestRequestErrors')


class TestInitialization(TestCase):

    @mock.patch('django_pybrowscap.middleware.settings')
    def test_initialization_default(self, settings):
        settings.PYBROWSCAP_FILE_PATH = BROWSCAP_FILE
        response = self.client.get(reverse('view'), **{'HTTP_USER_AGENT': USER_AGENT})
        self.assertIsInstance(response.context['browser'], Browser)

    @mock.patch('django_pybrowscap.middleware.settings')
    def test_initialization_on(self, settings):
        settings.PYBROWSCAP_FILE_PATH = BROWSCAP_FILE
        settings.PYBROWSCAP_INITIALIZE = True
        response = self.client.get(reverse('view'), **{'HTTP_USER_AGENT': USER_AGENT})
        self.assertIsInstance(response.context['browser'], Browser)

    @mock.patch('django_pybrowscap.middleware.settings')
    def test_initialization_off(self, settings):
        settings.PYBROWSCAP_FILE_PATH = BROWSCAP_FILE
        settings.PYBROWSCAP_INITIALIZE = False
        response = self.client.get(reverse('view'), **{'HTTP_USER_AGENT': USER_AGENT})
        self.assertIsNone(response.context['browser'])


class TestIgnorePaths(TestCase):

    @mock.patch('django_pybrowscap.middleware.settings')
    def test_ignore_nothing(self, settings):
        settings.PYBROWSCAP_FILE_PATH = BROWSCAP_FILE
        settings.PYBROWSCAP_IGNORE_PATHS = None
        response = self.client.get(reverse('view'), **{'HTTP_USER_AGENT': USER_AGENT})
        self.assertIsInstance(response.context['browser'], Browser)
        response = self.client.get(reverse('robots'), **{'HTTP_USER_AGENT': USER_AGENT})
        self.assertIsInstance(response.context['browser'], Browser)

    @mock.patch('django_pybrowscap.middleware.settings')
    def test_ignore_robots(self, settings):
        settings.PYBROWSCAP_FILE_PATH = BROWSCAP_FILE
        settings.PYBROWSCAP_IGNORE_PATHS = (re.compile(r'^/robots.txt$'),)
        response = self.client.get(reverse('robots'), **{'HTTP_USER_AGENT': USER_AGENT})
        self.assertIsNone(response.context['browser'])


class TestRequestErrors(TestCase):

    def setUp(self):
        self.request = WSGIRequest(environ={
            'wsgi.input': StringIO(),
            'REQUEST_METHOD': 'POST',
            'SERVER_NAME': 'testserver',
            'SERVER_PORT': '80',
            'CONTENT_TYPE': 'text/html',
            'ACCEPT': 'text/html',
            'USER_AGENT': USER_AGENT
        })

    @mock.patch('django_pybrowscap.middleware.settings')
    def test_no_meta(self, settings):
        settings.PYBROWSCAP_FILE_PATH = BROWSCAP_FILE
        middleware = PybrowscapMiddleware()
        delattr(self.request, 'META')
        middleware.process_request(self.request)
        self.assertIsNone(self.request.browser)

    @mock.patch('django_pybrowscap.middleware.settings')
    def test_no_meta_user_agent(self, settings):
        settings.PYBROWSCAP_FILE_PATH = BROWSCAP_FILE
        del self.request.META['USER_AGENT']
        middleware = PybrowscapMiddleware()
        middleware.process_request(self.request)
        self.assertIsNone(self.request.browser)