import os, sys
from os.path import abspath, dirname, join
import site

PROJECT_DIR  = abspath(dirname(dirname(__file__)))
# Gives the directory above this one, in my case:
# /Users/chris/Projects/hq/core/pave/pave

# Add python virtualenv site-packages to path so it can get Django
VIRTUALENV_DIR = abspath(join(PROJECT_DIR, '..', 'lib', 'python2.7', 'site-packages'))
#print "##django-pave.wsgi: VIRTUALENV_DIR=%s" % VIRTUALENV_DIR
site.addsitedir(VIRTUALENV_DIR)

# Avoid permission denied
#os.environ['PYTHON_EGG_CACHE'] = '/tmp'

# Our project's not on PYTHONPATH so add them;
# why do I need to add both? Swedish Chef says "bjork bork bork!"
sys.path.append(PROJECT_DIR)               #.../pave/pave
sys.path.append(join(PROJECT_DIR, 'pave')) #.../pave/pave/pave

# How to make it different than development, e.g., DEBUG=False ?
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()