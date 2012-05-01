django-pybrowscap
=================


django-pybrowscap is django middleware with support for pybrowscap.
It decorates request with browser attribute, browser being instance of pybrowscap.Browser class.

Requirements
------------

- python 2.7+
- django
- pybrowscap
- browscap csv file (http://browsers.garykeith.com/downloads.asp)


Installation
------------

Install via pipy or copy this module into your project or into your PYTHON_PATH.
Download latest version of browscap.csv file from http://browsers.garykeith.com/downloads.asp.


**Put django_pybrowscap into INSTALLED_APPS in your projects settings.py file**

::

 INSTALLED_APPS = (
     'localeurl',
     'django.contrib.auth',
     'django.contrib.contenttypes',
     'django.contrib.sessions',
     'django.contrib.sites',
     'django.contrib.admin',
     'django.contrib.sitemaps',
     'web',
     'debug_toolbar',
     'rosetta',
     'south',
     'django_pybrowscap'
 )


**Put django_pybrowscap.middleware.PybrowscapMiddleware into MIDDLEWARE_CLASSES in your projects settings.py file**

::

 MIDDLEWARE_CLASSES = (
     'web.middleware.LocaleMiddleware',
     'django.middleware.common.CommonMiddleware',
     'django.contrib.sessions.middleware.SessionMiddleware',
     'django_pybrowscap.middleware.PybrowscapMiddleware',
     ....
 )


Configuration
-------------

**django settings.py constants**

::

 # This setting will effectively turn the middleware off, to speed up requests/response while developing
 PYBROWSCAP_INITIALIZE = True # Default is `not settings.DEBUG`.

 # Path where browscap file is located on filesystem
 PYBROWSCAP_FILE_PATH = MEDIA_ROOT+os.sep+'browscap.csv' # Default is '' (empty string)

 # Whether to perform automatic updates of browscap file
 PYBROWSCAP_UPDATE = False # Default is False

 # Interval of automatic browscap file updates
 PYBROWSCAP_UPDATE_INTERVAL = 604800 # Default one week in seconds

 # Tuple or regex expressions of path that are to be ignored by middleware
 PYBROWSCAP_IGNORE_PATHS = (
     re.compile(r'^/sitemap.xml$'),
     re.compile(r'^/robots.txt$'),
     re.compile(r'^/favicon.ico$'),
     re.compile(r'^/media/')
 ) # Default empty tupple


Example
-------

::

 def standard_view(request):
     if request.browser is not None and request.browser.is_crawler():
         # do something
     else:
         # do something else



Tests
-----

**Tested on evnironment**

- Xubuntu Linux 12.04 LTS precise 64-bit
- python 2.7.3
- python unitest
- browscap_22_06_2011.csv from Wed, 22 Jun 2011 23:26:51 -0000

**Running tests**

To run the test run command: ::

 $ python manage.py test django_pybrowscap



Author
------

| char0n (Vladimir Gorej, CodeScale s.r.o.)
| email: gorej@codescale.net
| web: http://www.codescale.net


References
----------

- http://github.com/char0n/django-pybrowscap
- http://browsers.garykeith.com/
- http://php.net/get_browser
- http://www.codescale.net/en/community#django-pybrowscap