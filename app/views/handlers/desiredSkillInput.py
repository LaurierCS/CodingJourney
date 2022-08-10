from django.shortcuts import render
from app.forms import DesiredSkillsInputForm
from app.models import DesiredSkill
from views.injectors.desiredSkillInputInjection import *
from views.pages.manageDesiredSkills import *


def desired_skill_input_handler(request): 
    context = {}
    if request.method == 'POST':
        user = request.user.profile
        form = DesiredSkillsInputForm(data=request.POST, user_id=user)         

        if (form.is_valid()):
            form_data = form.cleaned_data
            DesiredSkill.objects.create(
                user_id=request.user.profile,
                skill=form_data["skill"],
                proficiency=form_data["proficiency"],
                description=form_data["description"],
            ) 
            desired_skill_input_injection(request, context)
            # experience_instance.skills.set(form_data["skills"])
            return manage_desired_skills_page(request)
        else: 
            for field in form:
                print("Field Error:", field.name,  field.errors)
            ds = DesiredSkill.objects.filter(user_id=request.user.profile)

            template_name = "app/manage_desired_skills.html"
            context = {
                "profile": request.user.profile,
                "desired_skills": ds,
                "ds_count": len(ds)
            }

            desired_skill_input_injection(request, context=context, form=form)
            return render(request, template_name, context)
    else: 
        desired_skill_input_injection(request, context=context)
        return render(request, 'app/desired_skill_modal.html', context=context)