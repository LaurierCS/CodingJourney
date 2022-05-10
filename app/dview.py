from django.shortcuts import render
from .views import TreeQueries
def d(r):
    tree_json = TreeQueries.getFullTree()
    return render(r, 'app/d.html', {"tree_json": tree_json})
