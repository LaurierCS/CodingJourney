from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from app.models import Experience, Profile

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