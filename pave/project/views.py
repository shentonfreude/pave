from django.core.context_processors import csrf
from django.db.models import Q
from django.forms import Form, CharField, DateField, ChoiceField, MultipleChoiceField
from django.shortcuts import render_to_response
from django.template import RequestContext

from constants import center_codes, project_statuses
from models import Project

class SearchForm(Form):
    project_id = CharField(max_length=80, required=False)
    status = MultipleChoiceField(required=False, choices=project_statuses)
    nasa_centers = MultipleChoiceField(required=False, choices=center_codes)
    date = DateField(required=False)
    date_start = DateField(required=False)
    date_end = DateField(required=False)

def search(request):
    if request.method == 'POST':
        form = SearchForm(data=request.POST)
        if form.is_valid():
            # Form gives us nasa_centers *code* not *name*
            # We want Centers and Status each to be logical OR, but then ANDed with other criteria.
            q = Q()
            nasa_centers = form.cleaned_data['nasa_centers']
            if nasa_centers:
                q = q & Q(nasa_centers__code__in=nasa_centers)
            #import pdb; pdb.set_trace()
            status = form.cleaned_data['status']
            if status:
                q = q & Q(status__in=status)
            projects = Project.objects.filter(q)
            return render_to_response('project/project_list.html', # reduce, reuse, recycle
                                      {'object_list': projects},
                                      context_instance=RequestContext(request));
    else:
        form = SearchForm()
    return render_to_response('search.html',
                              {'form': form},
                              context_instance=RequestContext(request));
