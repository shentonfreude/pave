Installation
============

Virtualenv, Django
------------------

Something like this::

  /usr/local/python/2.7/bin/virtualenv --no-site-packages --distribute pave
  cd pave
  source bin/activate
  pip install sphinx
  pip install django
  git clone .../pave.git

Make the docs
-------------

The document source is in doc/source and you can format them to HTML
and epub with `sphinx`::

  pushd docs/
  make html epub
  popd

The HTML documents are now in doc/build/html/ and the epub format is
in doc/build/epub/.

Get the Django application running
----------------------------------

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

