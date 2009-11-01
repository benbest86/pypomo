from django.conf.urls.defaults import *


urlpatterns = patterns('pomodoro.views',

    # shortcut urls - not RESTful at all, but they make life easier :)
    url(r'^complete_pomodoro/$', 'complete_pomodoro', name='complete_pomodoro'),
    url(r'^cancel_pomodoro/$', 'cancel_pomodoro', name='cancel_pomodoro'),
    url(r'^add_internal_interruption/$', 'add_internal_interruption', name='add_internal_interruption'),
    url(r'^add_external_interruption/$', 'add_external_interruption', name='add_external_interruption'),
    url(r'^active_sheet/$', 'active_sheet', name='active_sheet'),

    # task sheets
    url(r'^task_sheets/$', 'task_sheets_index',),
    url(r'^task_sheets/new/$', 'new_task_sheet', name='new_task_sheet',),
    url(r'^task_sheets/(?P<task_sheet_id>\d+)/$', 'task_sheet_detail', name='task_sheet_detail'),


    # tasks and inbox items
    url(r'^task_sheets/(?P<task_sheet_id>\d+)/tasks/$', 'tasks_index', name='tasks_index'),
    url(r'^task_sheets/(?P<task_sheet_id>\d+)/tasks/(?P<task_id>\d+)/$', 'task_detail', name='task_detail'),

    url(r'^inbox_items/$', 'inbox_items_index', name='inbox_items_index'),
    url(r'^inbox_items/(?P<inbox_item_id>\d+)/$', 'inbox_item_detail', name='inbox_item_detail'),
)
