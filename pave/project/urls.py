from django.conf.urls.defaults import * #GROSS
from django.views.generic.simple import direct_to_template
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import create_object
from models import Project
from views import search, browse

info_dict = {
    'queryset' : Project.objects.all()
    }

urlpatterns = patterns(
    '',
    url(r'^$',                     browse, name="projects"),
    url(r'^search/$',              search, name="search"),
    url(r'^(?P<object_id>\d+)/$',  object_detail, info_dict, name="details"),
    # url(r'^search/$',              direct_to_template, {'template': 'search.html'}, name="search"),
    url(r'^new/$',                 create_object, {'model': Project}), # For admins only
)

