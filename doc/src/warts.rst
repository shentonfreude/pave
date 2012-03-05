===============
 WARTS IN PAVE
===============

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

Search by Project ID
--------------------

Search by Project ID doesn't remove trailing spaces, so if you search
for "PAVE-12-SSC-002-372 " (e.g., from cut-n-paste) it won't find
anything; you have to enter "PAVE-12-SSC-002-372".

You have to enter the entire Project ID; no partial matching is
done. I don't know if it would be useful to do partial matches.  PAVE
encodes project data into the ID (year, center, office code), which is
generally not a good idea: it means if you edit the object (e.g., to
correct the Center) then the ID is misleading, or has to be changed
(which would break links).

Search by Date and Range
------------------------

The Date Range is not described, especially how it's different than
Specific Date.

Details doesn't always show all fields?
---------------------------------------

PAVE Project Details frequently doesn't show fields "after the fold":
Pay Plan, Series Codes, Grade Levels, NASA Centers.  Is this because
they're somehow marked as "ALL"? Some other reason?

