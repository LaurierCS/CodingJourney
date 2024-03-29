from django.db import models
from django.db.models.fields import *
from django.template.defaultfilters import slugify
from django import forms
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, related_name = 'profile', null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=False, default="John")
    last_name = models.CharField(max_length=100, blank=False, default="Doe")
    bio = models.TextField(max_length=500, blank=True)
    email = models.EmailField(max_length=256, blank=True)
    image = models.ImageField(
        default="images/profile_picture.svg", upload_to='user_media/profile_images')
    # 👇 THE "tech_roadmap" RELATIONSHIP BELOW IS THE TECHNOLOGIES THAT THE USER WANTS TO ACHIEVE
    # (if a tech is in this list, it will show up on the tree graph)
    # This is all the tech they either want to work with or have already achieved experience with
    # This will allow us to make the graph unique to each persons tech goals, instead of showing nodes for dozens of different
    # technologies they aren't even aiming to achieve
    # tech_roadmap = models.ManyToManyField("Technology", blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    email = models.EmailField(max_length=256, blank=True, null=True)
    twitter = models.URLField(max_length=200, blank=True, null=True)
    linkedin = models.URLField(max_length=200, blank=True, null=True)
    github = models.URLField(max_length=200, blank=True, null=True)
    website = models.URLField(max_length=200, blank=True, null=True)

    liked_experiences = models.ManyToManyField("Experience", related_name="liked_experiences")

    def __str__(self):
        return self.user.username


"""
  Condensed skill tree and markers into one unit
  Skill tree elements of type N will now represent skills 
  Skill tree elements of type C will be parents to at least one node of type N 
"""
class Skill(models.Model): 

  node_type_choices = (
    ("C", "Category"), ("N", "Node"), ("U", "User"))
  # Foreign key fields 
  parentId = models.ForeignKey("Skill", on_delete=models.CASCADE, null=True)

  # Text fields
  id = models.CharField(primary_key=True, max_length=30)
  name = models.CharField(max_length=200)
  icon_HREF = models.URLField(max_length=200)
  node_type = models.CharField(max_length=40, choices=node_type_choices, default="C")

  def __str__(self): 
    return self.name

"""
  DesiredSkills list will contain all skills that a user is either currently proficient in or 
  desires to be proficient in
  There will be different degrees of efficiency on a 0 to 5 scale 
  Each desired skill will have a set of experiences with it that can be nullable
"""
class DesiredSkill(models.Model):
  proficiency_choices = [
    (0, "Aiming to Learn"),
    (1, "Some Understanding"),
    (2, "Some Proficiency"),
    (3, "Capable"),
    (4, "Able to Use Professionally"),
    (5, "Expert"),
    ]
    
  # Foreign Key Fields
  user_id = models.ForeignKey("Profile", on_delete=models.CASCADE)
  skill = models.ForeignKey("Skill", on_delete=models.CASCADE)

  # User Input Fields 
  proficiency = models.FloatField(choices=proficiency_choices, default=0)
  description = models.TextField(max_length=1000)
  
  def __str__(self):
    return self.skill.__str__()

class Experience(models.Model):
  # technologies = models.ManyToManyField("Technology")
  EXPERIENCE_TYPE = (
    ('E', 'Exploration'),
    ('P', 'Project'),
    ('L', 'Learning'),
    ('H', 'Hackathon'),
    ('Ev', 'Event'),
  )

  # Foreign Key Fields
  profile = models.ForeignKey("Profile", on_delete=models.CASCADE, null=True)
  skills = models.ManyToManyField(DesiredSkill)
  # Text Fields 
  name = models.CharField(max_length=200)
  kind = models.CharField(max_length=40, choices=EXPERIENCE_TYPE, default="E")
  description = models.TextField(null=True, blank=True)
  # Other Fields
  likes_amount = models.IntegerField(default=0)
  start_date = models.DateField(null=True, blank=True) #let these be allowed to be null for now until the widget is setup for date input sumbission
  end_date = models.DateField(null=True, blank=True) #let these be allowed to be null for now until the widget is setup for date input sumbission
  project_link = models.URLField(max_length=2000, null=True, blank=True)
  image = models.ImageField(default="images/journey_image.jpg", upload_to='experience_images/', blank=True)
  
  def increment_like(self):
    self.likes_amount += 1
    self.save()
    return

  def decrement_like(self):
    self.likes_amount -= 1
    self.save()
    return
  
  def __str__(self):
    return self.name

