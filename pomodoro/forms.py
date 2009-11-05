from django import forms
from pomodoro.models import TaskSheet, Task, InboxItem, Mark

class TaskSheetForm(forms.ModelForm):
    class Meta:
        model = TaskSheet
        fields = ('location',)

class InboxItemForm(forms.ModelForm):
    class Meta:
        model = InboxItem
        fields = ('name',)

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('name', 'estimate',)

class MarkForm(forms.ModelForm):
    class Meta:
        model = Mark
        fields = ('type',)
