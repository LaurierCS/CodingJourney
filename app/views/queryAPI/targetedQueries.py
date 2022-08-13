from django.http import HttpResponseBadRequest, JsonResponse, HttpResponseNotFound
from django.shortcuts import render
from django.db.models import F
from app.models import *

class TargetedQueries:
    def experienceGetter(request): 
        if request.method == "POST":
            return HttpResponseBadRequest("Does not accept POST requests.")

        exp_id = request.GET.get("exp_id")

        if exp_id is None:
            return HttpResponseBadRequest("No experience ID given.")

        try:
            print("""
            


            """)
            print(exp_id)
            print("""
            

            
            """)
            experience = Experience.objects.filter(pk=exp_id)
        except Experience.DoesNotExist:
            return HttpResponseBadRequest("No element exists with id:" + exp_id)
        
        
        exp_values = experience.values(
            "image",
            "name",
            "description",
            "project_link",
            "profile__user__username", 
            "profile__image", 
            "id",
            "likes_amount",
            "start_date",
            "end_date",
            )

        exp = exp_values[0]
        skills = DesiredSkill.objects.filter(experience__id=exp['id']).annotate(skill_name=F("skill__name")).values("skill_name")
        experience_obj = {
                "name": exp["name"],
                "image": exp["image"],
                "description": exp['description'],
                'profile': {
                    'username': exp['profile__user__username'],
                    'image': exp['profile__image']
                },
                'skills': list(skills),
                # 'kind': best_matches.filter(id=exp['id']).first().get_kind_display(),
                "url": exp["project_link"],
                "likes": exp["likes_amount"],
                "start_date": exp["start_date"].strftime("%d %B, %Y") if exp['start_date'] is not None else None,
                "end_date": exp["end_date"].strftime("%d %B, %Y") if exp['end_date'] is not None else None,
                "category": "experience",
            }
        context = {
            "experience": experience_obj,
        }

        return JsonResponse(context)

    def getExperiencesBySkills(request, skill_name):
        print(skill_name)
        document_title = "Roadmap & Experiences"
        # PUT ALL OTHER DATA, QUERIES ETC BELOW HERE
        
        skill=DesiredSkill.objects.filter(skill=Skill.objects.get(name=skill_name))
        experiences_qs = Experience.objects.filter(skills__in=skill).order_by('start_date')
        print(experiences_qs)
        experiences = experiences_qs.annotate(username=F("profile__user__username"))

        template_name = "components/project_list.html"
        context = {
            "document_title":document_title,
            "experiences":experiences,
            "type": "skill_search_click"
        }
        return render(request, template_name, context)

    def getProfilePictureByUsername(request):
        username = request.GET.get('username')

        if username is not None:
            profile = Profile.objects.get(user__username=username)
            if profile is None:
                return HttpResponseNotFound(f"No user with username: {username}")
            data = {
                "url": profile.image.url
            }

            return JsonResponse(data)