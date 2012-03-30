==============
 Data Sources
==============

WIMS: Employee Grade Level, Center, Minority Code
=================================================

PAVE is said to query WIMS via DB-Link to their Oracle (?)
database. Two tables are updated in PAVE: `current_employees` and
`static`.  Below, some salient fields from the bowdlerized version in
development on host scutum.

It looks like WIMS does *not* give us email, so we'll have to query
NED, or get a dump from some other source.

current_employees
-----------------

Not all fields listed, just the non-nulls that look useful.

* duty_stn_code: what?
* ofcl_name: first + last
* grade_code: GS level (e.g., 12)
* instl_code: center id, see other tables (e.g., 2100)
* name_first
* name_last
* name_middle
* posn_series_code: GS/OPM job code? (e.g., 0301)
* posn_title_text: (e.g.,CAREER MANAGMENT SPECIALIST)
* pay_plan: GS or something else? (e.g., GS)
* uupic

static
------

* mnrty_code: minority status type? (e.g., C)
* sex: (e.g., F)
* uupic

Connecting to Oracle
--------------------

NB: The 64-bit version of Oracle `instantclient` doesn't work on any
modern OS X; the 32-bit does, but this may make it impossible to
compile into web frameworks that have been built with 64-bit
libraries.

You'd think you could issue a command like::

  sqlplus username/password@host.example.com/sidname

and you'd be wrong::

  SQL*Plus: Release 10.2.0.4.0 - Production on Thu Mar 29 15:49:59 2012
  ERROR:
  ORA-12514: TNS:listener does not currently know of service requested in connect descriptor


No, you have to issue the memorable::

  sqlplus 'username/password@(DESCRIPTION=(ADDRESS_LIST=(ADDRESS=(PROTOCOL=TCP)(HOST=hostname.example.com)(PORT=1521)))(CONNECT_DATA=(SID=sidname)))'

The single-quotes are needed to hide the special characters from the shell.

You better be using this within Emacs or something because there's no
command line history or editing. Welcome to the 1960's. 

You can create a `.tnsnames.ora` (note the leading dot) in your home
directory like::

  mydb = 
    (DESCRIPTION=
      (ADDRESS_LIST=
        (ADDRESS=
          (PROTOCOL=TCP)
          (HOST=hostname.example.com)
          (PORT=1521)))
      (CONNECT_DATA=(SID=sidname))
    )

then you'll be able to invoke like::

  sqlplus mydb

And this will work with Emacs' `sql-oracle` mode as well.


NED: Email
==========

How to query::

  ldapsearch -x -h dir.nasa.gov -b ou=people,dc=nasa,dc=gov "(&(givenName=liteshia)(sn=dennis))"

Interesting attributes from results::

  nasaSupervisor: [employeeNumber elided]
  nasaEmployer: NASA
  nasaIdentityStatus: Active
  roomNumber: 9Z99 [mangled]
  title: IT SPECIALIST (APPSW)
  nasaOrgLevel: 5
  nasaPaidCenter: HQ
  nasaBWOrg: 10  00LM022
  nasaWebTADSParentOrg: LM020
  nasaOrgName: Information Technology and Communications Division
  nasaBuilding: HQ
  mail: [elided]
  nasaPrimaryEmail: [elided]
  nasaDarGroup: HQ Users A - R
  agencyUID: [elided]
  employeeNumber: [elided]
  ou: HQ
  nasaorgCode: LM022

Can we get more attributes if we're authenticate? GS level? other target attrs?

As search of the public directory outside the firewall only gives::

  cshenton@Asylum/source$ ldapsearch -x -h pubdir.nasa.gov -b ou=people,dc=nasa,dc=gov "(&(givenName=liteshia)(sn=dennis))"

  # 626370252, people, nasa.gov
  dn: employeenumber=626370252,ou=people, dc=nasa, dc=gov
  objectClass: nasaperson
  objectClass: inetOrgPerson
  objectClass: organizationalPerson
  objectClass: person
  objectClass: top
  objectClass: sunAMAuthAccountLockout
  givenName: LITESHIA
  sn: DENNIS
  employeeNumber: 626370252
  mail: liteshia.b.dennis@nasa.gov
  initials: BEAMON
  cn: LITESHIA BEAMON DENNIS
  telephoneNumber: 202.358.4778

