=============
 PAVE README
=============

Purpose
=======

Provide authenticated users a way to advertise short-term "project"
opportunities; allow unauthenticated people to view and apply for
them.

Project Management
==================

Project opportunities specify skill sets, GS levels, NASA Center for work, (?)
eligible Centers, start- and stop-dates, descriptions, etc.

Presumably each Project offeror controls their own projects, they
cannot affect projects which they do not own, which they did not list.

A project can be awarded to an applicant and closed, closed without an
applicant, or canceled.


Applicants
==========

Applicants do not need to authenticate to *browse* and *search* projects.

Search can multi-select Center (which? destination or employee?),
search by date or date-range, lookup by Project ID, and finer by
projects that are Announced, Closed, or Canceled.

Once a project is selected, the applicant enters their name and is
verified by NASA Directory lookup. 

They then ...


WARTS IN PAVE
=============

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