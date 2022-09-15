from django.urls import path
from . import views
from django.conf import settings

urlpatterns = [

    path('login/',views.loginPage,name="login"),
    path('logout/',views.logoutUser,name="logout"),
    path('register/',views.registerPage,name="register"),
    path('results/<str:pk>/',views.resultEvent,name="results-event"),
    path('', views.home, name="home"),
    path('update-user/',views.updateUser,name="update-user"),
    path('update-athlete/<str:pk>',views.updateAthlete,name="update-athlete"),
    path('athlete-search/',views.searchAthlete,name="athlete-search"),
    path('view-athlete/<str:pk>',views.viewAthlete,name="view-athlete"),
    path('create-athlete/',views.createAthlete,name="create-athlete"),
    path('update-performance/<str:pk>',views.updatePerformance,name="update-performance"),
    path('create-performance/<str:eventid>/<str:male>',views.createPerformance,name="create-performance"),
    path('test/',views.testpage,name="test-page"),
    path('recentactivity/',views.recentActivityPage,name="recent-activity"),
]




