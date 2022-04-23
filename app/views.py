"""
django.contrib.auth.decorators
- module that used for restricted users for certain functions in our app
from django.contrib.auth.forms import UserCreationForm
- A form that creates a user, with no privileges, from the given username and password.
"""

# general django imports 
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View

# from django auth import s
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout

# forms imports
from .forms import *

# models imports 
from .models import *


def homepage(request):
    template_name = "app/homepage.html"
    template = {}
    return render(request, template_name , template)

# page for login user
def loginPage(request):
    page = "login"
    if request.method == 'POST':
        # get the name and password, once the user submit in login page
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try: # where you test error
            user = User.objects.get(username=username)
        except:
            # flash messages
            # messages are gonna show up in template
            messages.error(request, "User does not exist.")
        
        # authenticate() --> takes in the request from submission, and check if username and password are align to the value in user model
        # dis either gonna give us error, or return back the user object that matches the credential
        user = authenticate(request, username=username, password=password)

        # if the user exists, then login the user with login()
        # login() method: used for adding the session in our database and browser(cookie)
        if user is not None:
            login(request, user)
            return redirect("homepage")
        else:
           # flash messages
            # messages are gonna show up in template
            messages.error(request, "Username OR Password does not exist.") 

    context = {'page': page}
    return render(request, 'app/login_register.html', context)

def logoutUser(request):
    # remove the session id and get user back to the login page
    logout(request)
    return redirect('homepage')

def register(request):
    page = "register"
    form = UserCreationForm()
    print(form)
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # by setting commit = False, we are saving this form, freezing the user in time, for us to access the user right away
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('homepage')
        else:
            messages.error(request, "An error occured during registration")

    context = { page: "register", 'form': form}
    return render(request, 'app/login_register.html', context)


def langing_page(request):
    template = "app/landing_page.html"
    context = {
        "site_title": "design your\ncoding journey",
        "site_description": "Coding Journey is a journal for programmers. Mark your current destination, create your coding path, explore other coders' journey and more!"
    }

    return render(request, template, context)



# template code for project input multi phase form 
def projectInput(request): 
    form = ProjectInputForm(request.POST)
    return render(request, "app\\project_input1.html", {"form": form})


# def projectInputSave(request):
#     # if method is not a post method, then we need to redirect to project input 
#     if request.method != "POST":

#         return HttpResponseRedirect(reverse("projectInput"))
#     # otherwise we can submit the post request 
#     else:
#         form = ProjectInputForm(request.POST)
#         if form.is_valid():



"""
Later goal is to take initial input and cause phase 2 to render while storing information 
inside of a session variable to be accessed by later phases + to populate form 
fields 
"""
# def projectInput1(request):
#     initial={'fn': request.session.get('fn', None)}
#     form = PersonForm(request.POST or None, initial=initial)
#     if request.method == 'POST':
#         if form.is_valid():
#             request.session['fn'] = form.cleaned_data['fn']
#             return HttpResponseRedirect(reverse('step2'))
#     return render(request, 'step1.html', {'form': form})

# def projectInput2(request):
#     form = PetForm(request.POST or None)
#     if request.method == 'POST':
#         if form.is_valid():
#             pet = form.save(commit=False)
#             person = Person.objects.create(fn=request.session['fn'])
#             pet.owner = person
#             pet.save()
#             return HttpResponseRedirect(reverse('finished'))
#     return render(request, 'step2.html', {'form': form})
# 
