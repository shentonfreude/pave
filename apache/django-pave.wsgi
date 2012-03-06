import os, sys
import site

#sys.path.append("/Users/chris/Projects/hq/core/pave/lib/python2.7/site-packages")

# Add virtualenv python site-packages to path so it can get Django
site.addsitedir("/Users/chris/Projects/hq/core/pave/lib/python2.7/site-packages")


# Avoid permission denied
os.environ['PYTHON_EGG_CACHE'] = '/tmp'

# Our project's not on PYTHONPATH so:
sys.path.append("/Users/chris/Projects/hq/core/pave/pave")
sys.path.append("/Users/chris/Projects/hq/core/pave/pave/pave")

# How to make it different than development, e.g., DEBUG=False
os.environ['DJANGO_SETTINGS_MODULE'] = 'pave.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()