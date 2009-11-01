from django import forms
from pomodoro.models import TaskSheet, Task, InboxItem

class TaskSheetForm(forms.ModelForm):
    class Meta:
        model = TaskSheet
        fields = ('location',)

class InboxItemForm(forms.ModelForm):
    class Meta:
        model = InboxItem

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
