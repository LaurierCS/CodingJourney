from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from django.db.models import Q, F,Value, IntegerField
from app.models import *

class SearchQueries:

    def searchHandle(request):

        if request.method == "POST":
            return HttpResponseBadRequest("Does not accept POST requests.")

        search = request.GET.get("search_query")

        if search is None:
            return HttpResponseBadRequest("No search query.")

        scope = request.GET.get("search_scope")
        quick_query = request.GET.get("quick_query") == "true" # make it a boolean value

        if scope == "all":
            users = SearchQueries.search_users(search)
            skills = SearchQueries.search_skills(search)
            experiences = SearchQueries.search_experiences(search)

            results = users + experiences + skills
        elif scope == "user":
            results = SearchQueries.search_users(search)
        
        elif scope == "skill":
            results = SearchQueries.search_skills(search)
        
        elif scope == "experience":
            results = SearchQueries.search_experiences(search)

        else:
            # out of scope
            results = []

        context = {
            "search": search,
            "scope": scope,
            "results": results,
            "quick_query": quick_query,
            "entries": len(results),
        }

        if quick_query:
            return JsonResponse(context)

        template = "app/search_page.html"

        return render(request, template, context)

    def search_users(query_string):
        # todo: add limit to query result, aka pagination
        result = []

        splitted = query_string.split(" ")
        first_name = splitted[0]
        last_name = splitted[0]
        if len(splitted) > 1:
            last_name = splitted[1]

        best_matches = Profile.objects.filter(
            Q(user__username__startswith=query_string) |
            Q(first_name__startswith=first_name) | 
            Q(last_name__startswith=last_name)
        ).annotate(weight=Value(0, IntegerField())) \
            .values("user__username", "first_name", "last_name", "image", "bio")

        # todo: able to search for possible users that contain query string.
        # best_matches_ids = best_matches.values_list("id", flat=True)

        # users = Profile.objects.filter(
        #     Q(user__username__icontains=query_string) |
        #     Q(first_name__icontains=first_name) | 
        #     Q(last_name__icontains=last_name)
        #     ) \
        #         .annotate(weight=Value(1, IntegerField()))

        # bug: lost user__username after union. Unknown reason.
        # all_users = best_matches.union(users).order_by("weight")

        # todo: make url to go to user profile.
        for user in best_matches:
            result.append({
                "text": user["user__username"] + " - " + user["first_name"] + " " + user["last_name"],
                "image": user["image"],
                "first_name": user["first_name"],
                "last_name": user["last_name"],
                "bio": user["bio"],
                "username": user['user__username'],
                "category": "user",
                "url": "",
            })

        return result

    def search_skills(query_string):
        # todo: add limit to query result, aka pagination

        result = []

        best_matches = Skill.objects.filter(name__startswith=query_string) \
            .exclude(name="User")

        best_matches_ids = best_matches.values_list("id", flat=True)

        skills = Skill.objects.filter(name__icontains=query_string) \
            .exclude(name="User") \
                .exclude(id__in=best_matches_ids)[:10]

        '''
            Union is not possible when trying to limit queryset.
            Gives error: 'OFFSET/LIMIT operation cannot be done in subqueries'
        '''
        # all_skills = best_matches.union(skills).order_by('weight', 'name').values()

        best_skills = best_matches.values()
        potential_skills = skills.values()

        # todo: add url to show all experiences related to such skill.
        for skill in best_skills:
            result.append({
                "text": skill["name"],
                "image": skill["icon_HREF"],
                "category": "skill" if skill["node_type"] != "C" else "skill category",
                "url": "/experience-list-skill?name=" + skill["id"],
            })

        for skill in potential_skills:
            result.append({
                "text": skill["name"],
                "image": skill["icon_HREF"],
                "category": "skill" if skill["node_type"] != "C" else "skill category",
                "url": "",
            })

        return result
    
    def search_experiences(query_string):
        # todo: add limit to query result, aka pagination
        result = []

        best_matches = Experience.objects.filter(name__startswith=query_string)
        #     .annotate(weight=Value(0, IntegerField()))
        best_matches_ids = best_matches.values_list("id", flat=True)
        experiences = Experience.objects.filter(name__icontains=query_string) \
            .exclude(id__in=best_matches_ids)[:10]

        # print(best_matches.all().values("profile__user__username"))
        # print(experiences.all().values("profile__user__username"))

        # all_experiences = best_matches.union(experiences, all=True).order_by("weight", "name").values("name", "image", "description", "project_link")

        best_experiences = best_matches.values(
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

        potential_matches = experiences.values(
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

        # print(best_experiences)

        for exp in best_experiences:
            # search for skills related to experience
            skills = DesiredSkill.objects.filter(experience__id=exp['id']).annotate(skill_name=F("skill__name"), skill_image=F("skill__icon_HREF")).values("skill_name", "skill_image")

            result.append({
                "id": exp["id"],
                "text": exp["name"],
                "image": exp["image"],
                "description": exp['description'],
                'profile': {
                    'username': exp['profile__user__username'],
                    'image': exp['profile__image']
                },
                'skills': list(skills),
                'kind': best_matches.filter(id=exp['id']).first().get_kind_display(),
                "url": exp["project_link"],
                "likes": exp["likes_amount"],
                "start_date": exp["start_date"].strftime("%d %B, %Y") if exp['start_date'] is not None else None,
                "end_date": exp["end_date"].strftime("%d %B, %Y") if exp['end_date'] is not None else None,
                "category": "experience",
            })

        # append the potential searches
        for exp in potential_matches:
                        # search for skills related to experience
            skills = DesiredSkill.objects.filter(experience__id=exp['id']).annotate(skill_name=F("skill__name"), skill_image=F("skill__icon_HREF")).values("skill_name", "skill_image")

            kind = best_matches.filter(id=exp['id']).first()

            if kind is not None:
                kind = kind.get_kind_display()

            result.append({
                "id": exp["id"],
                "text": exp["name"],
                "image": exp["image"],
                "description": exp['description'],
                'profile': {
                    'username': exp['profile__user__username'],
                    'image': exp['profile__image']
                },
                'skills': list(skills),
                'kind': kind,
                "url": exp["project_link"],
                "likes": exp["likes_amount"],
                "start_date": exp["start_date"].strftime("%d %B, %Y") if exp['start_date'] is not None else None,
                "end_date": exp["end_date"].strftime("%d %B, %Y") if exp['end_date'] is not None else None,
                "category": "experience",
            })

        return result
