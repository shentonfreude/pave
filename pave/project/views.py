from django.forms import Form, CharField, DateField, ChoiceField, MultipleChoiceField

from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.template import RequestContext

from constants import center_codes, project_statuses

class SearchForm(Form):
    project_id = CharField(max_length=80, required=False)
    status = MultipleChoiceField(required=False, choices=project_statuses)
    centers = MultipleChoiceField(required=False, choices=center_codes)
    date = DateField(required=False)
    date_start = DateField(required=False)
    date_end = DateField(required=False)

def search(request):
    if request.method == 'POST':
        form = SearchForm(data=request.POST)
        if form.is_valid():
            # do the search
            search_results = {}
            return render_to_response('search_results.html',
                                     {'results': search_results},
                                     context_instance=RequestContext(request));
    else:
        form = SearchForm()
    return render_to_response('search.html',
                              {'form': form},
                              context_instance=RequestContext(request));
