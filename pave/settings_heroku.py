from settings import *

DATABASES = {
    'default': {
        # ENGINE: Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        #'ENGINE': 'django.db.backends.sqlite3',
        #'NAME': os.path.join(PROJECT_PATH, "db/pave.sqlite3"),  # Or path to database file if using sqlite3.
        #
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'pave',
        'USER': 'pave',                      # Not used with sqlite3.
        'PASSWORD': 'PaveThePlanet',                  # Not used with sqlite3.
        'HOST': '/tmp',                      # Need /tmp for Postgres running as my username; Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}
