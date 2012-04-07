import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'pave.settings'

import django.core.handlers.wsgi as w
application = w.WSGIHandler()
