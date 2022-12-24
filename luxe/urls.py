from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('<int:myid>', views.detail, name="detail"),
    path('login/', views.loginF, name="login"),
    path('register/', views.registerF, name="register"),
    path('logout/', views.logOut, name="logout"),
    path('product/', views.panier, name="panier"),
   # path('message_sms/', views.sms, name="sms" )
    
]