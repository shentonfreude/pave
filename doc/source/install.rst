Installation
============

Virtualenv, Sphinx, Django
--------------------------

Something like this::

  /usr/local/python/2.7/bin/virtualenv --no-site-packages --distribute pave
  cd pave
  source bin/activate
  pip install sphinx
  pip install django
  git clone https://github.com/shentonfreude/pave.git
  cd pave

Make the docs
-------------

The document source is in doc/source and you can format them to HTML
and epub with `sphinx`::

  pushd doc/
  make html epub
  popd

The HTML documents are now in doc/build/html/ and the epub format is
in doc/build/epub/.

Get the Django application running
----------------------------------

Seems like one-too-many layers, but::

  cd pave

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

-------------------------------------
ON Ubuntu cloud VM server:
-------------------------------------
(assumes virtualenv is already available; otherwise:
  sudo agt-get install git
  sudo apt-get install python-devtools
  sudo easy_install virtualenv)

1  virtualenv --no-site-packages --distribute pave
2  cd pave
3  source bin/activate
4  pip install sphinx
5  pip install django
6  history
7  git clone https://jhfrench@github.com/shentonfreude/pave.git 
8  cd pave
9  pushd doc/
10  make html epub
11  popd
12  cd pave
13  ./manage.py syncdb
14  ./manage.py loaddata fixtures/*.json
15  ./manage.py runserver 0.0.0.0:8080
16  ./manage.py runserver 0.0.0.0:8081
