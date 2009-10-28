from django.db import models


# see http://www.pomodorotechnique.com/ for the inspiration for this app
class TaskSheet(models.Model):
    """
    Represents a pomodoro task sheet. Essentially a date and location
    that holds tasks and Inbox items. Also allows for reflection bits.
    """
    date = models.DateField(auto_now_add=True)
    location = models.CharField(max_length=50)
    closed = models.DateTimeField(null=True, blank=True)

class Task(models.Model):
    """
    One pomodoro task. Cannot be spread over multiple task
    sheets - tasks should be completable in one task sheet
    sitting. May want to review. Has a place for estimate
    of number of pomodoros for completion.
    """
    task_sheet = models.ForeignKey(TaskSheet)
    name = models.CharField(max_length=250)
    estimate = models.SmallIntegerField()
    completed = models.DateTimeField(null=True, blank=True)

class InboxItem(models.Model):
    """
    Represents an item to be added to the Inbox
    and dealt with later.
    """
    task_sheet = models.ForeignKey(TaskSheet)
    name = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    dealt_with = models.DateTimeField(null=True, blank=True)

class Pomodoro(models.Model):
    """
    One pomodoro time period. Has a start and an end
    time with a flag for whether the pomodoro was cancelled
    mid way through.
    """
    task = models.ForeignKey(Task)
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(null=True, blank=True)
    cancelled = models.BooleanField(default=False)
    
class InternalInterruption(models.Model):
    """
    Represents a ' in the pomodoro technique.
    """
    task = models.ForeignKey(Task)
    time = models.DateTimeField(auto_now_add=True)

class ExternalInterruption(models.Model):
    """
    Represents a - in the pomodoro technique.
    """
    task = models.ForeignKey(Task)
    time = models.DateTimeField(auto_now_add=True)

class Reflection(models.Model):
    """
    Represents some textual reflection on the productivity
    of the day.
    """
    task_sheet = models.ForeignKey(TaskSheet)
    content = models.TextField()

