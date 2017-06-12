from django.db import models
#from django.utils import timezone

class Event(models.Model):
    event_name = models.TextField(default='') #name
    event_detail = models.TextField(default='') #detail
    event_numset = models.IntegerField(default=0) #limit for start
    event_location = models.TextField(default='') #location
    pcount = models.IntegerField(default=0) #person count
    #date = models.DateTimeField(default=timezone.now())#'date published')YYYY-MM-DD HH:MM

class Person(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, default=1)
    fname = models.TextField(default='') #first name
    lname = models.TextField(default='') #last name