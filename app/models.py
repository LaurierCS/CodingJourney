from django.db import models
from django.db.models.fields import *
from django.template.defaultfilters import slugify
from django import forms
from django.contrib.auth.models import User


class Profile(models.Model):
  user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
  email = models.EmailField(max_length=200, null=True)
  bio = models.TextField(max_length=500)
  image = models.ImageField(default="images/smiley.jpg", upload_to='images/', blank=True)
  date_created = models.DateTimeField(auto_now_add=True, null=True)

  def __str__(self):
    return self.user.username

  
class Experience(models.Model):
  profile = models.ForeignKey("Profile", on_delete=models.CASCADE, null=True)
  markers = models.ManyToManyField("Marker")
  name = models.CharField(max_length=200)
  EXPERIENCE_TYPE = (
        ('E', 'Exploration'),
        ('P', 'Project'),
        ('L', 'Learning'),
        ('H', 'Hackathon'),
        ('E', 'Event'),
    )
  kind = models.CharField(max_length=40, choices=EXPERIENCE_TYPE, default="E" )
  description = models.TextField(null=True, blank=True)
  likes_amount = models.IntegerField(default=0)
  start_date = models.DateField(null=True, blank=True) #let these be allowed to be null for now until the widget is setup for date input sumbission
  end_date = models.DateField(null=True, blank=True) #let these be allowed to be null for now until the widget is setup for date input sumbission
  project_link = models.CharField(max_length=2000, null=True, blank=True)
  image = models.ImageField(upload_to='images/', blank=True)
  
  def __str__(self):
    return self.project_name


class Difficulty(models.Model):
  name = models.CharField(max_length=200)
  difficulty_id = models.AutoField(primary_key=True)

  def __str__(self):
    return self.diffuculty_name


class Marker(models.Model):
  name = models.CharField(max_length=100)
  description = models.TextField(null=True, blank=True)

  def __str__(self):
    return self.marker_name