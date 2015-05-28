from settings import *

ADMINS = (
      ('Edward Gomez', 'egomez@lcogt.net'),
)

MANAGERS = ADMINS

DEV_DBFILE = CURRENT_PATH + '/whatsup.db'
DEV_DB_BACKEND = 'django.db.backends.sqlite3'

DATABASES = {
    'default':     {
             'ENGINE'    : 'django.db.backends.mysql' if PRODUCTION else DEV_DB_BACKEND,
             'NAME'      : 'whatsup' if PRODUCTION else DEV_DBFILE,
             'USER'      : 'citsci' if PRODUCTION else '',
             'PASSWORD'  : 'aster01d' if PRODUCTION else '',
             'HOST'      : 'db01sba' if PRODUCTION else '',
             'OPTIONS'   : {'init_command': 'SET storage_engine=INNODB character set utf8'} if PRODUCTION else {},
             }
}