from django.urls import path
from . import views

urlpatterns = [
    path('', views.langing_page, name="landing_page"),
    path('how-it-works/', views.how_it_works, name="how_it_works"),
    path('about-us/', views.about_us, name="about_us"),
    path('home/', views.homepage, name='homepage'),
    path('login/', views.login_page, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('register/', views.register, name="register"),
    path('experienceInput/', views.experienceInput, name="experience_input"),
    path('projectList/', views.projectList, name="project_list"),
]