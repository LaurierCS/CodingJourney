from django.urls import path
from . import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.langing_page, name="landing_page"),
    path('how-it-works/', views.how_it_works, name="how_it_works"),
    path('about-us/', views.about_us, name="about_us"),
    path('home/', views.homepage, name='homepage'),
    path('login/', views.login_page, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('register/', views.register, name="register"),
    path('project-input/', views.projectInput, name="project_input"),
    path('project-list/', views.projectList, name="project_list"),
    path('setting/',views.setting, name= "setting" ),
    path('profile/', views.profile, name= "profile"),
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
