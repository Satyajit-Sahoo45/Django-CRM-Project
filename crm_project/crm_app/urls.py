from django.urls import path
from .views import home, logout_user, Register_user

urlpatterns = [
    path('', home, name="home"),
    path('logout/', logout_user, name="logout"),
    path('register/', Register_user, name="register")
]