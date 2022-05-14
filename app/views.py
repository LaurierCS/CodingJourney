# DJANGO IMPORTS
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from django.views import View

# FILE IMPORTS
from .models import *
from .forms import *


# ****************************************************************************
# TEMPLATE VIEWS - GET DATA, PERFORM OPERATIONS, AND RETURN A TEMPLATE
# ****************************************************************************
def langing_page(request):
    document_title = "Coding Journey"
    page_header = "Design your\ncoding journey"
    description = "Coding Journey is a journal for programmers. Mark your current destination, create your coding path, explore other coders' journey and more!"
    # PUT ALL OTHER DATA, QUERIES ETC BELOW HERE

    template = "app/landing_page.html"
    context = {
        "document_title": document_title,
        "page_header": page_header,
        "description": description
    }

    return render(request, template, context)


def authpage(request):

    form_type = request.GET.get('form_type', 'login')

    document_title = form_type
    
    register_form = CreateUserForm()
    # LOGIN AND REGISTRATION AUTHENTICATION
    if request.user.is_authenticated:
        return redirect('dashboard_page')
    elif request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, f'Account was created for {user}')

            return redirect('login')

    template_name = "app/auth_page.html"
    form  = CreateUserForm(request.POST)
    context = {
        "document_title": document_title,
        "register_form": register_form,
        "endpoint": 'login',
        "form": form
    }
    return render(request, template_name, context)

def dashboard(request):

    # redirect user back to auth_page if not logged in
    if not request.user.is_authenticated:
        return redirect("auth_page")

    document_title = "Skill Tree"
    profile = request.user.profile

    

    template_name = "app/homepage.html"
    context = {
        "document_title": document_title,
        "profile": profile,
    }
    return render(request, template_name, context)



def allexperiences(request):
    document_title = "Roadmap & Experiences"
    # PUT ALL OTHER DATA, QUERIES ETC BELOW HERE
    profile=request.user.profile
    experiences = Experience.objects.filter(profile=profile)
    tech_roadmap = profile.tech_roadmap

    template_name = "app/homepage.html"
    context = {
        "document_title":document_title,
        "profile":profile,
        "experiences":experiences,
        "tech_roadmap":tech_roadmap
    }
    return render(request, template_name, context)


def profilepage(request):
    document_title = ""
    page_header = ""
    # PUT ALL OTHER DATA, QUERIES ETC BELOW HERE
    profile = request.user.profile


    template_name = "app/homepage.html"
    context = {
        "document_title":document_title,
        "page_header": page_header,
        "profile":profile
    }
    return render(request, template_name, context)


def settingspage(request):
    document_title = "Setting"
    page_header = ""
    # PUT ALL OTHER DATA, QUERIES ETC BELOW HERE
    profile = request.user.profile

    template_name = "app/setting.html"
    context = {
        "document_title":document_title,
        "page_header": page_header,
        "profile":profile
    }
    return render(request, template_name, context)


# *************************************************************************************
# ENDPOINT VIEWS - ONLY PERFORM ACTIONS ON DATA OR RETURN DATA,  DONT RETURN A TEMPLATE
# *************************************************************************************
def login_handler(request):
    if request.user.is_authenticated:
        return redirect('dashboard_page')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            print("Logged In")
            return redirect('dashboard_page')
        else:
            messages.info(request, 'Username or password is incorrect')
    return redirect("auth_page")

def registration_handler(request):
    if request.method == 'POST':
        register_form = CreateUserForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            messages.success(
                request, f'Account created')
            print("Account created")

            username = register_form.cleaned_data.get('username')
            password = register_form.cleaned_data.get("password1")
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('dashboard_page')
        else:
            if "password2" in register_form.errors:
                print(register_form.errors["password2"])
            messages.info(request, 'Registration Failed')
    return redirect(reverse("auth_page") + "?form=register")

def logout_handler(request):
    # remove the session id and get user back to the login page
    logout(request)
    return redirect('landing_page')
