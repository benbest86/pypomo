import datetime

from django.db import models
from django.db.models.signals import post_save
from projects.models import Task


# see http://www.pomodorotechnique.com/ for the inspiration for this app

class TaskSheetManager(models.Manager):

    def get_current(self):
        """
        Gets the current open task sheet or
        None if no task sheet is open.
        """
        qs = self.get_query_set()
        open_task_sheets = qs.filter(closed__isnull=True, opened__isnull=False)

        if open_task_sheets.count() == 0:
            return None
        else:
            # this intentionally raises an Exception when more than
            # one task sheet is open. This should theoretically never happen
            return open_task_sheets.get()

class TaskSheet(models.Model):
    """
    Represents a pomodoro task sheet. Essentially a date and location
    that holds tasks and Inbox items. Also allows for reflection bits.
    """
    date = models.DateTimeField()
    location = models.CharField(max_length=50)
    opened = models.DateTimeField(null=True, blank=True)
    closed = models.DateTimeField(null=True, blank=True)
    tasks = models.ManyToManyField(Task, through="TaskOnSheet", related_name='task_sheets')

    objects = TaskSheetManager()

    def serialize(self, recursive=False):
        serialized = {
                'id': self.id,
                'location': self.location,
                }
        serialized['date'] = self.date and str(self.date) or None
        serialized['opened'] = self.opened and str(self.opened) or None
        serialized['closed'] = self.closed and str(self.closed) or None
        tasks = []
        for task_on_sheet in self.tasks_on_sheet.all():
            if recursive:
                serialized_task = task_on_sheet.task.serialize()
                serialized_task['marks'] = [
                        mark.serialize() for mark in task_on_sheet.marks.all()]
                tasks.append(serialized_task)
            else:
                tasks.append(task_on_sheet.task.id)
        serialized['tasks'] = tasks

    def __unicode__(self):
        return '%s - %s' % (self.location, self.date.strftime('%Y-%m-%d'))

class TaskOnSheet(models.Model):
    """
    Allows each Mark to be associated with a task on a task sheet instead
    of just a task.
    """
    task = models.ForeignKey(Task, related_name='tasks_on_sheet')
    task_sheet = models.ForeignKey(TaskSheet, related_name='tasks_on_sheet')

class InboxItem(models.Model):
    """
    Represents an item to be added to the Inbox
    and dealt with later.
    """
    name = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    dealt_with = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.name

MARK_TYPE_CHOICES = (
        ('pomodoro', 'X'),
        ('internal', "'"),
        ('external', '-'),
        )

class Mark(models.Model):
    """
    A pomodoro mark. X for a pomodoro, ' for an internal interruption
    and - for an external interruption.
    """
    task_on_sheet = models.ForeignKey(TaskOnSheet, related_name='marks')
    time = models.DateTimeField(default=datetime.datetime.now())
    type = models.CharField(max_length=50, choices=MARK_TYPE_CHOICES)

    def __unicode__(self):
        return self.get_type_display()
    def serialize(self, recursive=False):
        serialized = {
                'id': self.id,
                'time': str(self.time),
                'type': self.type,
                'type_display': self.get_type_display(),
                'task': self.task_on_sheet.task.id,
                'task_sheet': self.task_on_sheet.task_sheet.id,
                }
        return serialized



class PomodoroManager(models.Manager):
    
    def get_current(self):
        """
        Returns the currently active pomodoro.
        """
        qs = self.get_query_set()
        ongoing_pomodoros = qs.filter(completed__isnull=True)
        # this intentionally raises an Exception when more than
        # one pomodoro is ongoing. This should theoretically never happen.
        return ongoing_pomodoros.count() and ongoing_pomodoros.get() or None


class Pomodoro(models.Model):
    """
    One pomodoro time period. Has a start and an end
    time with a flag for whether the pomodoro was cancelled
    mid way through.
    """
    task_on_sheet= models.ForeignKey(TaskOnSheet, related_name='pomodoros')
    completed = models.DateTimeField(null=True, blank=True)

    objects = PomodoroManager()

    @property
    def task(self):
        return self.task_on_sheet.task

    def __unicode__(self):
        base = 'X for %s' % self.task
        if self.completed:
            final = '%s at %s' % (base, str(self.completed))
        else:
            final = '%s (ongoing)' % base
        return final



class Reflection(models.Model):
    """
    Represents some textual reflection on the productivity
    of the day.
    """
    task_sheet = models.ForeignKey(TaskSheet)
    content = models.TextField()

    def __unicode__(self):
        return 'Reflection for %s' % self.task_sheet


#### SIGNALS ####

def add_pomodoro_mark(sender, instance, created, **kwargs):
    if instance.completed:
        Mark.objects.create(task=instance.task, type='pomodoro')

post_save.connect(add_pomodoro_mark, sender=Pomodoro, dispatch_uid="add_pomodoro_mark_on_pomo_save")
