from django.contrib import admin
from pomodoro.models import TaskSheet, Task, InboxItem, Reflection, Pomodoro, Mark

admin.site.register(TaskSheet)
admin.site.register(Task)
admin.site.register(InboxItem)
admin.site.register(Reflection)
admin.site.register(Pomodoro)
admin.site.register(Mark)
