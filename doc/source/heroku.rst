========
 Heroku
========

Heroku is a Platform-as-a-Service (PaaS) which can be used to deploy
Django apps without the fuss of command line sysadm.  It can scale out
web front ends as it uses backend Postgres DB for persistence: no
individual nodes hold data.

Create our local Postgres DB
============================

Install PostgreSQL on OS X
--------------------------

To develop on Mac, install PostgreSQL; I use the HomeBrew package
management system::

  brew install postgresql

Per HomeBrew's final instructions, we'll let Launchd run it from a
config in our home directory; it runs as your own username with the
specified config file::

  mkdir -p ~/Library/LaunchAgents
  cp /usr/local/Cellar/postgresql/9.1.2/org.postgresql.postgres.plist ~/Library/LaunchAgents/
  launchctl load -w ~/Library/LaunchAgents/org.postgresql.postgres.plist

We'll initialize the database, as our own user, but we'll tell it to
use "utf-8" encoding instead of the default (why, for the love of
dog?) ASCII::

  initdb --encoding=utf-8 /usr/local/var/postgres

If you install like the above, you do *not* need to use "sudo -u
postgres ..." in the following commands; if you deploy on Linux, you
probably installed PostgreSQL as a system daemon so will need this.

Create DB for PAVE that Heroku will Use
---------------------------------------

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
          'USER': 'pave',              # Not used with sqlite3.
          'PASSWORD': 'PaveThePlanet', # Not used with sqlite3.
          'HOST': '/tmp',              # Set to empty string for localhost. Not used with sqlite3.
          'PORT': '',                  # Set to empty string for default. Not used with sqlite3.
      }
  }

The HOST='/tmp' is needed if you're running PostgreSQL as yourself, an
unprivileged user; the daemon will create its socket there, where you
can write. If you're running as a system daemon process with
privileges, the default Host='' creates the socket under the '/var'
directory, which mortal users cannot write to.

Using '/tmp' won't hurt anything for priv users running locally, nor
for Heroku which overwrites this magically when it deploys.

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

You must commit your code to your local git repo so it can be pushed
to Heroku.

Now create a new application::

  $ heroku create --stack cedar

It will finish and tell you a DNS name to which you'll be able to
connect, and will edit your .git/config file to add Heroku as a new
remote, something like::

  [remote "heroku"]
          url = git@heroku.com:furious-beach-2481.git
          fetch = +refs/heads/*:refs/remotes/heroku/*

We push into a branch named `master` at Heroku and it does its magic.
If we're trying to push a *from* a different branch name, we must
specify Heroku's name `master` as a destination::

  $ git push heroku cs/feature.heroku:master

Note that you need to commit your local changes to your repo first,
else the changes won't be sent to Heroku.

It will output the build process, like::

  Warning: Permanently added the RSA host key for IP address '50.19.85.132' to the list of known hosts.
  Counting objects: 11, done.
  Delta compression using up to 8 threads.
  Compressing objects: 100% (6/6), done.
  Writing objects: 100% (6/6), 660 bytes, done.
  Total 6 (delta 5), reused 0 (delta 0)

  -----> Heroku receiving push
  -----> Python/Django app detected
  -----> Preparing virtualenv version 1.7
         New python executable in ./bin/python
         Installing distribute.............................................................................................................................................................................................done.
         Installing pip...............done.
  -----> Activating virtualenv
  -----> Installing dependencies using pip version 1.0.2
         Downloading/unpacking Django==1.3.1 (from -r requirements.txt (line 3))
         ...
         Successfully installed Django Jinja2 Pygments Sphinx django-bootstrap-form docutils psycopg2
         Cleaning up...
  -----> Injecting Django settings...
         Injecting code into pave/settings.py to read from DATABASE_URL
  -----> Discovering process types
         Procfile declares types         -> (none)
         Default types for Python/Django -> web
  -----> Compiled slug size is 12.5MB
  -----> Launching... done, v4
         http://furious-beach-2481.herokuapp.com Deployed to Heroku

  To git@heroku.com:furious-beach-2481.git
   * [new branch]      cs/feature.heroku -> master


Sync the DB, Load the Data
==========================

For these, you have to specify the full path relative to your app's
`manage.py` and the `fixtures` data::

 $ heroku run python pave/manage.py syncdb

 $ heroku run python pave/manage.py loaddata pave/fixtures/"*.json"

