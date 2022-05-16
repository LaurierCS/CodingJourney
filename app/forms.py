from django import forms
from django.forms import ModelForm, CheckboxSelectMultiple, ChoiceField, ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import *

class ExperienceInputform(forms.ModelForm): 
    name = forms.CharField(required=True)
    # type = forms.ModelMultipleChoiceField(
    #   queryset=Experience.EXPERIENCE_TYPE, 
    #   )
    # start as text input and adjust to match figma
    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        required=True,
        label="Skills", 
        help_text="What Skills did you learn or use?"
    )
    # kind = forms.ChoiceField(choices=Experience.EXPERIENCE_TYPE)
    description = forms.Textarea()
    start_date = forms.DateField(widget=forms.SelectDateWidget)
    end_date = forms.DateField(widget=forms.SelectDateWidget)
    project_link = forms.URLInput()
    image = forms.ImageField()
    
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
      if end_date and end_date < start_date:
        raise forms.ValidationError(("End date should be greater than start date."), code="invalidDate")


# class customMMCF():

from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class CreateUserForm(UserCreationForm):
  class Meta:
    model = User
    fields = ['username', 'email', 'password1', 'password2']

