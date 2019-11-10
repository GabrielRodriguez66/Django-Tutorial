import dj_database_url
from ..settings import *

DEBUG = False

ALLOWED_HOSTS = ['polls-app-tutorial.herokuapp.com', ]

DATABASES['default'].update(dj_database_url.config())
