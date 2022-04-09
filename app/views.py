"""
django.contrib.auth.decorators
- module that used for restricted users for certain functions in our app
from django.contrib.auth.forms import UserCreationForm
- A form that creates a user, with no privileges, from the given username and password.
"""

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
# from .forms import *
# from .models import *


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
