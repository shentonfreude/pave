=============
 PAVE README
=============

Purpose
=======

Provide authenticated users a way to advertise short-term "project"
opportunities; allow unauthenticated people to view and apply for
them.

Project Management
------------------

Project opportunities specify skill sets, GS levels, NASA Center for work, (?)
eligible Centers, start- and stop-dates, descriptions, etc.

Presumably each Project offeror controls their own projects, they
cannot affect projects which they do not own, which they did not list.

A project can be awarded to an applicant and closed, closed without an
applicant, or canceled.


Applicants
----------

Applicants do not need to authenticate to *browse* and *search* projects.

Search can multi-select Center (which? destination or employee?),
search by date or date-range, lookup by Project ID, and finer by
projects that are Announced, Closed, or Canceled.

Once a project is selected, the applicant enters their name and is
verified by NASA Directory lookup. 

They then ...


Installation
============

Virtualenv, Django
------------------

Something like this::

  /usr/local/python/2.7/bin/virtualenv --no-site-packages --distribute pave
  cd pave
  source bin/activate
  pip install django
  git clone .../pave.git

Sync the DB to the model::

  ./manage.py syncdb

(Note that if you change your models/schema, a syncdb won't *change*
existing table schemas; you'll need to wipe the .sqlite DB file and
reload fixtures. There are 'evolution' mechanisms and we could dump
and reload via fixtures.)

Load fixture data (centers, job codes, etc)::

  ./manage.py loaddata fixtures/*.json



WARTS IN PAVE
=============

Slow
----

Even returning from Search Results to Search Query form takes 5-10 seconds.

Free-form text input, unvalidated
---------------------------------

We can't do proper searches on unstructured input. The listings
overview has inconsistent use of Series, Grades, Centers:

Grades examples:
- 11,13,14,15-
- 13-15
- 7 - 9

Series examples:
- 0201 , ,
- 0301,0318,0341,0343 , ,
- All Series

Centers examples:
- SSC
- GSFC, HQ
- XX

Inconsistent Search result format
---------------------------------

If we query PAVE for Closed, it shows listing in different format than
normal listing, with a Closed PAVE Projects header TBD::

  project_id, position_title, start_date, closed_date, canceled date
  brief description,                                        CANCELED


If we query for Canceled projects it shows a similar format to above
with a "Canceled PAVE Projects" header::

  project_id, position_title, start_date, closed_date, canceled date
  brief description,                                        CANCELED


If we query for Closed or Canceled projects we get no header, but the
CLOSED or CANCELED status are shown under the date of closure or
cancelation::

  project_id, position_title, start_date, closed_date, canceled date
  brief description,                      CLOSED     or     CANCELED

Perhaps we should just show the status as an item? Possibly color
coded? Or group by status?
