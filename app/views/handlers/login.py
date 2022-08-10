from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import redirect

def login_handler(request):
    if request.user.is_authenticated:
        return redirect('dashboard_page')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard_page')
        else:
            messages.info(request, 'Username or password is incorrect')
    return redirect("auth_page")