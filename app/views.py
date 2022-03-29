from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import *
from .models import *


def homepage(request):
    x = "Hakuna Matata"
    context = {
        "x": x,
    }
    template_name = "index.html"

    return render(request, template_name, context)
