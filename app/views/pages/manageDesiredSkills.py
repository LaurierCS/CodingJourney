from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from app.models import DesiredSkill
from app.views.injectors.desiredSkillInputInjection import *

@login_required(login_url='auth_page')
def manage_desired_skills_page(request):

    # find all desired skills
    ds = DesiredSkill.objects.filter(user_id=request.user.profile)

    template_name = "app/manage_desired_skills.html"
    context = {
        "profile": request.user.profile,
        "desired_skills": ds,
        "ds_count": len(ds)
    }

    desired_skill_input_injection(request, context=context)
    return render(request, template_name, context)