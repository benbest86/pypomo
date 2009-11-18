from django.contrib import admin
from pomodoro.models import TaskSheet, InboxItem, Reflection, Pomodoro, Mark

admin.site.register(TaskSheet)
admin.site.register(InboxItem)
admin.site.register(Reflection)
admin.site.register(Pomodoro)
admin.site.register(Mark)
