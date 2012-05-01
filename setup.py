# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

import django_pybrowscap

def read(fname):
    """Utility function to read the README file.

    Used for the long_description. It's nice, because now 1) we have a top level
    README file and 2) it's easier to type in the README file than to put a raw
    string in below ...

    """
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='django-pybrowscap',
    version=django_pybrowscap.__version__,
    description='django-pybrowscap is django middleware with support for pybrowscap',
    long_description=read('README.rst'),
    author=u'Vladimír Gorej',
    author_email='gorej@codescale.net',
    url='http://www.codescale.net/en/community#django-pybrowscap',
    download_url='http://github.com/char0n/django-pybrowscap/tarball/master',
    license='BSD',
    keywords = 'browser browscap detection user agent django',
    packages=find_packages('.'),
    package_data = {
        # If any package contains *.csv files, include them:
        'django_pybrowscap.tests': ['data/*.csv']
    },
    install_requires=['django', 'pybrowscap'],
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