# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

import django_pybrowscap


setup(
    name='django-pybrowscap',
    version=django_pybrowscap.__version__,
    description='django-pybrowscap is django middleware with support for pybrowscap',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
    author=u'Vladimír Gorej',
    author_email='gorej@codescale.net',
    url='http://www.codescale.net/en/community#django-pybrowscap',
    download_url='http://github.com/CodeScaleInc/django-pybrowscap/tarball/master',
    license='BSD',
    keywords = 'browser browscap detection user agent django',
    packages=find_packages('.'),
    package_data = {
        # If any package contains *.csv files, include them:
        'django_pybrowscap.tests': ['data/*.csv']
    },
    test_suite='runtests.runtests',
    install_requires = ['django', 'pybrowscap', 'requests'],
    extras_require = {
        'tests': ['mock']
    },
    platforms='any',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Browsers'
    ]
)