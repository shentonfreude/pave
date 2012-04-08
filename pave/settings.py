# See hints in: https://github.com/kencochrane/django-cms-stackato/blob/master/mycms/settings.py

import os

#PROJECT_PATH = os.path.abspath(os.path.split(__file__)[0])
# better? from kencochrane
PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))

###print "###settings.py PROJECT_PATH=%s" % PROJECT_PATH

# Django settings for pave project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

## Pull in Stackato's production settings
## This example demonstrates how to access the bound MySQL service
import os
if 'VCAP_SERVICES' in os.environ:
    import json
    vcap_services = json.loads(os.environ['VCAP_SERVICES'])
    # XXX: avoid hardcoding here
    ## MYSQL:
    db_srv = vcap_services['mysql-5.1'][0]
    ## POSTGRES: db_srv = vcap_services['postgresql-8.4'][0]
    cred = db_srv['credentials']
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': cred['name'],
            'USER': cred['user'],
            'PASSWORD': cred['password'],
            'HOST': cred['hostname'],
            'PORT': cred['port'],
            }
        }
else:
  DATABASES = {
      'default': {
          # Local development:
          'ENGINE': 'django.db.backends.sqlite3',
          'NAME': os.path.join(PROJECT_PATH, "db/pave.sqlite3"),  # Or path to database file if using sqlite3.
          #
          # Heroku: 'ENGINE': 'django.db.backends.postgresql_psycopg2',
          #'NAME': 'pave',
          'USER': 'pave',                      # Not used with sqlite3.
          'PASSWORD': 'PaveThePlanet',                  # Not used with sqlite3.
          'HOST': '/tmp',                      # Need /tmp for Postgres running as my username; Set to empty string for localhost. Not used with sqlite3.
          'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
      }
  }

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

####django.core.exceptions.ImproperlyConfigured:
#### The STATICFILES_DIRS setting should not contain the STATIC_ROOT setting


# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
###os.path.join(PROJECT_PATH, "static") # at what level? do I need to pre-create? CONFLICTS 
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
# 2012-04-07 conflicts with same setting of STATIC_ROOT?? even if commented
STATICFILES_DIRS = (
    os.path.join(PROJECT_PATH, "static"), # put /css/ and /js/ under this
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '37z-jbx@$)zhcdn(5s28ikn)xp4^c9u3#=7gspy-bz$5lple5b'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
#    'django.contrib.auth.middleware.RemoteUserMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
#    'django.contrib.auth.backends.RemoteUserBackend',
)

ROOT_URLCONF = 'pave.urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, "templates"),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    # For django-bootstrap-form:
    'bootstrapform',
    'project',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
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
