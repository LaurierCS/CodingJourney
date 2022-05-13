# DJANGO IMPORTS
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from django.core import serializers
from django.db import connection


from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm

import json
import os

from django.apps import apps

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
    document_title = "Login"
    
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
    context = {
        "document_title": document_title,
        "register_form": register_form
    }
    return render(request, template_name, context)


def dashboard(request):
    document_title = "Skill Tree"
    # PUT ALL OTHER DATA, QUERIES ETC BELOW HERE
    profile = request.user.profile
    experiences = Experience.objects.filter(profile=profile)
    # tech_roadmap = profile.tech_roadmap

    

    template_name = "app/homepage.html"
    context = {
        "document_title": document_title,
        "profile": profile,
        "experiences":experiences,
        # "tech_roadmap":tech_roadmap
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
            return redirect('home')
        else:
            messages.info(request, 'Username or password is incorrect')
    return

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
    return

def logout_handler(request):
    # remove the session id and get user back to the login page
    logout(request)
    return redirect('login')

def experience_input_handler(request):
    if request.method == 'POST':
        form = ExperienceInputform(request.POST)
        if form.is_valid():
            new_instance = Experience.objects.create()
            

class TreeQueries:
    def getFullTree():
        skill_tree = Skill.objects.all()
        serialized = serializers.serialize('json', skill_tree, ensure_ascii=False)
        return serialized
    
    def getTrimmedTree(user):
        # todo: 1. need to include parent of nodes, always.
        # todo: 2. need to include user as root.
        # todo: 3. condense all information into the node.
        subset_skills = DesiredSkill.objects.all().values_list('skill', flat=True)

        print(Skill.objects.filter(id="user").values())

        # get all of the skills appearing in the desired skills subset
        skill_tree_nodes = Skill.objects.filter(id__in=subset_skills)
        # get ids of all parents in desired skills subset
        skill_tree_node_parents = skill_tree_nodes.values_list('parentId', flat=True)
        # get all categories that are parents of skills in desired skills subset
        skill_tree_categories = Skill.objects.filter(node_type="C").filter(id__in=skill_tree_node_parents)
        skill_tree = skill_tree_categories.union(skill_tree_nodes)

        print(DesiredSkill._meta.db_table)

        
        skill_tree = Skill.objects.raw('''
                SELECT *
                FROM app_desiredskill.skill
                ''')
                # FROM app_skill s
                # LEFT JOIN app_desiredskill on app_desiredskill.skill = s.id''')
        for skill in skill_tree: 
            print(skill.skill)

        # get all skills that are referenced by a foreign key in the DesiredSKills table s.t. skill.id = DesiredSkill.skill

        skill_tree = Skill.objects.raw('''
            WITH RECURSIVE skill_tree AS (
                SELECT *
                FROM app_skill s
                LEFT JOIN app_desiredskill ds on ds.skill = s.id

                UNION ALL 

                SELECT * 
                FROM app_skill sk 
                LEFT JOIN skill_tree st ON skill_tree.parentId = sk.id
            )

            Select * FROM skill_tree
        ''')
    
        serialized = serializers.serialize('json', skill_tree, ensure_ascii=False)
        
        # return serialized


    def populateDatabase(request): 
        #Open the JSON file
        tree_json_path = os.path.join("static/json/tree.json")
        f = open(tree_json_path)

        data = json.load(f)

        # tale all items from initial json and instantiate 
        # 
        for item in data: 
            id = item['id']
            name = item['label']
            node_type = item['node_type']
            if "icon_HREF" in item:
                icon_HREF = item['icon_HREF']
                Skill.objects.create(
                    id=id,
                    name=name,
                    icon_HREF=icon_HREF,
                    node_type=node_type
                )
            else: 
                Skill.objects.create(
                    id=id,
                    name=name,
                    node_type=node_type
                )
        
        for item in data: 
            if "parentId" in item:
                skill = Skill.objects.get(id=item["id"])
                parentId = Skill.objects.get(id=item["parentId"])
                skill.parentId = parentId
                skill.save()