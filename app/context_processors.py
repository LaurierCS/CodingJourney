import os

def export_env(request):
  data = {
    'DJANGO_ENV': os.environ.get('DJANGO_ENV')
  }

  return data

# ! UNRELIABLE WAY TO VERIFY OWNERSHIP OF DATA !
def verify_ownership(request):
  data = { }

  if not request.user.is_anonymous:
    requesting_username = None
    if request.GET:
      requesting_username = request.GET.get("username")
    elif request.POST:
      requesting_username = request.POST.get("username")

    is_owner = requesting_username is not None and request.user.username == requesting_username
    data['owned'] = is_owner
  else:
    data['owned'] = False

  return data