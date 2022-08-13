from django.shortcuts import render
from app.forms import ExperienceInputform
from app.models import DesiredSkill, Experience
from app.views.injectors.desiredSkillInputInjection import *
from app.views.injectors.experienceInputInjection import *
from app.views.pages.manageDesiredSkills import *

def experience_input_handler(request):
    if request.method == 'POST':
        user = request.user.profile
        form = ExperienceInputform(data=request.POST, user_id=user)
        
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
            desired_skills = DesiredSkill.objects.filter(skill__in=skills_ids).values_list('pk')
            for skill_tuple in desired_skills: 
                experience_instance.skills.add(skill_tuple[0])
            context = {
                'form': form,
            }

            # redirect user to manage_experiences page
            profile = request.user.profile
            experiences = Experience.objects.filter(profile=profile)
            template = "app/manage_experiences.html"
            context = {
                "profile": profile,
                "experiences": experiences,
                "experience_count": len(experiences),
                "method": "POST"
            }
            experience_input_injection(request, context=context)
            return render(request, template, context)
        else: 
            for field in form:
                print("Field Error:", field.name,  field.errors)
            # print(form_data)        
            # redirect user to manage_experiences page
            profile = request.user.profile

            experiences = Experience.objects.filter(profile=profile)

            template = "app/manage_experiences.html"
            context = {
                "profile": profile,
                "experiences": experiences,
                "experience_count": len(experiences),
            }
            experience_input_injection(request, context=context, form=form)
            return render(request, template, context)
    
    else: 
        user = request.user.profile
        context = {} 
        experience_input_injection(request, context=context)
        return render(request, 'app/manage_experiences.html', context=context)
    
def experience_update_handler(request, id): 
    if request.method == 'POST':
        user = request.user.profile
        form = ExperienceInputform(data=request.POST, user_id=user)
        
        if (form.is_valid()):
            form_data = form.cleaned_data
            experience_instance = Experience.objects.get(pk=id)
            experience_instance.profile=request.user.profile,
            experience_instance.name=form_data["name"],
            experience_instance.kind=form_data["kind"],
            experience_instance.description=form_data["description"],
            experience_instance.start_date=form_data["start_date"],
            experience_instance.end_date=form_data["end_date"],
            experience_instance.project_link=form_data["project_link"],
            experience_instance.image=form_data["image"], 
            experience_instance.skills=form_data["skills"]
            experience_instance.save()

            # redirect user to manage_experiences page
            profile = request.user.profile

            experiences = Experience.objects.filter(profile=profile)

            template = "app/manage_experiences.html"
            context = {
                "profile": profile,
                "experiences": experiences,
                "experience_count": len(experiences),
            }
            experience_input_injection(request, context=context)
            return render(request, template, context)
        else: 
            for field in form:
                print("Field Error:", field.name,  field.errors)
            # print(form_data)        
            # redirect user to manage_experiences page 
            profile = request.user.profile

            experiences = Experience.objects.filter(profile=profile)

            template = "app/manage_experiences.html"
            context = {
                "profile": profile,
                "experiences": experiences,
                "experience_count": len(experiences),
            }
            experience_input_injection(request, context=context, form=form)
            return render(request, template, context)
    
    else: 
        exp_instance = Experience.objects.get(pk=id)

        user = request.user.profile
        form = ExperienceInputform(data=request.POST, user_id=user, kwargs={
            "name": exp_instance.name, 
            "kind": exp_instance.kind, 
            "description": exp_instance.description, 
            "start_date": exp_instance.start_date, 
            "end_date": exp_instance.end_date, 
            "project_link": exp_instance.project_link, 
            "image": exp_instance.image, 
        })
        context = {
            'form': form,
        } 
        return render(request, 'app/experience_update_form.html', context=context)