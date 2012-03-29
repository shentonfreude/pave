==========
 Features
==========

These are features gleaned from existing PAVE, and filed under our
target 1.0. For post-1.0 we'll work with the customer, and perhaps
take ideas from the .doc file.

1.0
===

Inferred from unauthenticated public PAVE
-----------------------------------------

* Home: a single clear home page with quick links to actions
* Browse: unauthenticated: show most recent open and closed projects
* Search: by (full) Project ID, Status, Center, Date (one, or open & closed)
* Details: display all public attributes
* Apply:
  - validate center, name
  - gather email, phone
  - gather supervisor contact, comments, experience, anticipated gain
* Publish: [don't have visibility into this process yet]
  - authenticate (eAuth, ideally)
  - create announcement
  - select criteria for applicant
  - review number of applicants selected by criteria
  - submit for notification by email
* Notify: send opportunity by email to individuals by: multiple centers, multiple GS levels
* Migrate: existing data from old into new PAVE
* Provide automated tests suite: unit, functional, integration tests

Inferred from database schema analysis
--------------------------------------

* Track login history: date, userid, method and success; submit
* Different "user security levels": applicant, ...; 1, 2, 3, 4
* Survey (what?)
* Track which announcements were sent to which employees?
* Opt-out: existing table only lists devs


1.1 
===

Tanya's email to Liteshia summarizing 01/11/2012 meeting
--------------------------------------------------------

* Reporting capabilities on announcements (details?)
* Capture candidate selection
* Info on announcement and candidates not in system sufficiently to answer Data Calls

From PAVE Meeting Minutes 09/16/2011
------------------------------------

* Queue email delivery when over some limit, send during non-production hours
* Comment out Minority Code so users can apply (details?)
* 500 Character wrap issue (details?)
* Automated deployment
* Automated testing

1.2 New Requirements
====================

From PAVE Meeting Minutes 09/16/2011.

* Update with new Organization IDs (can we query a live feed for this,
  or do it manually in-app?)
* new report with Organizational ID and close positions
* Print individual applicants who have applied
* update applicant info fields
* all users should have access as Office administrator role (not unauthenticated?)
* review application roles to ensure duties and who is assigned
* add email notifications to send to Rhonda (better: a BCC person defined in-app)
* consistent and more efficient checkboxes
* ability to attach resumes
* update message when user doesn't meet position criteria
* update (OPM?) job series listing (from live feed, or in-app?)
* Update reports, create new reports (details?)

1.3 HITSS Identified Improvements
=================================

From doc attached to PAVE Meeting Minutes 09/16/2011.

Application Functionality and User Integration
----------------------------------------------

* Remove lock-out of applicants if they fail to apply 3 times
* Improve integration with WIMS, need higher frequency; recommend HQTS [don't believe it has Grade level, Job code]
* Announcements should link directly to Project description, not Welcome screen
* Improve applicant is civil servant verification logic
* Improve navigation and reduce pop-ups
* Consolidate report selection/creation
* Automatically maintain HQ Office and Organizations [what feeds?]
* Improve search: partial-text on announcement ID [better, on more fields]

Application UI
--------------

* Improve User Interface [oh, yeah -- we got that!]

Code and DB Development
-----------------------

* Re-Develop using framework, improve DB structure [this reimplementation does just that!]
  - Reduce the amount of bugs, within the application caused by the use of outdated methods, algorithms or functions.
  - It will allow for faster and easier development of future updates.
  - It will allow for scalability of changes.
  - It will improve how data is organized in the database, reducing the size of queries that may take up unnecessary resources.
  - Provides a platform that all developers are familiar with, so anyone can work on it. I.e. if someone is out sick.

1.4
===

Review "PAVE Requirements for Analysis of Alternatives" document to
determine what's not yet implemented, and what features are requested
or needed by users. There are 79 unique features identified in that
document.
