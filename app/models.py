# Imports
from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import *
from django.template.defaultfilters import slugify
import uuid

# Project Model
class Project(models.Model):
  project_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  project_name = models.CharField(max_length=200)
  project_description = models.TextField(null=True, blank=True)
  markers = models.ManyToManyField("Marker")
  likes = models.IntegerField(default=0)
  start_date = models.DateField(auto_now=False, auto_now_add=False)
  end_date = models.DateField(null=True, blank=True, auto_now=False, auto_now_add=False)
  project_link = models.CharField(max_length=2000, null=True, blank=True)
  
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
  title = models.CharField(max_length=100)
  description = models.TextField(null=True, blank=True)

  def __str__(self):
    return self.title


