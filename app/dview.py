from django.shortcuts import render
from .views import TreeQueries
import json

def d(r):
    tree_json = TreeQueries.getFullTree()
    print(tree_json)
    return render(r, 'app/d.html', {'tree_json': tree_json})
