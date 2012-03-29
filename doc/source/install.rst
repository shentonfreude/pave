==============
 Installation
==============

Install on Development Machine
==============================

Get the code
------------

Clone the repo into a new ./pave/ directory and change into it::

  git clone git@github.com:shentonfreude/pave.git
  cd pave

Virtualenv
----------

Create and activate a virtualenv in this directory; note the trailing dot::

  /usr/local/python/2.7.2/bin/virtualenv --no-site-packages --distribute .
  source bin/activate

Install django, sphinx
----------------------

Use virtualenv's `pip` to install django framework and sphinx documentation tools::

  pip install django
  pip install sphinx

Build docs
----------

The document source is in doc/source and you can format them to HTML
and epub with `sphinx`::

  pushd doc
  make html epub
  popd

You can now find nicely formatted docs in the pave/doc/html/ and
pave/doc/epub/ directories.

Initialize Django DB
--------------------

Use the Django management tool to sync the database to the
application's model definitions; it will create the database if it
doesn't exist. The location is specified in the settings.py file::

  cd pave
  ./manage.py syncdb

Load fixture data
-----------------

Now  load up data about Centers, OMB job classification codes, and
sample data from an initial attempt at importing data from production
PAVE::

  ./manage.py loaddata fixtures/*.json

(Note that if you change your models/schema, a syncdb won't *change*
existing table schemas; you'll need to wipe the .sqlite DB file and
reload fixtures. There are 'evolution' mechanisms and we could dump
and reload via fixtures.)

Run it
------

Run the app with the development server::

  ./manage.py runserver



On Ubuntu cloud VM server
=========================

Assumes virtualenv is already available; otherwise::

  $ sudo agt-get install git
  $ sudo apt-get install python-devtools
  $ sudo easy_install virtualenv

Then::

  $  git clone https://jhfrench@github.com/shentonfreude/pave.git
  $  cd pave
  $  virtualenv --no-site-packages --distribute .
  $  source bin/activate
  $  pip install django
  $  pip install sphinx
  $  pushd doc/
  $  make html epub
  $  popd
  $  cd pave
  $  ./manage.py syncdb
  $  ./manage.py loaddata fixtures/*.json
  $  ./manage.py runserver 0.0.0.0:8081
