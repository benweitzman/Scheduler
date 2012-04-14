from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User

PRIORITIES = (
    (11,"Need"),
    (5,"5"),
    (4,"4"),
    (3,"3"),
    (2,"2"),
    (1,"1"),
)

class PersonalEvent(models.Model):
    priority = models.IntegerField(choices=PRIORITIES)
    user = models.ForeignKey(User)
    name = models.CharField(max_length=100)
    description = models.TextField()
    startTime = models.TimeField()
    endTime = models.TimeField()
    days = models.CommaSeparatedIntegerField(max_length=14)


class ClassObject(models.Model):
    professor = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    description = models.TextField()
    times = models.CharField(max_length=40)
    days = models.CharField(max_length=5)
    locations = models.CharField(max_length=50)
    courseNumber = models.CharField(max_length=15)
    callNumber = models.CharField(max_length=7)
    #section = models.CharField(max_length = 10)
    closed = models.BooleanField()

    def __unicode__(self):
        return self.courseNumber

class ClassEvent(models.Model):
    user = models.ForeignKey(User)
    classObject = models.ForeignKey(ClassObject)
    priority = models.IntegerField(choices=PRIORITIES)

class Department(models.Model):
    title = models.CharField(max_length=100)
    key = models.CharField(max_length=10)
    classes = models.ManyToManyField(ClassObject)

    def __unicode__(self):
        return self.key