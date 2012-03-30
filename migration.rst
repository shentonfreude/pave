===========
 Migration
===========

Database
========

We'll have to migrate existing projects and metadata from the Oracle database.
Schema spelunking, fun.

Issues
======

URLs
----

The shape of URLs will change.  Instead of the un-RESTful ColdFusion way:

  /pave/pave_user_main_pave_form_view.cfm?p_key=PAVE-12-HQ-DM000-390

We'll use a RESTful approach that's hierarchical based on Year,
Center, and Office ID, and the final path will be a human readable
form of the job title::

  /project/2012/hq/dm000/policy-analyst-2

This allows us to provide listings of all opportunities within a Year,
at a Center, and within an Organization::

  /project/2012/
  /project/2012/hq/
  /project/2012/hq/dm000/

But this will break existing links and bookmarks.

More critically it will break links already sent in mail which refers
to the existing site.  Is this an issue? I read a request to have
email links point to the actual project instead of the Welcome page so
maybe it's not an issue yet.

Perhaps we could put a handler that catches old form URLs and
redirects permanently to the new form.  It would have to get the
project_number and query for it to get the new URL.

Slugs
-----

We'll have to create new slugs from old project_numbers so that
new-style URLs work.

Project Numbers
---------------

Apparently, people are used to referring to projects by their
info-encoded name, e.g., "PAVE-12-DM000-390".

Actually, the P_KEY field is *inconsistent*; sometimes with Center,
other times like, apparently using office `code` but not Center::

  PAVE-05-LA-2175
  PAVE-03-S-1488

We see the pave.p_key getting defined in dbx_pave_ann.cfm::

	<cfquery name="qry_ref_no_cs" datasource="#datasource#">
		SELECT
		'PAVE' || '-' || TO_CHAR(sysdate,'yy') || '-' || '#TRim(form.cent)#' || '-' ||
		<cfif form.code eq ''>
		'#TRim(qry_org.org)#'
		<cfelse>
		'#TRim(form.code)#'
		</cfif>
		 || '-' || HRTS_FORM_52.nextval AS ref_no
		FROM DUAL
	</cfquery>

We could just make the number the plain old id, e.g., "390" since that
uniquely identifies it.

How do we reconcile Project Number and URL in the new format? If the URL is:: 

  /2012/hq/dm000/policy-analyst-2

the Project Number might be::

  2012-hq-dm000-policy-analyst-2

but that seems painful.

To accommodate a project whose Center or Office changes, we probably
should just give out the unique ID (primary key) as the Project
Number.  That way browsing by /yyyy/cc/ooooo/ still works even if a
project moves hierarchies. Not sure.



