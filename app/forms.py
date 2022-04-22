# Imports
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *



def step1(request):
    initial={'fn': request.session.get('fn', None)}
    form = PersonForm(request.POST or None, initial=initial)
    if request.method == 'POST':
        if form.is_valid():
            request.session['fn'] = form.cleaned_data['fn']
            return HttpResponseRedirect(reverse('step2'))
    return render(request, 'step1.html', {'form': form})

def step2(request):
    form = PetForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            pet = form.save(commit=False)
            person = Person.objects.create(fn=request.session['fn'])
            pet.owner = person
            pet.save()
            return HttpResponseRedirect(reverse('finished'))
    return render(request, 'step2.html', {'form': form})