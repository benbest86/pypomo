"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from projects.models import Project
from pomodoro.models import PomodoroTask
from django.core import serializers

class TestTaskSerialization(TestCase):

    def setUp(self):
        self.default_project = Project.objects.create(
                name='test project', success_statement='a passing test')

    def tearDown(self):
        PomodoroTask.objects.all().delete()
        Project.objects.all().delete()


    def test_serialize_barebones_task(self):
        task = PomodoroTask.objects.create(
                project=self.default_project, name='a barebones task')
        serialized = task.serialize()
