#!/bin/sh

SETTINGS='settings.py'

cat > $SETTINGS <<EOF
DATABASES = {
    'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'test.db',
    },
}

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django_pybrowscap.middleware.PybrowscapMiddleware'
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django_pybrowscap',
)

SECRET_KEY = 'secret_key'
ROOT_URLCONF = 'django_pybrowscap.tests'
EOF

export PYTHONPATH=.
export DJANGO_SETTINGS_MODULE=settings

django-admin.py test django_pybrowscap $@

rm -f $SETTINGS*
rm -f test.db