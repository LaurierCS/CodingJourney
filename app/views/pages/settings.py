from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from app.views import injectors
from app.models import Experience, DesiredSkill
from app.forms import UserSettingForm
import app.views.injectors as Injectors

@login_required(login_url='auth_page')
def settingspage(request):
    document_title = "Setting"
    page_header = ""
    # PUT ALL OTHER DATA, QUERIES ETC BELOW HERE
    profile = request.user.profile
    setting_form = UserSettingForm(instance=profile)


    # print(desired_skills)

    template_name = "app/setting.html"

    if request.method == "POST":
        setting_form = UserSettingForm(request.POST, request.FILES, instance=profile)
        if setting_form.is_valid():
            setting_form.save()
            messages.success(request, 'Profile details updated.')
            return redirect('settings_page')
        else:
            messages.warning(request, 'Incorrect detail change.')

    desired_skills = DesiredSkill.objects.filter(user_id=profile)
    experiences = Experience.objects.filter(profile=profile)
            
    context = {
        "document_title":document_title,
        "page_header": page_header,
        "profile":profile,
        "desired_skills": desired_skills,
        "experiences": experiences,
        "setting_form":setting_form,
    }
    return render(request, template_name, context)