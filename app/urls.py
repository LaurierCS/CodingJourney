from django.urls import path
from . import views

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
    path('search', views.SearchQueries.searchHandle, name="search_page"),

    # ************************************************************
    # ENDPOINT URLS - FOR HANDLING DATA LIKE LOGIN AND REGISRATION
    # ************************************************************
    path('login', views.login_handler, name="login"),
    path('register', views.registration_handler, name="register"),
    path('logout', views.logout_handler, name="logout"),

    # ************************************************************
    # Testing URLS - FOR Testing existing Functions
    # ************************************************************
    path('populate-skills', views.TreeQueries.populateDatabase, name="pop-database"),
    path('test-trimmed-tree', views.TreeQueries.getTrimmedTree, name="get-trimmed-tree"),
    path('experience-input', views.experience_input_handler, name="exp-input-test")
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


from . import dview
urlpatterns.append(path("d/",dview.d,name='d'))
urlpatterns.append(path("test/",dview.node_side_bar,name='node_side_bar'))

