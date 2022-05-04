# django lib imports
# from tkinter.tix import Select
from django import forms
from django.forms import CheckboxSelectMultiple, ChoiceField, ModelForm

# django auth imports
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import *

#  our class defined imports
from .models import *

class ExperienceInputform(forms.ModelForm): 
    # start as text input and adjust to match figma
    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
    )
    kind = forms.ChoiceField(choices=Experience.EXPERIENCE_TYPE)
    description = forms.Textarea()
    start_date = forms.DateField(widget=forms.SelectDateWidget)
    end_date = forms.DateField(widget=forms.SelectDateWidget)
    project_link = forms.URLInput()
    
    class Meta:
        model = Experience
        fields = "__all__"
        exclude = ('profile', 'likes_amount',)

        # lables = { 
        #   "name": "Experience Name",
        #   "markers": "Add Marker Tags",
        #   "kind": "Experience Type",
        #   "descripton": "Experience Description",
        # }

    def clean(self):
      cleaned_data = super().clean()
      start_date = cleaned_data.get("start_date")
      end_date = cleaned_data.get("end_date")
      if end_date < start_date:
        raise forms.ValidationError(("End date should be greater than start date."), code="invalidDate")

      return cleaned_data


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
