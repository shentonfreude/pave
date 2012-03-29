from django.shortcuts import render_to_response
from django.template import RequestContext

def home(request):
    # Manager login form needs CSRF context
    return render_to_response('home.html',
                              {},
                              context_instance=RequestContext(request));

