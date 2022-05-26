import os

def export_env(request):
  data = {
    'DJANGO_ENV': os.environ.get('DJANGO_ENV')
  }

  return data