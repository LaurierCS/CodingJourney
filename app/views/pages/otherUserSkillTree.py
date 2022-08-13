from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from app.views.queryAPI.treeQueries import TreeQueries
from app.models import Profile

def other_user_skill_tree_page(request):
    username = request.GET.get("username")
    profile = Profile.objects.get(user__username=username)
    ds = TreeQueries.getTrimmedTree(profile)
    context = {
        "tree_json": ds,
        "profile": profile,
        "editable": False
    }
    template = "app/other_user_skill_tree.html"

    return render(request, template, context)