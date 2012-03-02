from django.conf.urls.defaults import * #GROSS
from models import Project

info_dict = {
    'queryset' : Project.objects.all()
    }

urlpatterns = patterns(
    '',
    (r'^$',                     'django.views.generic.list_detail.object_list', info_dict),
    (r'^new/$',                 'django.views.generic.create_update.create_object', {'model': Project}),
    (r'^(?P<object_id>\d+)/$',  'django.views.generic.list_detail.object_detail', info_dict),
)

