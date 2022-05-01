# django lib imports
# from tkinter.tix import Select
from django import forms
from django.forms import CheckboxSelectMultiple, ChoiceField, ModelForm

# django auth imports
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import *

#  our class defined imports
from .models import *

# class ProjectInputForm(forms.ModelForm): 
#     project_input = forms.TextInput()
#     project_description = forms.Textarea()
#     # start as text input and adjust to match figma
#     markers = forms.ModelMultipleChoiceField(
#         queryset=Marker.objects.all(),
#         widget=forms.CheckboxSelectMultiple
#     )
#     start_date = forms.DateInput()
#     end_date = forms.DateInput()
#     project_link = forms.URLField()
    
#     class Meta:
#         model = Project
#         fields = "__all__"

# class customMMCF():

from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class CreateUserForm(UserCreationForm):
  class Meta:
    model = User
    fields = ['username', 'email', 'password1', 'password2']

class ProfileForm(ModelForm):
  class Meta:
    model = Profile
    fields = ['email', 'bio', 'image']
