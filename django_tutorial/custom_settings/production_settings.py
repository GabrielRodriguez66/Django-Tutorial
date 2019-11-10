import dj_database_url
from .base_settings import *

DEBUG = False

ALLOWED_HOSTS = ['polls-app-tutorial.herokuapp.com', ]

DATABASES['default'].update(dj_database_url.config())
