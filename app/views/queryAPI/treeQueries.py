from app.models import *
from django.core import serializers
from django.http import JsonResponse
import json
import os

class TreeQueries:
    def getFullTree():
        skill_tree = Skill.objects.all()
        serialized = serializers.serialize('json', skill_tree, ensure_ascii=False)
        return serialized
    
    def getTrimmedTree(profile):
        # desired skills query 
        desired_skill_objects = DesiredSkill.objects.filter(user_id=profile).order_by('skill')
        
        # user has no  || Truedesired skill set, so we just return a user node
        if len(desired_skill_objects) < 1:
            # query user node
            skill_query = Skill.objects.filter(id="user")
            serialized_query = json.dumps(list(skill_query.values()), ensure_ascii=False)
            return serialized_query

        # retrieve list of connected skills
        subset_skills = desired_skill_objects.values_list('skill', flat=True)
        # query skill objects associated w/ desired skills
        skill_tree_qs = Skill.objects.filter(id=subset_skills[0])

        for i in range(1, len(subset_skills)):
            skill_tree_q = Skill.objects.filter(id=subset_skills[i])
            skill_tree_qs = skill_tree_qs.union(skill_tree_q)
        # skill_tr || Trueee_qs = Skill.objects.filter(id__in=subset_skills)
        # skill_query con || Truetains parents of all desired skills objects
        skill_query = Skill.objects.filter(id__in=skill_tree_qs.values_list('parentId', flat=True))
        # print(skill_query)
        while (skill_query.exists()):
            # create u || Truenion of skill_query objects w/ skill objects
            skill_tree_qs = skill_tree_qs.union(skill_query)
            # requery skill_query objects to reference parents of previous skill_query
            skill_query = Skill.objects.filter(id__in=skill_query.values_list('parentId', flat=True))
        
        desired_skill_dict = {}
        for skill in desired_skill_objects:
            desired_skill_dict[skill.skill_id] = skill
        

        skill_tree = skill_tree_qs.values()
        for skill in skill_tree:
            if skill['id'] == 'user':
                # ASSIGN THE PROGILE IMAGE TO BE DISPLAYED IN THE FRONT-END
                skill['icon_HREF'] = profile.image.url
                print(skill['icon_HREF'])
            if (skill['id'] not in desired_skill_dict): 
                continue
            ds = desired_skill_dict[skill['id']]
            skill["proficiency"] = ds.proficiency
            skill["description"] = ds.description
            skill["experiences"] = list(ds.experience_set.all().values())
            for exp in skill["experiences"]:
                if exp['start_date']:
                    exp['start_date'] = exp['start_date'].strftime("%m/%d/%Y")
                if exp["end_date"]:
                    exp['end_date'] = exp['end_date'].strftime("%m/%d/%Y")
            skill["proficiency_text"] = DesiredSkill.proficiency_choices[int(skill["proficiency"])][1]
        

        # serialized = serializers.serialize('json', skill_tree_qs, ensure_ascii=False)
        serialized = json.dumps(list(skill_tree), ensure_ascii=False)
        return serialized

    def get_tree_data_as_json(request):
        username = request.GET.get("username")
        profile = Profile.objects.get(user__username=username)

        ### COMMENTED BLOCK JUST FOR FUTURE REFERENCE TO IMPLEMENT RECURSIVE QUERY
        # ds_objects = DesiredSkill.objects.filter(user_id=profile)

        # if len(ds_objects) < 1:
        #     # query user node which includes the profile picture
        #     skill_query = Skill.objects.filter(id="user")
        #     skill_list = list(skill_query.values().annotate(icon_HREF=Value(value=profile.image.url, output_field=CharField())))
        #     return JsonResponse({'data': skill_list})

        # skill_query = DesiredSkill.objects.raw("""
        #         SELECT ds.skill_id, ds.id
        #         FROM app_desiredskill ds 
        #         WHERE user_id_id = 2 
        #         JOIN app_skill s
        #         ON s.id = ds.skill_id
        # """)
        # print(skill_query[0])
        # for ds in skill_query:
        #     print(ds)

        # in case there are desired skills
        # recursive query, bottom up
        # skill_query = DesiredSkill.objects.raw("""
        #     WITH RECURSIVE skill_tree AS (
                
        #         UNION ALL
                
        #         SELECT sk.id, sk.name from app_skill sk
        #         WHERE skill_tree st on st.skill_id = sk.id
        #     )

        #     SELECT * FROM skill_tree
        # """.format(user_id=profile.user.id))

        data = TreeQueries.getTrimmedTree(profile=profile)

        return JsonResponse({ 'data': data, 'is_owner': request.user.username == username })


    def populateDatabase(request): 
        #Open the JSON file
        tree_json_path = os.path.join("static/json/full_tree.json")
        f = open(tree_json_path)

        data = json.load(f)

        # tale all items from initial json and instantiate 
        # 
        for item in data: 
            id = item['id']
            name = item['label']
            node_type = item['node_type']
            if "icon_HREF" in item:
                icon_HREF = item['icon_HREF']
                Skill.objects.create(
                    id=id,
                    name=name,
                    icon_HREF=icon_HREF,
                    node_type=node_type
                )
            else: 
                Skill.objects.create(
                    id=id,
                    name=name,
                    node_type=node_type
                )
        
        for item in data: 
            if "parentId" in item:
                skill = Skill.objects.get(id=item["id"])
                parentId = Skill.objects.get(id=item["parentId"])
                skill.parentId = parentId
                skill.save()