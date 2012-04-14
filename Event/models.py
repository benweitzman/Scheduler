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


class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    startTime = models.TimeField()
    endTime = models.TimeField()
    days = models.CommaSeparatedIntegerField(max_length=14)
    priority = models.IntegerField(choices=PRIORITIES)
    user = models.ForeignKey(User)


class Class(Event):
    professor = models.CharField(max_length=100)
    url = models.URLField()



