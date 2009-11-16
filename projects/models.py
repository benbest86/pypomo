from django.db import models

# Create your models here.

class Project(models.Model):
    name = models.CharField(max_length=250)
    success_statement = models.TextField()
    created = models.DateField(auto_now_add=True)
    completed = models.DateField(null=True, blank=True)

    def __unicode__(self):
        return self.name

    def serialize(self, recursive=False):
        serialized = {
                'id': self.id,
                'name': self.name,
                'success_statement': self.success_statement,
                'created': str(self.created),
                }
        serialized['completed'] = self.completed and str(self.completed) or None
        return serialized

class Task(models.Model):
    project = models.ForeignKey(Project)
    name = models.TextField()
    due = models.DateField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    completed = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return self.name

    def serialize(self, recursive=False):
        serialized = {
                'id': self.id,
                'name': self.name,
                'created': str(self.created)
                }
        serialized['due'] = self.due and str(self.due) or None
        serialized['completed'] = self.completed and str(self.completed) or None
        if recursive:
            serialized['project'] = project.serialize()
        else:
            serialized['project'] = self.project_id
        return serialized

