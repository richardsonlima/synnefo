import os
os.environ['SYNNEFO_SETTINGS_DIR'] = '/etc/synnefo-test-settings'

from synnefo.settings import *

DEBUG = False
TEST = True

DATABASES = {
    'default': {
        #'ENGINE': 'django.db.backends.sqlite3',
        #'NAME': '/tmp/synnefo_test_db.sqlite',

        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'pithos',
        'USER': 'postgres',
        'PORT': '5432',
    }
}

LOGGING_SETUP['handlers']['console']['level'] = \
    os.environ.get('SYNNEFO_TESTS_LOGGING_LEVEL', 'WARNING')

LOGIN_URL = 'http://host:port/'


SOUTH_TESTS_MIGRATE = bool(int(os.environ.get('SOUTH_TESTS_MIGRATE', True)))

ASTAKOS_IM_MODULES = ['local', 'shibboleth']

CYCLADES_PROXY_USER_SERVICES = False
PITHOS_PROXY_USER_SERVICES = False
