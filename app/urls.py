from django.urls import path

# pages imports
from app.views.pages.auth import *
from app.views.pages.landing import *
from app.views.pages.dashboard import *
from app.views.pages.experiencesList import *
from app.views.pages.landing import *
from app.views.pages.manageDesiredSkills import *
from app.views.pages.manageExperiences import *
from app.views.pages.otherUserProfile import *
from app.views.pages.otherUserSkillTree import *
from app.views.pages.profile import *
from app.views.pages.settings import *
# handlers imports
from app.views.handlers.desiredSkillDelete  import *
from app.views.handlers.desiredSkillInput  import *
from app.views.handlers.desiredSkillUpdate  import *
from app.views.handlers.experienceDelete  import *
from app.views.handlers.experienceInput  import *
from app.views.handlers.likeHandlers  import *
from app.views.handlers.login  import *
from app.views.handlers.logout  import *
from app.views.handlers.registration  import *
#queries imports 
from app.views.queryAPI.searchQueries import *
from app.views.queryAPI.targetedQueries import *
from app.views.queryAPI.treeQueries import *

from . import viewsFile

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', landing_page, name="landing_page"),
    path('auth', authpage, name="auth_page"),
    path('dashboard', dashboard, name='dashboard_page'),
    path('summary', allexperiences, name="summary_page"), #currently unreferenced
    path('profilepage', profilepage, name="profile_page"),
    path('settings', settingspage, name="settings_page"),
    path('profile', profilepage, name="profile_page"),
    path('profile/<str:username>', otherprofilepage, name='other_profile_page'),
    path('manage-desired-skills', manage_desired_skills_page, name="manage_desired_skills_page"),
    path('manage-experiences', manage_experiences_page, name="manage_experiences_page"),
    path('skill-tree', other_user_skill_tree_page, name="other_user_skill_tree_page"),
    
    path('search', viewsFile.SearchQueries.searchHandle, name="search_page"),
    path('experiences-by-skill/<str:skill_name>', 
        viewsFile.TargetedQueries.getExperiencesBySkills, 
        name="experiences_by_skills"),    
    

    # ************************************************************
    # ENDPOINT URLS - FOR HANDLING DATA LIKE LOGIN AND REGISRATION
    # ************************************************************
    path('login', login_handler, name="login"),
    path('register', registration_handler, name="register"),
    path('logout', logout_handler, name="logout"),
    path('update-ds-description', update_desired_skill, name="update_ds"),
    path('experience-handler', experience_input_handler, name="experience-handler"),
    path('search', SearchQueries.searchHandle, name="search_page"),
    path('experience-view-handler', viewsFile.TargetedQueries.experienceGetter, name="Experience Query"),
    path('desired-skill-input', viewsFile.desired_skill_input_handler, name="desired-skill-query"),
    path('delete-ds', viewsFile.delete_desired_skill, name="delete_desired_skill"),
    path('delete-exp', viewsFile.delete_exp, name="delete_exp"),
    path('exp-like', viewsFile.LikeHandlers.exp_like_handler, name="exp_like"),
    path('skill-tree-data', viewsFile.TreeQueries.get_tree_data_as_json, name="skill_tree_data"),
    path('user-profile-picture', viewsFile.TargetedQueries.getProfilePictureByUsername, name="user_profile_picture"),
    path('update-exp/<int:id>', viewsFile.experience_update_handler, name="update_exp"),
    path('experience-input', experience_input_handler, name="exp-input"),
    # path('update-ds', viewsFile.experience_update_handler, name="update_exp"),

    # ************************************************************
    # Testing URLS - FOR Testing existing Functions
    # ************************************************************
    path('populate-skills', viewsFile.TreeQueries.populateDatabase, name="pop-database"),
    path('test-trimmed-tree', viewsFile.TreeQueries.getTrimmedTree, name="get-trimmed-tree"),
    
    path('experience-list', viewsFile.allexperiences, name='experience-list'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

