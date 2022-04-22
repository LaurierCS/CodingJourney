from django.db import models
from django.db.models.fields import *
from django.template.defaultfilters import slugify
from django import forms
from django.contrib.auth.models import User
import uuid


# Journey Model
class Journey(models.Model):
  user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
  journey_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  journey_name = models.CharField(max_length=200, null=True)
  email = models.EmailField(max_length=200, null=True)
  journey_bio = models.TextField(max_length=500)
  pic_link = models.CharField(max_length=2000, null=True, blank=True)
  date_created = models.DateTimeField(auto_now_add=True, null=True)

  def __str__(self):
    return self.journey_name

  

# Project Model
class Project(models.Model):
  project_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  project_name = models.CharField(max_length=200)
  project_description = models.TextField(null=True, blank=True)
  journey_id = models.ForeignKey("Journey", on_delete=models.CASCADE, null=True)
  markers = models.ManyToManyField("Marker")
  likes_amount = models.IntegerField(default=0)
  start_date = models.DateField(auto_now=False, auto_now_add=False)
  end_date = models.DateField(null=True, blank=True, auto_now=False, auto_now_add=False)
  project_link = models.CharField(max_length=2000, null=True, blank=True)
  difficulty = models.ForeignKey("Difficulty", on_delete=models.CASCADE)
  
  def __str__(self):
    return self.project_name

# difficulty model
class Difficulty(models.Model):
  diffuculty_name = models.CharField(max_length=200)
  difficulty_id = models.AutoField(primary_key=True)

  def __str__(self):
    return self.diffuculty_name

# Markers Model
class Marker(models.Model):
  marker_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  marker_name = models.CharField(max_length=100)
  description = models.TextField(null=True, blank=True)

  def __str__(self):
    return self.marker_name