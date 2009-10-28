from django.conf.urls.defaults import *


urlpatterns = patterns('pomodoro.views',
    url(r'^tasks/$', 'tasks_index',),
)
