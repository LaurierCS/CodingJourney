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
    return self.name

"""
  Condensed skill tree and markers into one unit
  Skill tree elements of type N will now represent skills 
  Skill tree elements of type C will be parents to at least one node of type N 
"""
class Skill(models.Model): 
  id = models.CharField(primary_key=True, max_length=30)
  children = models.ManyToOneRel("Skill", null=True)
  name = models.CharField(max_length=30)
  icon_HREF = models.URLField(max_length=200)
  node_type_choices = [("C", "Category"), ("N", "Node")]
  node_type = models.CharField(max_length=1, choices=node_type_choices)

  def __str__(self): 
    return self.name


"""
  DesiredSkills list will contain all skills that a user is either currently proficient in or 
  desires to be proficient in
  There will be different degrees of efficiency on a 0 to 5 scale 
  Each desired skill will have a set of experiences with it that can be nullable
"""
class DesiredSkill(models.Model):
  user_id = models.ForeignKey("Profile", on_delete=models.CASCADE)
  skill = models.ForeignKey("Skill")
  experiences = models.ManyToOneRel("Experience", null=True)
  proficiency_choices = [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]
  proficiency = models.FloatField(choices=proficiency_choices, default=0)
  description = models.TextField(max_length=1000)

  def __str__(self):
    return self.skill.__str__()