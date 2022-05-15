from django.shortcuts import render
from .views import TreeQueries

def d(r):
    tree_json = TreeQueries.getFullTree()
    return render(r, 'app/d.html', {"tree_json": tree_json})

def node_side_bar(r):
    template = "components/node_side_bar.html"
    context = {
        "icon_href": "/static/images/python_logo.png"
    }

    return render(r, template, context)