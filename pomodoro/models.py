from django.db import models
from django.db.models.signals import post_save


# see http://www.pomodorotechnique.com/ for the inspiration for this app

class TaskSheetManager(models.Manager):

    def get_current(self):
        """
        Gets the current open task sheet or
        None if no task sheet is open.
        """
        qs = self.get_query_set()
        open_task_sheets = qs.filter(closed=None)

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
    date = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=50)
    closed = models.DateTimeField(null=True, blank=True)

    objects = TaskSheetManager()

    def __unicode__(self):
        return '%s - %s' % (self.location, self.date.strftime('%Y-%m-%d'))

class Task(models.Model):
    """
    One pomodoro task. Cannot be spread over multiple task
    sheets - tasks should be completable in one task sheet
    sitting. May want to review. Has a place for estimate
    of number of pomodoros for completion.
    """
    task_sheet = models.ForeignKey(TaskSheet, related_name='tasks')
    name = models.CharField(max_length=250)
    estimate = models.SmallIntegerField()
    completed = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.name


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
    """
    task = models.ForeignKey(Task, related_name='marks')
    time = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=50, choices=MARK_TYPE_CHOICES)

    def __unicode__(self):
        return self.get_type_display()



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
    task = models.ForeignKey(Task, related_name='pomodoros')
    completed = models.DateTimeField(null=True, blank=True)

    objects = PomodoroManager()

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

post_save.connect(add_pomodoro_mark, sender=Pomodoro, dispatch_uid='add_pomodoro_mark')
