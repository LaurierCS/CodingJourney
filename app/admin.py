from django.apps import apps
from django.contrib import admin
from .models import *

# Method 1: Register all models automatically
models = apps.get_models()
for model in models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass


# # Method 2: Register all models manually
# admin.site.register(Profile)
# admin.site.register(Experience)
# admin.site.register(Difficulty)
# admin.site.register(Marker)
