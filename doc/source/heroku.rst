========
 Heroku
========

Heroku is a Platform-as-a-Service (PaaS) which can be used to deploy
Django apps without the fuss of command line sysadm.  It can scale out
web front ends as it uses backend Postgres DB for persistence: no
individual nodes hold data.

Create our local Postgres DB
============================

Since Heroku uses Postgres, we'll set our development up the same way
to ensure we can run with it locally. Create the DB, user, and grant
access::

  $ sudo -u postgres createdb pave

  $ sudo -u postgres createuser pave
  Shall the new role be a superuser? (y/n) n
  Shall the new role be allowed to create databases? (y/n) n
  Shall the new role be allowed to create more new roles? (y/n) n

  $ sudo -u postgres psql
  postgres=# alter user pave with encrypted password 'PaveThePlanet';
  ALTER ROLE
  postgres=# grant all privileges on database pave to pave;
  GRANT

settings.py
===========

Edit settings.py to use this::

  DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.postgresql_psycopg2',
          'NAME': 'pave',
          'USER': 'pave',                      # Not used with sqlite3.
          'PASSWORD': 'PaveThePlanet',                  # Not used with sqlite3.
          'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
          'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
      }
  }

Recreate DB on Schema Change
============================

I found when importing some fixtures/* files that some of my model
definitions had fields too short to hold the fixture data. It turns
out these fields were pathalogical cases from Donnie's security
testing.  SQLite does *not* enforce field size limits so we never
noticed this before.

I had to edit the models.py to increase the field size to
accommodate. I then had to re-create the application's database so
that we could do a fresh `syncdb`::

  $ sudo -u postgres dropdb   pave
  $ sudo -u postgres createdb pave

Then do the normal `syncdb` and `loaddata` again.

Push to Heroku
==============

We push into a branch named `master` at Heroku and it does its magic.
If we're trying to push a different branch, we must specify Heroku's
name `master` as a destination::

  $ git push heroku cs/feature.heroku:master


