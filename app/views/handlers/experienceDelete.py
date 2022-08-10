from django.shortcuts import redirect
from app.forms import DeleteDsOrExpForm
from app.models import Experience
from views.injectors.desiredSkillInputInjection import *
from views.pages.manageDesiredSkills import *

def delete_exp(request):

    if request.POST:
        form = DeleteDsOrExpForm(request.POST)

        if form.is_valid():
            exp_ids = form['names'].value()
            callback_url = form['callbackurl'] if 'callbackurl' in form else None

            list_of_ids = exp_ids.split(',')

            experiences = Experience.objects.filter(id__in=list_of_ids, profile=request.user.profile)

            for exp in experiences:
                exp.delete()
            
            if callback_url is not None:
                return redirect(callback_url)

    return redirect("manage_experiences_page")