from django.shortcuts import redirect
from app.forms import DeleteDsOrExpForm
from app.models import DesiredSkill
from app.views.injectors.desiredSkillInputInjection import *
from app.views.pages.manageDesiredSkills import *

def delete_desired_skill(request):

    if request.POST:
        form = DeleteDsOrExpForm(request.POST)

        if form.is_valid():
            ds_names = form['names'].value()
            callback_url = form['callbackurl'] if 'callbackurl' in form else None

            list_of_names = ds_names.split(',')

            ds = DesiredSkill.objects.filter(skill__name__in=list_of_names, user_id=request.user.profile)

            for skill in ds:
                skill.delete()

            if callback_url is not None:
                return redirect(callback_url)