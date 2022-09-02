from operator import mod
from statistics import mode
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.




class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)
    avatar = models.ImageField(null=True, default="avatar.svg")
    # USERNAME_FIELD = 'email'
    Editor = models.BooleanField(default=False)
    Maintainer = models.BooleanField(default=False)
    REQUIRED_FIELDS = []



class Athlete(models.Model):
    Graduation = models.IntegerField()
    Athlete = models.CharField(max_length=200, null=True)
    Male = models.BooleanField()
    Active = models.BooleanField()
    First = models.CharField(max_length=200, blank=True)
    Last = models.CharField(max_length=200, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Athlete

class Meet(models.Model):
    MeetName = models.TextField()
    State = models.BooleanField()
    Indoor = models.BooleanField()
    Location =  models.CharField(max_length=200, null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.MeetName

class Event(models.Model):
    EventName = models.CharField(max_length=200, null=True)
    FieldEvent = models.BooleanField()
    Current = models.BooleanField()
    Relay = models.BooleanField()
    Order = models.IntegerField()
    MeasurementSystem = models.CharField(max_length=20)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.EventName

class Performance(models.Model):
    EventID = models.ForeignKey(Event, on_delete=models.SET_NULL,null=True)
    Mark = models.CharField(max_length=200, null=True)
    MarkRawLarge = models.IntegerField()
    MarkRawSmall = models.DecimalField(decimal_places=3,max_digits=20)
    MeetID = models.ForeignKey(Meet, on_delete=models.SET_NULL,null=True)
    PerformanceNote = models.CharField(max_length=10,null=True,blank=True)
    CY = models.IntegerField(null=True)
    EventDate = models.DateField(null=True)
    Notes = models.TextField(null = True,blank=True)
    Archive = models.BooleanField()
    StateChamp = models.BooleanField(null=True)
    AthleteID = models.ManyToManyField(Athlete)
    Confirmed = models.BooleanField(null=False,default=False)
    Locked = models.BooleanField(null=False,default=False)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.Mark



