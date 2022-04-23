# django lib imports
from tkinter.tix import Select
from django import forms
from django.forms import CheckboxSelectMultiple, ChoiceField, ModelForm

# django auth imports
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

#  our class defined imports
from .models import *



class ProjectInputForm1(forms.Form): 
    # project_name = forms.CharField(label='Project Name', max_length=100)
    # project_link = forms.CharField(label='Project Link', max_length=100)
    # start_date = forms.DateInput()
    # end_date = forms.DateInput()

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        if end_date < start_date:
            raise forms.ValidationError("End date should be greater than start date.")

class ProjectInputForm2(forms.Form): 
    project_description = forms.CharField(label="Proejct Description", widget=forms.Textarea())

# want an input field w/ multiple inputs corresponding to 
class ProjectInputForm3(forms.Form):
    forms.TypedMultipleChoiceField()

class ProjectInputForm(forms.ModelForm): 
    project_input = forms.TextInput()
    project_description = forms.Textarea()
    # start as text input and adjust to match figma
    markers = forms.ModelMultipleChoiceField(
        queryset=Marker.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
    start_date = forms.DateInput()
    end_date = forms.DateInput()
    project_link = forms.URLField()
    
    class Meta:
        model = Project
        fields = [
            "project_name",
            "project_description",
            "markers",
            "start_date",
            "end_date",
            "project_link"
        ]


# class customMMCF():

#     def func1():
#         return