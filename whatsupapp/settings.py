import os
import sys
from django.utils.crypto import get_random_string

TEST = 'test' in sys.argv
CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
BASE_DIR = os.path.dirname(CURRENT_PATH)
PREFIX = os.environ.get('PREFIX', '')

# Forces the application to use the prefix, so when we host these apps we don't
# get funny stuff happening at log in.
FORCE_SCRIPT_NAME = PREFIX

# Do not enable debug mode in production!
DEBUG = (os.environ.get('DEBUG', 'False').upper() == 'TRUE')

ADMINS = (
    #('Edward Gomez', 'egomez@lcogt.net'),
)

chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
SECRET_KEY = get_random_string(50, chars)

SESSION_COOKIE_NAME = "whatsup.sessionid"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.environ.get('DB_NAME', ''),
        "USER": os.environ.get('DB_USER', ''),
        "PASSWORD": os.environ.get('DB_PASS', ''),
        "HOST": os.environ.get('DB_HOST', ''),
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.4/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['*']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'UTC'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

STATICFILES_DIRS = []
STATIC_URL = PREFIX + '/static/'

STATIC_ROOT = '/var/www/html/static/'


# #### Upload directory for the proposalsubmit app. Also where proposal PDFs are created
MEDIA_ROOT = os.path.join(CURRENT_PATH, 'media')
MEDIA_URL = PREFIX + '/media/'

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'whatsupapp.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'whatsupapp.wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

INSTALLED_APPS = (
    'whatsup.apps.WhatsupConfig',
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'rest_framework'
)

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework_jsonp.renderers.JSONPRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    )
}

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

COORDS = {
    'ogg': {'lat': 20.7075, 'lon': -156.256111},
    'coj': {'lat': -31.273333, 'lon': 149.071111},
    'lsc': {'lat': -30.1675, 'lon': -70.804722},
    'elp': {'lat': 30.67, 'lon': -104.02},
    'sqa': {'lat': 20.7075, 'lon': -156.256111},
    'cpt': {'lat': -32.38, 'lon': 20.81},
    'tfn': {'lat': 28.3, 'lon': -16.51},
}

if not CURRENT_PATH.startswith('/var/www'):
    try:
        from .local_settings import *
    except ImportError as e:
        if "local_settings" not in str(e):
            raise e
