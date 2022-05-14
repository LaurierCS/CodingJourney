from django.db import models
from django.db.models.fields import *
from django.template.defaultfilters import slugify
from django import forms
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    email = models.EmailField(max_length=254, blank=False)
    first_name = models.CharField(max_length=100, blank=False, default="John")
    last_name = models.CharField(max_length=100, blank=False, default="Doe")
    bio = models.TextField(max_length=500, blank=True)
    image = models.ImageField(default="images/smiley.jpg", upload_to='images/', blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    # 👇 THE "tech_roadmap" RELATIONSHIP BELOW IS THE TECHNOLOGIES THAT THE USER WANTS TO ACHIEVE
    # (if a tech is in this list, it will show up on the tree graph)
    # This is all the tech they either want to work with or have already achieved experience with
    # This will allow us to make the graph unique to each persons tech goals, instead of showing nodes for dozens of different
    # technologies they aren't even aiming to achieve
    # tech_roadmap = models.ManyToManyField("Technology", blank=True, null=True)

    def __str__(self):
        return self.user.username


class Skill(models.Model):
    # 1. EVERY Skill IS EITHER A LANGUAGE, FRAMEWORK OR LIBRARY
    # 2. EVERY Skill CAN HAVE ANOTHER Skill AS A PARENT USING THE parent RELATIONSHIP VARIABLE
    name = models.CharField(max_length=100, blank=False)
    description = models.TextField(null=True, blank=True)
    # parents = models.ManyToManyField("self", null=False, blank=False)
    Skill_TYPE = (
        ('L', 'Language'),
        ('F', 'Framework'),
        ('L', 'Library or Package'),
        ('C', 'Programming Paradigm'),
    )
    kind = models.CharField(max_length=40, choices=Skill_TYPE, default="L")

    def __str__(self):
        return self.name


class Experience(models.Model):
    profile = models.ForeignKey(
        "Profile", on_delete=models.CASCADE, null=False, blank=False)
    # technologies = models.ManyToManyField("Technology")
    name = models.CharField(max_length=200)
    EXPERIENCE_TYPE = (
        ('E', 'Exploration'),
        ('P', 'Project'),
        ('L', 'Learning'),
        ('H', 'Hackathon'),
        ('E', 'Event'),
    )
    kind = models.CharField(
        max_length=40, choices=EXPERIENCE_TYPE, default="E")
    description = models.TextField(null=True, blank=True)
    likes_amount = models.IntegerField(default=0)
    # let these be allowed to be null for now until the widget is setup for date input sumbission
    start_date = models.DateField(null=True, blank=True)
    # let these be allowed to be null for now until the widget is setup for date input sumbission
    end_date = models.DateField(null=True, blank=True)
    project_link = models.CharField(max_length=2000, null=True, blank=True)
    image = models.ImageField(upload_to='images/', blank=True)

    def __str__(self):
        return self.name
