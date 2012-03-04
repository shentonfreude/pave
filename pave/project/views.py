from django.core.context_processors import csrf
from django.db.models import Q
from django.forms import Form, CharField, DateField, ModelMultipleChoiceField
from django.shortcuts import render_to_response
from django.template import RequestContext

from models import Project, Center, Status

class SearchForm(Form):
    project_id   = CharField(max_length=80, required=False)
    status       = ModelMultipleChoiceField(queryset=Status.objects.all(), required=False)
    nasa_centers = ModelMultipleChoiceField(queryset=Center.objects.all(), required=False)
    date         = DateField(required=False, help_text="MM/DD/YYYY or YYYY-MM-DD")
    date_start   = DateField(required=False, help_text="MM/DD/YYYY or YYYY-MM-DD")
    date_end     = DateField(required=False, help_text="MM/DD/YYYY or YYYY-MM-DD")

def search(request):
    if request.method == 'POST':
        form = SearchForm(data=request.POST)
        if form.is_valid():
            # Form gives us nasa_centers *code* not *name*
            # We want Centers and Status each to be logical OR, but then ANDed with other criteria.
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
#            import pdb; pdb.set_trace()
            return render_to_response('project/project_list.html', # reduce, reuse, recycle
                                      {'object_list': projects},
                                      context_instance=RequestContext(request));
    else:
        form = SearchForm()
    return render_to_response('search.html',
                              {'form': form},
                              context_instance=RequestContext(request));
