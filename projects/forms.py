from django import forms

from projects.models import Project, Task

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'success_statement',)

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('name', 'due', 'estimate',)
