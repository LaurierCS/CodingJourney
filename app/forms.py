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
        queryset=Skill.objects.filter(node_type="N"),
        required=True,
        label="Skills", 
        help_text="What Skills did you learn or use?"
    )
    kind = forms.ChoiceField(choices=Experience.EXPERIENCE_TYPE)
    description = forms.Textarea()
    start_date = forms.DateField(widget=forms.SelectDateWidget)
    end_date = forms.DateField(widget=forms.SelectDateWidget)
    project_link = forms.URLInput()
    image = forms.ImageField(required=False)
    
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

    def __init__(self, *args, **kwargs):
      super(ExperienceInputform, self).__init__(*args, **kwargs)
      self.fields['name'].widget.attrs.update({'class': 'input'})
      self.fields['skills'].widget.attrs.update({'class': 'input multi-select-input'})
      self.fields['description'].widget.attrs.update({'class': 'input fixed-size-input'})
      self.fields['start_date'].widget.attrs.update({'class': 'input select'})
      self.fields['end_date'].widget.attrs.update({'class': 'input select'})
      self.fields['project_link'].widget.attrs.update({'class': 'input'})
      self.fields['kind'].widget.attrs.update({'class': 'input select'})
      self.fields['image'].widget.attrs.update({'class': 'tech-tag tech-tag-blue'})

    def clean(self):
      cleaned_data = super().clean()
      start_date = cleaned_data.get("start_date")
      end_date = cleaned_data.get("end_date")
      if end_date and end_date < start_date:
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

class UserSettingForm(ModelForm):
  class Meta:
    model = Profile
    fields = ['email', 'image', 'bio']

class SearchQueryForm(forms.Form):
  search_query = forms.CharField(required=True)
  search_scope = forms.CharField(required=True)