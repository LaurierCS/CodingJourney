# DJANGO IMPORTS
from django.http import HttpResponseBadRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.core import serializers
from django.db import connection
from django.contrib import messages
from django.db.models import Q, F,Value, IntegerField

# Django Auth
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

@login_required(login_url='auth_page')
def dashboard(request):

    # redirect user back to auth_page if not logged in
    if not request.user.is_authenticated:
        return redirect("auth_page")

    document_title = "Skill Tree"
    profile = request.user.profile
    experiences = Experience.objects.filter(profile=profile)
    tree_json = TreeQueries.getTrimmedTree(profile) # todo: profile to function when update_ds_description is merged.
    # tech_roadmap = profile.tech_roadmap

    template_name = "app/dashboard.html"
    context = {
        "document_title": document_title,
        "profile": profile,
        "experiences":experiences,
        "tree_json": tree_json
        # "tech_roadmap":tech_roadmap
    }
    return render(request, template_name, context)

def allexperiences(request):
    document_title = "Roadmap & Experiences"
    # PUT ALL OTHER DATA, QUERIES ETC BELOW HERE
    profile=request.user.profile
    experiences_qs = Experience.objects.filter(profile=profile).order_by('start_date') 
    experiences = experiences_qs

    template_name = "components/project_list.html"
    context = {
        "document_title":document_title,
        "profile":profile,
        "experiences":experiences,
    }
    for experience in experiences:
        print(experience)
    return render(request, template_name, context)

@login_required(login_url='auth_page')
def profilepage(request):
    document_title = "Profile"
    page_header = ""
    # PUT ALL OTHER DATA, QUERIES ETC BELOW HERE
    profile = request.user.profile
    num_exp = len(Experience.objects.filter(profile=profile))
    # testing for getting other user profile
    profiles = Profile.objects.all()

    template_name = "app/profile.html"
    context = {
        "document_title":document_title,
        "page_header": page_header,
        "profile":profile,
        "profiles": profiles,
        "num_exp": num_exp,
    }
    return render(request, template_name, context)

@login_required(login_url='auth_page')
def otherprofilepage(request, username):
    profile = Profile.objects.get(user__username=username)
    experiences = Experience.objects.filter(profile=profile)
    num_exp = len(experiences)

    template_name = "app/other_user_profile.html"
    context = {
        "profile":profile,
        "experiences": experiences,
        "num_exp":num_exp,
    }
    return render(request, template_name, context)

@login_required(login_url='auth_page')
def settingspage(request):
    document_title = "Setting"
    page_header = ""
    # PUT ALL OTHER DATA, QUERIES ETC BELOW HERE
    profile = request.user.profile
    setting_form = UserSettingForm(instance=profile)
    template_name = "app/setting.html"

    if request.method == "POST":
        setting_form = UserSettingForm(request.POST, request.FILES, instance=profile)
        if setting_form.is_valid():
            setting_form.save()
            messages.success(request, 'Profile details updated.')
            return redirect('settings_page')
        else:
            messages.warning(request, 'Incorrect detail change.')
            
    context = {
        "document_title":document_title,
        "page_header": page_header,
        "profile":profile,
        "setting_form":setting_form,
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
            return redirect('dashboard_page')
        else:
            messages.info(request, 'Username or password is incorrect')
    return redirect("auth_page")

def registration_handler(request):
    if request.method == 'POST':
        register_form = CreateUserForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            username = register_form.cleaned_data.get('username')
            password = register_form.cleaned_data.get("password1")
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('dashboard_page')
        else:
            if "password2" in register_form.errors:
                for validationError in register_form.errors.as_data()['password2']:
                    messages.info(request, validationError.message)
            if "username" in register_form.errors:
                for validationError in register_form.errors.as_data()['username']:
                    messages.info(request, validationError.message)
    
    return redirect(reverse("auth_page") + "?form=register")

def logout_handler(request):

    if not request.user.is_authenticated:
        return redirect("auth_page")

    # remove the session id and get user back to the login page
    logout(request)
    return redirect('login')

def experience_input_handler(request):
    
    if request.method == 'POST':
        form = ExperienceInputform(request.POST)
        
        if (form.is_valid()):
            form_data = form.cleaned_data
            experience_instance = Experience.objects.create(
                profile=request.user.profile,
                name=form_data["name"],
                kind=form_data["kind"],
                description=form_data["description"],
                start_date=form_data["start_date"],
                end_date=form_data["end_date"],
                project_link=form_data["project_link"],
                image=form_data["image"],
            )
            skills_ids = [skill.id for skill in form_data['skills']]
            print(skills_ids)
            context = {
                'form': form,
            } 
            # experience_instance.skills.set(form_data["skills"])
            return render(request, 'app/experience_form.html', context=context)
        else: 
            for field in form:
                print("Field Error:", field.name,  field.errors)
            # print(form_data)        
            context = {
                'form': form,
            } 
            return render(request, 'app/experience_form.html', context=context)
        
    
    else: 
        form = ExperienceInputform()
        context = {
            'form': form,
        } 
        return render(request, 'app/experience_form.html', context=context)
            

class TreeQueries:
    def getFullTree():
        skill_tree = Skill.objects.all()
        serialized = serializers.serialize('json', skill_tree, ensure_ascii=False)
        return serialized
    
    def getTrimmedTree(profile):
        # todo: 1. need to include parent of nodes, always.
        # todo: 2. need to include user as root.
        # todo: 3. condense all information into the node.
        # desired skills query 
        desired_skill_objects = DesiredSkill.objects.filter(user_id=profile).order_by('skill')
        
        # user has no desired skill set, so we just return a user node
        if len(desired_skill_objects) < 1:
            # query user node
            skill_query = Skill.objects.filter(id="user")
            serialized_query = serializers.serialize("json", skill_query, ensure_ascii=False)
            return serialized_query

        # retrieve list of connected skills
        subset_skills = desired_skill_objects.values_list('skill', flat=True)
        print(subset_skills)
        # query skill objects associated w/ desired skills
        skill_tree_qs = Skill.objects.filter(id=subset_skills[0])
        print(skill_tree_qs)

        # pdb.set_trace()
        for i in range(1, len(subset_skills)):
            skill_tree_q = Skill.objects.filter(id=subset_skills[i])
            skill_tree_qs = skill_tree_qs.union(skill_tree_q)
        
        # skill_tree_qs = Skill.objects.filter(id__in=subset_skills)
        
        # skill_query contains parents of all desired skills objects
        skill_query = Skill.objects.filter(id__in=skill_tree_qs.values_list('parentId', flat=True))
        print(skill_query)
        while (skill_query.exists()): 
            # create union of skill_query objects w/ skill objects
            skill_tree_qs = skill_tree_qs.union(skill_query)
            # requery skill_query objects to reference parents of previous skill_query
            skill_query = Skill.objects.filter(id__in=skill_query.values_list('parentId', flat=True))
        
        desired_skill_dict = {}
        for skill in desired_skill_objects:
            desired_skill_dict[skill.skill_id] = skill
        

        skill_tree = skill_tree_qs.values()
        for skill in skill_tree:
            if (skill['id'] not in desired_skill_dict): 
                continue
            ds = desired_skill_dict[skill['id']]
            skill["proficiency"] = ds.proficiency
            skill["description"] = ds.description
            skill["experiences"] = list(ds.experience_set.all().values())
            for exp in skill["experiences"]:
                if exp['start_date']:
                    exp['start_date'] = exp['start_date'].strftime("%m/%d/%Y")
                if exp["end_date"]:
                    exp['end_date'] = exp['end_date'].strftime("%m/%d/%Y")
            skill["proficiency_text"] = DesiredSkill.proficiency_choices[int(skill["proficiency"])][1]
        

        # serialized = serializers.serialize('json', skill_tree_qs, ensure_ascii=False)
        serialized = json.dumps(list(skill_tree), ensure_ascii=False)
        return serialized


    def populateDatabase(request): 
        #Open the JSON file
        tree_json_path = os.path.join("static/json/full_tree.json")
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

def update_desired_skill_description(request):
    if request.method == "POST":
        form = UpdateDesiredSkillDescriptionForm(request.POST)
        ds = DesiredSkill.objects.filter(user_id=request.user.profile, skill__name=form['skill_name'].value())
        ds.update(description=form['description'].value())
        return HttpResponse()
    
    return HttpResponseBadRequest()

# class SkillsSerializer(serializers.ModelSerializer): 
    
#     class Meta: 
#         model = Skill
#         fields = ('parentId', 'id', 'name', 'icon_HREF', 'node_type', 'experiences', 'proficiency', 'description')

#     def get_experiences(self):
#         return self.context['item'].experience
    
#     def get_proficiency(self): 
#         return self.context['item'].proficiency
    
#     def get_description(self):
#         return self.context['item'].description

class SearchQueries:

    def searchHandle(request):

        if request.method == "POST":
            return HttpResponseBadRequest("Does not accept POST requests.")

        search = request.GET.get("search_query")

        if search is None:
            return HttpResponseBadRequest("No search query.")

        scope = request.GET.get("search_scope")
        quick_query = request.GET.get("quick_query") == "true" # make it a boolean value

        if scope == "all":
            users = SearchQueries.search_users(search)
            skills = SearchQueries.search_skills(search)
            experiences = SearchQueries.search_experiences(search)

            results = users + experiences + skills
        elif scope == "user":
            results = SearchQueries.search_users(search)
        
        elif scope == "skill":
            results = SearchQueries.search_skills(search)
        
        elif scope == "experience":
            results = SearchQueries.search_experiences(search)

        else:
            # out of scope
            results = []

        context = {
            "search": search,
            "scope": scope,
            "results": results,
            "quick_query": quick_query,
            "entries": len(results),
        }

        if quick_query:
            return JsonResponse(context)

        template = "app/search_page.html"

        return render(request, template, context)

    def search_users(query_string):
        # todo: add limit to query result, aka pagination
        result = []

        splitted = query_string.split(" ")
        first_name = splitted[0]
        last_name = splitted[0]
        if len(splitted) > 1:
            last_name = splitted[1]

        best_matches = Profile.objects.filter(
            Q(user__username__startswith=query_string) |
            Q(first_name__startswith=first_name) | 
            Q(last_name__startswith=last_name)
        ).annotate(weight=Value(0, IntegerField())) \
            .values("user__username", "first_name", "last_name", "image", "bio")

        # todo: able to search for possible users that contain query string.
        # best_matches_ids = best_matches.values_list("id", flat=True)

        # users = Profile.objects.filter(
        #     Q(user__username__icontains=query_string) |
        #     Q(first_name__icontains=first_name) | 
        #     Q(last_name__icontains=last_name)
        #     ) \
        #         .annotate(weight=Value(1, IntegerField()))

        # bug: lost user__username after union. Unknown reason.
        # all_users = best_matches.union(users).order_by("weight")

        # todo: make url to go to user profile.
        for user in best_matches:
            result.append({
                "text": user["user__username"] + " - " + user["first_name"] + " " + user["last_name"],
                "image": user["image"],
                "first_name": user["first_name"],
                "last_name": user["last_name"],
                "bio": user["bio"],
                "username": user['user__username'],
                "category": "user",
                "url": "",
            })

        return result

    def search_skills(query_string):
        # todo: add limit to query result, aka pagination

        result = []

        best_matches = Skill.objects.filter(name__startswith=query_string) \
            .exclude(name="User")

        best_matches_ids = best_matches.values_list("id", flat=True)

        skills = Skill.objects.filter(name__icontains=query_string) \
            .exclude(name="User") \
                .exclude(id__in=best_matches_ids)[:10]

        '''
            Union is not possible when trying to limit queryset.
            Gives error: 'OFFSET/LIMIT operation cannot be done in subqueries'
        '''
        # all_skills = best_matches.union(skills).order_by('weight', 'name').values()

        best_skills = best_matches.values()
        potential_skills = skills.values()

        # todo: add url to show all experiences related to such skill.
        for skill in best_skills:
            result.append({
                "text": skill["name"],
                "image": skill["icon_HREF"],
                "category": "skill" if skill["node_type"] != "C" else "skill category",
                "url": "",
            })

        for skill in potential_skills:
            result.append({
                "text": skill["name"],
                "image": skill["icon_HREF"],
                "category": "skill" if skill["node_type"] != "C" else "skill category",
                "url": "",
            })

        return result
    
    def search_experiences(query_string):
        # todo: add limit to query result, aka pagination
        result = []

        best_matches = Experience.objects.filter(name__startswith=query_string)
        #     .annotate(weight=Value(0, IntegerField()))
        best_matches_ids = best_matches.values_list("id", flat=True)
        experiences = Experience.objects.filter(name__icontains=query_string) \
            .exclude(id__in=best_matches_ids)[:10]

        # print(best_matches.all().values("profile__user__username"))
        # print(experiences.all().values("profile__user__username"))

        # all_experiences = best_matches.union(experiences, all=True).order_by("weight", "name").values("name", "image", "description", "project_link")

        best_experiences = best_matches.values(
            "image",
            "name",
            "description",
            "project_link",
            "profile__user__username", 
            "profile__image", 
            "id",
            "likes_amount",
            "start_date",
            "end_date",
            )

        potential_matches = experiences.values(
            "image",
            "name",
            "description",
            "project_link",
            "profile__user__username", 
            "profile__image", 
            "id",
            "likes_amount",
            "start_date",
            "end_date",
            )

        # print(best_experiences)

        for exp in best_experiences:
            # search for skills related to experience
            skills = DesiredSkill.objects.filter(experience__id=exp['id']).annotate(skill_name=F("skill__name"), skill_image=F("skill__icon_HREF")).values("skill_name", "skill_image")

            result.append({
                "text": exp["name"],
                "image": exp["image"],
                "description": exp['description'],
                'profile': {
                    'username': exp['profile__user__username'],
                    'image': exp['profile__image']
                },
                'skills': list(skills),
                'kind': best_matches.filter(id=exp['id']).first().get_kind_display(),
                "url": exp["project_link"],
                "likes": exp["likes_amount"],
                "start_date": exp["start_date"].strftime("%d %B, %Y") if exp['start_date'] is not None else None,
                "end_date": exp["end_date"].strftime("%d %B, %Y") if exp['end_date'] is not None else None,
                "category": "experience",
            })

        # append the potential searches
        for exp in potential_matches:
                        # search for skills related to experience
            skills = DesiredSkill.objects.filter(experience__id=exp['id']).annotate(skill_name=F("skill__name"), skill_image=F("skill__icon_HREF")).values("skill_name", "skill_image")

            kind = best_matches.filter(id=exp['id']).first()

            if kind is not None:
                kind = kind.get_kind_display()

            result.append({
                "text": exp["name"],
                "image": exp["image"],
                "description": exp['description'],
                'profile': {
                    'username': exp['profile__user__username'],
                    'image': exp['profile__image']
                },
                'skills': list(skills),
                'kind': kind,
                "url": exp["project_link"],
                "likes": exp["likes_amount"],
                "start_date": exp["start_date"].strftime("%d %B, %Y") if exp['start_date'] is not None else None,
                "end_date": exp["end_date"].strftime("%d %B, %Y") if exp['end_date'] is not None else None,
                "category": "experience",
            })

        return result