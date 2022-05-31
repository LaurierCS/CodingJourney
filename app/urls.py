from django.urls import path
from . import views
# from . import testView

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.langing_page, name="landing_page"),
    path('auth', views.authpage, name="auth_page"),
    path('dashboard', views.dashboard, name='dashboard_page'),
    path('summary', views.allexperiences, name="summary_page"),
    path('profilepage', views.profilepage, name="profile_page"),
    path('settings', views.settingspage, name="settings_page"),
    path('profile', views.profilepage, name="profile_page"),
    path('profile/<str:username>', views.otherprofilepage, name='other_profile_page'),
    path('search', views.SearchQueries.searchHandle, name="search_page"),
    path('experiences-by-skill/<str:skill_name>', 
        views.TargetedQueries.getExperiencesBySkills, 
        name="experiences_by_skills"),    
    path('manage-desired-skills', views.manage_desired_skills_page, name="manage_desired_skills_page"),
    path('manage-experiences', views.manage_experiences_page, name="manage_experiences_page"),

    # ************************************************************
    # ENDPOINT URLS - FOR HANDLING DATA LIKE LOGIN AND REGISRATION
    # ************************************************************
    path('login', views.login_handler, name="login"),
    path('register', views.registration_handler, name="register"),
    path('logout', views.logout_handler, name="logout"),
    path('update-ds-description', views.update_desired_skill_description, name="update_ds_description"),
    path('experience-handler', views.experience_input_handler, name="experience-handler"),
    path('search', views.SearchQueries.searchHandle, name="search_page"),
    path('experience-view-handler', views.TargetedQueries.experienceGetter, name="Experience Query"),
    path('delete-ds', views.delete_desired_skill, name="delete_desired_skill"),
    path('delete-exp', views.delete_exp, name="delete_exp"),


    # ************************************************************
    # Testing URLS - FOR Testing existing Functions
    # ************************************************************
    path('populate-skills', views.TreeQueries.populateDatabase, name="pop-database"),
    path('test-trimmed-tree', views.TreeQueries.getTrimmedTree, name="get-trimmed-tree"),
    path('experience-input', views.experience_input_handler, name="exp-input-test"),
    path('experience-list', views.allexperiences, name='experience-list'),
    # path('experience-display-modal', testView.experience_display_view , name='experience-list'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

