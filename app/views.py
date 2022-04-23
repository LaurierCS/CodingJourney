from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

# Create your views here
from .models import *
from .forms import CreateUserForm
from django.db.models import Q

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
        "logo" : 'svg/bookmark.html',
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
    if request.user.is_authenticated:
        return redirect('homepage')
    else:
        page = "register"
        form = CreateUserForm()
        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, f'Account was created for {user}')

                return redirect('login')
        context = { "page": page, "form": form}
        return render(request, 'app/loginregister_page.html', context)

# page for login user
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('homepage')
    else:
        page = "login"
        if request.method == 'POST':
            username = request.POST.get('username').lower()
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('homepage')
            else:
                messages.info(request, "Username/Password is incorrect")
                return redirect('login')

        context = {'page': page}
        return render(request, 'app/loginregister_page.html', context)

def logoutUser(request):
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
    template = "app/landingpage.html"
    context = {
        "site_title": "design your\ncoding journey",
        "site_description": "Coding Journey is a journal for programmers. Mark your current destination, create your coding path, explore other coders' journey and more!"
    }

    return render(request, template, context)


