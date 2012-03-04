===========
 TODO/Done
===========

To Do
=====

* Browse: provide links to browse options like PAVE's All Open or All Closed
* Browse: make display table a reusable template, not cut-paste for Approved, Closed
* Search: date fields should provide picker like Admin UI does (why doesn't it?)
* Display Job Series in Projects List as just the number, not description; while leaving it descriptive in the Admin UI
* Sane defaults, e.g., Status=Approved, PayCode=GS
* Should we use the same 2-different-templates for Browse and Search like PAVE does?
* Admin date input doesn't accept: 03/16/2012 -- what does it want? 2012-03-02
* Admin: selector for All NASA Centers, All Job Code Series (or use Empty as signifier; how affects search?)
* Generate project_number: PAVE-yyyy-center-office-####
* Apply for Project: center and name verificaiton, supervisor info, justification: needs LDAP access ("fieldset"?)
* Apply: LDAP lookup to verify first, last, center.
* CSV, JSON output
* Social Media: post to FaceBook, Twitter, etc.

Done
====

CSS
---

It's progressing. See static/css/base.css.

How to load images (e.g., <imr src=...>) and css
------------------------------------------------

settings.py::

  PROJECT_PATH = os.path.abspath(os.path.split(__file__)[0])
  TEMPLATE_DIRS = (
      os.path.join(PROJECT_PATH, "templates"),
  )
  STATICFILES_DIRS = (
      os.path.join(PROJECT_PATH, "static"), # put /css/ and /js/ under this
  )

templates/base.html::

  <head>
    <link href="{{STATIC_URL}}/css/base.css" rel="stylesheet" type="text/css" />
  </head>
  <body>
    <header id="banner">
      <img src="{{STATIC_URL}}/img/paveheader1.gif" />
    </header>

static assets in:
- .../pave/static/css/base.css
- .../pave/static/img/paveheader1.gif
- .../pave/static/js/*

Menubar style horizontal
------------------------

base.css::
  nav#menubar ul{
      background-color: #99c6e7;  /*original PAVE color*/
      width: 100%;
      float: left;
      list-style: none;
      margin: 0 0 3em 0;
      padding: 0;
      border-top: 1px solid red;
      border-bottom: 2px solid #0183b5; /*worm-logo earth blue*/
  }
  nav#menubar li {
      float: left;
  }
  nav#menubar li a {
      display: block;
      padding: 8px 15px;
      text-decoration: none;
      font-weight: bold;
      border-right: 1px solid #0183b5; /*worm-logo earth blue*/
      }

CSRF for forms
--------------

project/views.py::

  from django.core.context_processors import csrf
  from django.shortcuts import render_to_response
  from django.template import RequestContext
  ...
      return render_to_response('search.html',
                                {'form': form},
                                context_instance=RequestContext(request));

search.html::

  <form id="search" method="POST" action=".">{% csrf_token %}


URL template references to urls.py names
----------------------------------------

Use {% url ... %} template tag in base.html::

  <li><a href="{% url home %}">Home</a></li>
  <li><a href="{% url projects %}">Browse</a></li>
  <li><a href="{% url search %}">Search</a></li>


Multiselect fields must use ManyToManyField(Choices)
----------------------------------------------------

Define foreign models and link to them in models.py::

  class Project(Model):
      ...
      series_codes		= ManyToManyField(JobCode)
      grade_levels		= ManyToManyField(GradeLevel)
      nasa_centers		= ManyToManyField(Center, related_name='Centers')
      owner                       = ForeignKey(User, unique=False, blank=False)
      applicant                   = ForeignKey(Applicant, unique=False, blank=True, null=True)

Cycle bars on table displays
----------------------------

In base.css::
  table tr.odd {
      background-color: #dddddd;
  }
  table tr.even {
      background-color: #eeeeee;
  }

In project_list.html::

  {% for project in object_list %}
  <tr class="{% cycle 'odd' 'even' %}">


Link project_listing to individual project details
--------------------------------------------------

project/urls.py::

    url(r'^(?P<object_id>\d+)/$',  object_detail, info_dict, name="details"),

project_list.html::

      <td><a href="{% url details object_id=project.id %}">{{project.project_number}}</a></td>

Detailed listing
----------------

See project_details.html


Create sample Closed and Cancelled jobs, Export sample jobs as fixture
----------------------------------------------------------------------

We manually cut-paste Projects from PAVE into Django PAVE to create content.

In a virtual environment at /Users/cshenton/Projects/core/pave/pave::

 ./manage.py dumpdata --format=json --indent=4 --exclude=auth --exclude=admin project.project > fixtures/project_project.json

Then we can load all the fixtures with::

  ./manage.py loaddata fixtures/*.json

Make Objectives a TextField (bigger)
------------------------------------

In models.py, change CharField(max_length=80,...) to::

    objectives                  = TextField(max_length=2000, blank=True)
    skill_mix                   = TextField(max_length=2000, blank=True)

Add Cancel Date and Cancel Reason to project
--------------------------------------------

Add to models.py::

  cancel_date                 = DateField(blank=True, null=True, help_text="YYYY-MM-DD")
  cancel_reason               = TextField(max_length=2000, blank=True)

Add cancel_date to each project in fixtures/project_project.json::

            "cancel_date": null,
            "cancel_reason": "",

Wipe the DB, syncdb, and reload the fixtures.

Search: do query based on form input, return results using same project_list.html
---------------------------------------------------------------------------------

We have to start with an empty query and build it up based on which
fields are populated in the search form; we can't have a hard-coded
query on (say) Center if the user didn't enter a Center. Center and
Status are multiselect so those values are logical-ORed, but we
connect each field with a logical AND. From project/views.py::

            q = Q()
            project_id = form.cleaned_data['project_id'].strip()
            if project_id:
                q = q & Q(project_number=project_id)
            nasa_centers = form.cleaned_data['nasa_centers']
            if nasa_centers:
                q = q & Q(nasa_centers__code__in=nasa_centers)
            #import pdb; pdb.set_trace()
            status = form.cleaned_data['status']
            if status:
                q = q & Q(status__in=status)
            date = form.cleaned_data['date']
            if date:
                q = q & Q(project_starts__lte=date) & Q(project_ends__gte=date)
            else:
                date_start = form.cleaned_data['date_start']
                date_end   = form.cleaned_data['date_end']
                if date_start and date_end:
                    q = q & Q(project_starts__lte=date_start) & Q(project_ends__gte=date_end)
            projects = Project.objects.filter(q)

In the above there's a problem: our first version of the search form
populated the Center select field from choices=((1000,"HQ"), ...)
tuples, and the form gave us the Center *code* which we then queried
for.  Now we're populating the form with a ModelMultipleCoiceField and
queryset is the Center model, so the form now gives us full-on Center
objects. Now that portion of our query is more simple and robust::

            if nasa_centers:
                q = q & Q(nasa_centers__in=nasa_centers)

It was dumb luck that the Status worked -- I didn't try to explicitely
force the query to use its name and it "just worked". See next section.

Search form should get choices from DB, not from constants.py file
------------------------------------------------------------------

Instead of MultipleChoiceField and 'choices', use
ModelMultipleChoiceField and 'queryset' into the Model we want to
populate from::

  from django.forms import Form, CharField, DateField, ModelMultipleChoiceField

  class SearchForm(Form):
      ...
      status       = ModelMultipleChoiceField(queryset=Status.objects.all(), required=False)
      nasa_centers = ModelMultipleChoiceField(queryset=Center.objects.all(), required=False)

Specific field types like EmailField
------------------------------------

In https://docs.djangoproject.com/en/dev/ref/models/fields/, there's
an EmailField, but no field for phone numbers or other more specific
things. In models.py::

  class Applicant(Model):
      ...
      email                       = EmailField(max_length=80)
      project_starts		= DateField(help_text="YYYY-MM-DD")


Browse: show "recent" Approved, Closed Projects; what to sort on?
-----------------------------------------------------------------

I'm guessing we're sorting on the Announcement Closing Date, in
reverse order. We do a simple query, order it, reverse it, then limit
what we pass to the template. In view.py browse()::

    LIMIT = 2
    approved = Project.objects.filter(status__name="Approved").order_by('announcement_closes').reverse()
    closed = Project.objects.filter(status__name="Closed").order_by('announcement_closes').reverse()
    return render_to_response('project/project_browse.html', # reduce, reuse, recycle
                              {'limit': LIMIT,
                               'approved': approved[0:LIMIT],
                               'approved_num': len(approved),
                               'closed' : closed[0:LIMIT],
                               'closed_num': len(closed)
                               },
                              context_instance=RequestContext(request));

