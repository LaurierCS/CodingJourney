from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from app.models import Experience

@login_required(login_url='auth_page')
def dashboard(request):

    # redirect user back to auth_page if not logged in
    if not request.user.is_authenticated:
        return redirect("auth_page")

    document_title = "Skill Tree"
    profile = request.user.profile
    experiences = Experience.objects.filter(profile=profile)
    # tech_roadmap = profile.tech_roadmap

    template_name = "app/dashboard.html"
    context = {
        "document_title": document_title,
        "profile": profile,
        "experiences":experiences,
        "editable": True,
    }
    return render(request, template_name, context)