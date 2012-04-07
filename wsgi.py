import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'hellodjango.settings'

import django.core.handlers.wsgi as w
application = w.WSGIHandler()
