from django import forms
from pomodoro.models import TaskSheet, PomodoroTask, InboxItem, Mark

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
        model = PomodoroTask
        fields = ('name', 'estimate',)

class MarkForm(forms.ModelForm):
    class Meta:
        model = Mark
        fields = ('type',)
