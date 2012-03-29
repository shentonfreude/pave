from django.core.context_processors import csrf
from django.db.models import Q
from django.forms import Form, CharField, DateField, ModelMultipleChoiceField
from django.forms import SelectMultiple

from django.shortcuts import render_to_response
from django.template import RequestContext

from models import Project, Center, Status

class SearchForm(Form):
    project_id   = CharField(max_length=80, required=False)
    status       = ModelMultipleChoiceField(queryset=Status.objects.all(), required=False,
                                            widget=SelectMultiple(attrs={'size':len(Status.objects.all())}))
    nasa_centers = ModelMultipleChoiceField(queryset=Center.objects.all(), required=False,
                                            label="NASA Centers",
                                            widget=SelectMultiple(attrs={'size':len(Center.objects.all())}))
    date         = DateField(required=False, help_text="MM/DD/YYYY or YYYY-MM-DD")
    date_start   = DateField(required=False, help_text="MM/DD/YYYY or YYYY-MM-DD")
    date_end     = DateField(required=False, help_text="MM/DD/YYYY or YYYY-MM-DD")

def search(request):
    if request.method == 'POST':
        form = SearchForm(data=request.POST)
        if form.is_valid():
            # Form gives us nasa_centers as Center objects, not text strings.
            # We want Centers and Status each to be logical OR, but then ANDed with other criteria.
            q = Q()
            project_id = form.cleaned_data['project_id'].strip()
            if project_id:
                q = q & Q(project_number=project_id)
            nasa_centers = form.cleaned_data['nasa_centers']
            if nasa_centers:
                q = q & Q(nasa_centers__in=nasa_centers)
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
            return render_to_response('project/search_results.html',
                                      {'object_list': projects},
                                      context_instance=RequestContext(request));
    else:
        form = SearchForm()
    return render_to_response('search.html',
                              {'form': form},
                              context_instance=RequestContext(request));


def browse(request, status=None):
    """Show 10 most recent Approved and 10 most recent Closed, with total count of each.
    """
    LIMIT = 5
    approved = Project.objects.filter(status__name="Approved").order_by('announcement_closes').reverse()
    closed = Project.objects.filter(status__name="Closed").order_by('announcement_closes').reverse()
    return render_to_response('project/project_browse.html',
                              {'limit': LIMIT,
                               'approved': approved[0:LIMIT],
                               'approved_num': len(approved),
                               'closed' : closed[0:LIMIT],
                               'closed_num': len(closed),
                               },
                              context_instance=RequestContext(request));

def approved(request):
    """Show all Approved projects
    If we had lots of different statuses, we'd use an option on the url,
    but this is cleaner for the two simple cases.
    """
    approved = Project.objects.filter(status__name="Approved").order_by('announcement_closes').reverse()
    return render_to_response('project/project_browse.html', # reduce, reuse, recycle
                              {'limit': 0,
                               'approved': approved,
                               'approved_num': len(approved),
                               'closed' : [],
                               'closed_num': 0,
                               },
                              context_instance=RequestContext(request));

def closed(request):
    """Show all Approved projects
    If we had lots of different statuses, we'd use an option on the url,
    but this is cleaner for the two simple cases.
    """
    closed = Project.objects.filter(status__name="Closed").order_by('announcement_closes').reverse()
    return render_to_response('project/project_browse.html', # reduce, reuse, recycle
                              {'limit': 0,
                               'approved': [],
                               'approved_num': 0,
                               'closed' : closed,
                               'closed_num': len(closed),
                               },
                              context_instance=RequestContext(request));


