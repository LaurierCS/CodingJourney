"""
django.contrib.auth.decorators
- module that used for restricted users for certain functions in our app
from django.contrib.auth.forms import UserCreationForm
- A form that creates a user, with no privileges, from the given username and password.
"""

# general django imports 
from sqlite3 import Date
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
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

# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required


# Create your views here
from .models import *
from .forms import CreateUserForm
from django.db.models import Q

# CONSTANTS
LOGIN_FORM_INPUTS = [{
                "attributes": {
                    "id": "username_input",
                    "name": "username",
                    "type": "text",
                    "required": "true"
                },
                "label": "Username",
            },
            {
                "attributes": {
                    "id": "password_input",
                    "name": "password",
                    "type": "password",
                    "required": "true"
                },
                "label": "Password",
            }]
REGISTER_FORM_INPUTS = [{
                "attributes": {
                    "id": "id_username",
                    "name": "username",
                    "type": "text",
                    "maxlength": "250",
                    "required": "true"
                },
                "label": "Username",
            },
            {
                "attributes": {
                    "id": "id_email",
                    "name": "email",
                    "type": "email",
                    "maxlength": "254",
                    "required": "true"
                },
                "label": "Email Address",
            },
            {
                "attributes": {
                    "id": "id_password1",
                    "name": "password1",
                    "type": "password",
                    "required": "true",
                    "autocomplete": "new-password"
                },
                "label": "Password",
            },
            {
                "attributes": {
                    "id": "id_password2",
                    "name": "password2",
                    "type": "password",
                    "required": "true",
                    "autocomplete": "new-password"
                },
                "label": "Password Confirmation",
            }]


def homepage(request):
    template_name = "app/homepage.html"

    tech = {
            'python': ['E-commerce', 'Hotel Booking App'], 
            'html':['E-commerce', 'Hotel Booking App', 'Portfolio'],
            'css':['AmazingMe', 'Coding Journey'],
        }
    """
    comment:
        inside the card have context, got the key of tech-card
        dict:
        techname
        project_list:
        {
            name:
            tech list:
            tag name: (marker??)

            exp:
            1: {   
                name: Amazingme
                tech_list: ['python', 'javascript', 'css']
            }
            

        }
    
    """
    tech = dict(sorted(tech.items()))
    
    context = {
        "name" : 'item name',
        "logo" : 'icons/bookmark_outline.html',
        "link" : 'homepage',
        "tech" : tech 

    }
    return render(request, template_name , context)


# def get_user(request):
#     current_user = request.user
#     print(current_user.id)

# def get_projects(request):
    #current_user = request.user
    #profile = current_user.profile
    #print(profile1.project_set.all())

# def filter_projects(request, marker):

    
def register(request):
    # populate forms
    context = {"register_form_inputs": REGISTER_FORM_INPUTS}
    template = "app/register_page.html"

    if request.user.is_authenticated:
        return redirect('homepage')

    if request.method == "POST":
        form = CreateUserForm(request.POST) # here we are essentially overriding the previous value
        
        """
        as of now, the form does not validate if the passwords match or not in real time before submitting the form
        """
        
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, f'Account was created for {user}')

            return redirect('login')

    return render(request, template, context)

# page for login user
def login_page(request):
    # populate forms
    context = { "login_form_inputs": LOGIN_FORM_INPUTS }
    template = "app/login_page.html"

    if request.user.is_authenticated:
        return redirect('homepage')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('homepage')

        messages.info(request, "Username/Password is incorrect")
        return redirect('login')

    return render(request, template, context)

def logout_user(request):
    # remove the session id and get user back to the login page
    logout(request)
    return redirect('login')


# search feature
"""def searchProjects(request):
    searchQuery = ""
    
    if request.GET.get('searchQuery'):
        searchQuery = request.GET.get('searchQuery')

    # We will have a query set of skills here
    markers = Marker.objects.filter(title__icontains = searchQuery)

    projects = Project.objects.distinct().filter(
        Q(project_name__icontains = searchQuery) |
        Q(markers__in = markers) | 
        Q(project_description = searchQuery))
    context = {"projects": projects, "search_query": searchQuery}

    return render(request, "app/homepage.html", context)
"""

def langing_page(request):
    template = "app/landing_page.html"
    context = {
        "site_title": "design your\ncoding journey",
        "site_description": "Coding Journey is a journal for programmers. Mark your current destination, create your coding path, explore other coders' journey and more!"
    }

    return render(request, template, context)

# Project List Display

dummyData = [ { 
        "project_id": 1, 
        "project_name": "project 1", 
        "project_description" : "Lorem ipsum",
        "markers": [], 
        "likes": 1, 
        "start_date": Date(2022, 2, 2),
        "end_date": Date(2022, 3, 2),
        "project_url": "https://github.com/"
    },
    { 
        "project_id": 2, 
        "project_name": "project 2", 
        "project_description" : "Lorem ipsum",
        "markers": [], 
        "likes": 1, 
        "start_date": Date(2022, 2, 2),
        "end_date": Date(2022, 3, 2),
        "project_url": "https://github.com/"
    },
    { 
        "project_id": 3, 
        "project_name": "project 3", 
        "project_description" : "Lorem ipsum",
        "markers": [], 
        "likes": 1, 
        "start_date": Date(2022, 2, 2),
        "end_date": Date(2022, 3, 2),
        "project_url": "https://github.com/"
    },
    { 
        "project_id": 3, 
        "project_name": "project 3", 
        "project_description" : "Lorem ipsum",
        "markers": [], 
        "likes": 1, 
        "start_date": Date(2022, 2, 2),
        "end_date": Date(2022, 3, 2),
        "project_url": "https://github.com/"
    },
    { 
        "project_id": 3, 
        "project_name": "project 3", 
        "project_description" : "Lorem ipsum",
        "markers": [], 
        "likes": 1, 
        "start_date": Date(2022, 2, 2),
        "end_date": Date(2022, 3, 2),
        "project_url": "https://github.com/"
    },
    { 
        "project_id": 3, 
        "project_name": "project 3", 
        "project_description" : "Lorem ipsum",
        "markers": [], 
        "likes": 1, 
        "start_date": Date(2022, 2, 2),
        "end_date": Date(2022, 3, 2),
        "project_url": "https://github.com/"
    },
]

def projectList(request):
    context = { 
        "projectList": dummyData, 
        "header": ["Project Name", "Date Posted", ""]
    }
    return render(request, "components\project_list.html", context)



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

def how_it_works(request):
    return render(request, 'app/how_it_works_page.html', {})

def about_us(request):
    return render(request, 'app/about_us_page.html', {})

def setting(request):
    template = 'app/setting.html'
    user = request.user
    tech = {
            'python': ['E-commerce', 'Hotel Booking App'], 
            'html':['E-commerce', 'Hotel Booking App', 'Portfolio'],
            'css':['AmazingMe', 'Coding Journey'],
        }
    profile = Profile.objects.get(user=user)
    # get back the form that contain all the info of the user profile
    profile_form = ProfileForm(instance=profile)

    if request.method == "POST":
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)

        if profile_form.is_valid():
            profile_form.save()
            return redirect('setting')

    context = {
        "name" : 'item name',
        "logo" : 'icons/bookmark_outline.html',
        "link" : 'homepage',
        "tech" : tech,
        
    }

    return render(request, template, context)

def profile(request):
    template = 'app/profile.html'
    tech = {
            'python': ['E-commerce', 'Hotel Booking App'], 
            'html':['E-commerce', 'Hotel Booking App', 'Portfolio'],
            'css':['AmazingMe', 'Coding Journey'],
        }
    context = {
        "name" : 'item name',
        "logo" : 'icons/bookmark_outline.html',
        "link" : 'homepage',
        "tech" : tech,
    }
    return render(request, template, context)
    