from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_handler(request):

    if not request.user.is_authenticated:
        return redirect("auth_page")

    # remove the session id and get user back to the login page
    logout(request)
    return redirect('login')