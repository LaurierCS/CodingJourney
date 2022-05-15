from django import forms
from django.forms import ModelForm, CheckboxSelectMultiple, ChoiceField, ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import *

class CreateUserForm(UserCreationForm):
  class Meta:
    model = User
    fields = ['username', 'email', 'password1', 'password2']

class UserSettingForm(ModelForm):
  class Meta:
    model = Profile
    fields = ['email', 'image', 'bio']