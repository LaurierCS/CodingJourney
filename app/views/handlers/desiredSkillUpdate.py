from django.http import JsonResponse, HttpResponseBadRequest
from app.forms import UpdateDesiredSkillDescriptionForm
from app.models import DesiredSkill, Skill
from views.injectors.desiredSkillInputInjection import *
from views.pages.manageDesiredSkills import *

def update_desired_skill(request):
    if request.method == "POST" and request.user.is_authenticated:
        form = UpdateDesiredSkillDescriptionForm(request.POST)
        ds = DesiredSkill.objects.filter(user_id=request.user.profile, skill__name=form['skill_name'].value())

        if len(ds) > 0:
            ds.update(description=form['description'].value(), proficiency=form['proficiency'].value())
        else:
            # create new desired skill
            skill = Skill.objects.get(name =form['skill_name'].value())

            ds = DesiredSkill.objects.create(
                user_id=request.user.profile,
                description=form['description'].value(),
                skill=skill,
                proficiency=form['proficiency'].value()
            )

        new_values = ds.values("description", "proficiency")[0]

        new_values["proficiency_text"] = ds.first().get_proficiency_display()
        
        return JsonResponse(new_values)
    
    return HttpResponseBadRequest()