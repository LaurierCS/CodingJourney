# Imports
from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Project)#Model to register in the Admin site)
admin.site.register(Difficulty)
admin.site.register(Marker)
