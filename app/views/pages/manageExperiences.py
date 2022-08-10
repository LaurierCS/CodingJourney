from django.shortcuts import render
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from app.models import Experience
from app.views.injectors.experienceInputInjection import *

@login_required(login_url="auth_page")
def manage_experiences_page(request):

    if request.POST:
        return HttpResponseBadRequest("Does not support POST request.")
    
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