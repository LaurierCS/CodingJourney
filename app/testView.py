from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.views import View
from django.core import serializers
from django.db import connection
from django.contrib import messages
from django.db.models import Q, Case, F, Avg, When, Value, FloatField, IntegerField

# Django Auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm

import json
import os

from django.apps import apps
import tornado

# FILE IMPORTS
from .models import *
from .forms import *


def experience_display_view(request):
    context = {
    } 
    return render(request, 'app/experience_display.html', context=context)