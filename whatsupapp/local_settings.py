import os

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': CURRENT_PATH + '/whatsup.db',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'OPTIONS': {},
    }
}

STATIC_ROOT = '/home/egomez/public_html/static/whatsup'
