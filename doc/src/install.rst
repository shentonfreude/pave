Installation
============

Virtualenv, Django
------------------

Something like this::

  /usr/local/python/2.7/bin/virtualenv --no-site-packages --distribute pave
  cd pave
  source bin/activate
  pip install django
  pip install sphinx
  git clone .../pave.git

Sync the DB to the model::

  ./manage.py syncdb

(Note that if you change your models/schema, a syncdb won't *change*
existing table schemas; you'll need to wipe the .sqlite DB file and
reload fixtures. There are 'evolution' mechanisms and we could dump
and reload via fixtures.)

Load fixture data (centers, job codes, etc)::

  ./manage.py loaddata fixtures/*.json

Run the app with the development server::

  ./manage.py runserver

