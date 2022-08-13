from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from app.models import Experience

@login_required(login_url='auth_page')
def allexperiences(request):
    document_title = "Roadmap & Experiences"
    # PUT ALL OTHER DATA, QUERIES ETC BELOW HERE
    profile=request.user.profile
    experiences_qs = Experience.objects.filter(profile=profile).order_by('start_date') 
    experiences = experiences_qs

    template_name = "components/project_list.html"
    context = {
        "document_title":document_title,
        "profile":profile,
        "experiences":experiences,
    }
    for experience in experiences:
        print(experience)
    return render(request, template_name, context)