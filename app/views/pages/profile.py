from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from app.models import Experience, Profile

@login_required(login_url='auth_page')
def profilepage(request):
    document_title = "Profile"
    page_header = ""
    # PUT ALL OTHER DATA, QUERIES ETC BELOW HERE
    profile = request.user.profile
    num_exp = len(Experience.objects.filter(profile=profile))
    # testing for getting other user profile
    profiles = Profile.objects.all()

    template_name = "app/profile.html"
    context = {
        "document_title":document_title,
        "page_header": page_header,
        "profile":profile,
        "profiles": profiles,
        "num_exp": num_exp,
    }
    return render(request, template_name, context)