from django.http import HttpResponseBadRequest, HttpResponse
from app.models import *
from app.forms import LikeExperienceForm

class LikeHandlers():
    def exp_like_handler(request):

        if request.POST:
            form = LikeExperienceForm(request.POST)
            exp_id = form['exp_id'].value()
            profile = request.user.profile

            exp = Experience.objects.get(pk=int(exp_id))

            if exp in profile.liked_experiences.all():
                # unlike
                profile.liked_experiences.remove(exp)
                exp.decrement_like()
            else:
                # like
                profile.liked_experiences.add(exp)
                exp.increment_like()

            return HttpResponse()

        return HttpResponseBadRequest("GET request not allowed.")

    def getDesiredSkillByUserAndSkill(request, skill_name): 
        user = request.user.profile
        skill = Skill.objects.get(skill_name)
        ds = DesiredSkill.objects.filter(skill=skill)
        return
        # ds_obj = {
        #     "name": exp["name"],
        #     "image": exp["image"],
        #     "description": exp['description'],
        #     'profile': {
        #         'username': exp['profile__user__username'],
        #         'image': exp['profile__image']
        #     },
        #     'skills': list(skills),
        #     # 'kind': best_matches.filter(id=exp['id']).first().get_kind_display(),
        #     "url": exp["project_link"],
        #     "likes": exp["likes_amount"],
        #     "start_date": exp["start_date"].strftime("%d %B, %Y") if exp['start_date'] is not None else None,
        #     "end_date": exp["end_date"].strftime("%d %B, %Y") if exp['end_date'] is not None else None,
        #     "category": "experience",
        # }