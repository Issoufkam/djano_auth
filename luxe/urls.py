from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.loginF, name="login"),
    path('register/', views.registerF, name="register"),
    path('logout/', views.logOut, name="logout"),
    
]