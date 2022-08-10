from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from app.forms import CreateUserForm

def registration_handler(request):
    if request.method == 'POST':
        register_form = CreateUserForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            username = register_form.cleaned_data.get('username')
            password = register_form.cleaned_data.get("password1")
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('dashboard_page')
        else:
            if "password2" in register_form.errors:
                for validationError in register_form.errors.as_data()['password2']:
                    messages.info(request, validationError.message)
            if "username" in register_form.errors:
                for validationError in register_form.errors.as_data()['username']:
                    messages.info(request, validationError.message)
    
    return redirect(reverse("auth_page") + "?form=register")