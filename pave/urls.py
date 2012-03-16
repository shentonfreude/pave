from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.views.generic.simple import direct_to_template

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', direct_to_template, {'template': 'home.html'}, name='home'),
    url(r'^manage$', direct_to_template, {'template': 'manage.html'}, name='manage'),
    url(r'^exit$', direct_to_template, {'template': 'exit.html'}, name='exit'),

    # trying Twitter Bootstrap fluid-grid
    url(r'^bootstrap$', direct_to_template, {'template': 'bootstrap.html'}, name='bootstrap'),
    url(r'^about$',     direct_to_template, {'template': 'about.html'},     name='about'),

    # url(r'^pave/', include('pave.foo.urls')),
    (r'^project/', include('project.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
