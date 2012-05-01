import os
import re
import time
import unittest
from datetime import datetime

from pybrowscap import Browser
from django_pybrowscap import middleware


class RequestMock(object):

    def __init__(self):
        self.path_info = '/'
        self.META = {'HTTP_USER_AGENT': 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.18) Gecko/20110628 Ubuntu/10.10 (maverick) Firefox/3.6.18'}


class BaseTest(unittest.TestCase):

    def setUp(self):

        middleware.settings.PYBROWSCAP_FILE_PATH = os.path.join(os.path.dirname(__file__), 'data', 'browscap_22_06_2011.csv')
        self.request = RequestMock()
        self.DEFAULT_PYBROWSCAP_INITIALIZE = middleware.settings.PYBROWSCAP_INITIALIZE
        self.DEFAULT_PYBROWSCAP_FILE_PATH = middleware.settings.PYBROWSCAP_FILE_PATH
        self.DEFAULT_PYBROWSCAP_UPDATE = middleware.settings.PYBROWSCAP_UPDATE
        self.DEFAULT_PYBROWSCAP_UPDATE_INTERVAL = middleware.settings.PYBROWSCAP_UPDATE_INTERVAL
        self.DEFAULT_PYBROWSCAP_IGNORE_PATHS = middleware.settings.PYBROWSCAP_IGNORE_PATHS

    def tearDown(self):
        middleware.settings.PYBROWSCAP_INITIALIZE = self.DEFAULT_PYBROWSCAP_INITIALIZE
        middleware.settings.PYBROWSCAP_FILE_PATH = self.DEFAULT_PYBROWSCAP_FILE_PATH
        middleware.settings.PYBROWSCAP_UPDATE = self.DEFAULT_PYBROWSCAP_UPDATE
        middleware.settings.PYBROWSCAP_UPDATE_INTERVAL = self.DEFAULT_PYBROWSCAP_UPDATE_INTERVAL
        middleware.settings.PYBROWSCAP_IGNORE_PATHS = self.DEFAULT_PYBROWSCAP_IGNORE_PATHS


class TestInitialize(BaseTest):

    def test_initialization_on(self):
        middleware.settings.PYBROWSCAP_INITIALIZE = True
        instance = middleware.PybrowscapMiddleware()
        self.assertTrue(hasattr(instance, 'browscap'))
        instance.process_request(self.request)
        self.assertIsNotNone(self.request.browser)
        self.assertIsInstance(self.request.browser, Browser)
        self.assertFalse(self.request.browser.is_crawler())

    def test_initialization_off(self):
        middleware.settings.PYBROWSCAP_INITIALIZE = False
        instance = middleware.PybrowscapMiddleware()
        self.assertFalse(hasattr(instance, 'browscap'))
        self.assertFalse(hasattr(self.request, 'browser'))

    def test_initialization_no_file(self):
        middleware.settings.PYBROWSCAP_FILE_PATH = ''
        instance = middleware.PybrowscapMiddleware()
        self.assertIsNone(instance.browscap)


class TestUpdate(BaseTest):

    def test_update(self):
        middleware.settings.PYBROWSCAP_UPDATE = True
        middleware.settings.PYBROWSCAP_UPDATE_INTERVAL = 0.1
        instance = middleware.PybrowscapMiddleware()
        self.assertGreaterEqual(datetime.now(), instance.browscap.loaded_at)
        self.assertIsNone(instance.browscap.reloaded_at)
        time.sleep(0.2)
        instance.process_request(self.request)
        self.assertGreaterEqual(datetime.now(), instance.browscap.loaded_at)
        self.assertGreaterEqual(datetime.now(), instance.browscap.reloaded_at)

    def test_update_long_interval(self):
        middleware.settings.PYBROWSCAP_UPDATE = True
        middleware.settings.PYBROWSCAP_UPDATE_INTERVAL = 100
        instance = middleware.PybrowscapMiddleware()
        self.assertGreaterEqual(datetime.now(), instance.browscap.loaded_at)
        self.assertIsNone(instance.browscap.reloaded_at)
        time.sleep(0.1)
        instance.process_request(self.request)
        self.assertGreaterEqual(datetime.now(), instance.browscap.loaded_at)
        self.assertIsNone(instance.browscap.reloaded_at)

    def test_no_update(self):
        middleware.settings.PYBROWSCAP_UPDATE = False
        middleware.settings.PYBROWSCAP_UPDATE_INTERVAL = 0.1
        instance = middleware.PybrowscapMiddleware()
        self.assertGreaterEqual(datetime.now(), instance.browscap.loaded_at)
        self.assertIsNone(instance.browscap.reloaded_at)
        time.sleep(0.1)
        instance.process_request(self.request)
        self.assertGreaterEqual(datetime.now(), instance.browscap.loaded_at)
        self.assertIsNone(instance.browscap.reloaded_at)


class TestIgnorePaths(BaseTest):

    def test_ignore_nothing(self):
        instance = middleware.PybrowscapMiddleware()
        instance.process_request(self.request)
        self.assertIsNotNone(self.request.browser)
        self.assertIsInstance(self.request.browser, Browser)
        self.assertFalse(self.request.browser.is_crawler())

    def test_ignore_media(self):
        middleware.settings.PYBROWSCAP_IGNORE_PATHS = (
            re.compile(r'^/media/'),
        )
        self.request.path_info = '/media/image.jpg'
        instance = middleware.PybrowscapMiddleware()
        instance.process_request(self.request)
        self.assertFalse(hasattr(self.request, 'browser'))


class TestRequestErrors(BaseTest):

    def test_no_meta(self):
        del self.request.META
        instance = middleware.PybrowscapMiddleware()
        instance.process_request(self.request)
        self.assertTrue(hasattr(self.request, 'browser'))
        self.assertIsNone(self.request.browser)

    def test_no_meta_user_agent(self):
        self.request.META = {}
        instance = middleware.PybrowscapMiddleware()
        instance.process_request(self.request)
        self.assertTrue(hasattr(self.request, 'browser'))
        self.assertIsNone(self.request.browser)