from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

    url(r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'home.html'}, name='home',),
    (r'^', include('pomodoro.urls')),
    url(r'^stats/$', 'django.views.generic.simple.direct_to_template', {'template': 'home.html'}, name='stats',), # TODO 
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    (r'^admin/', include(admin.site.urls)),
)
