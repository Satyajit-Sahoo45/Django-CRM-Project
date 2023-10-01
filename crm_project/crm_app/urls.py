from django.urls import path
from .views import home, logout_user, Register_user, customer_record, delete_record, add_record

urlpatterns = [
    path('', home, name="home"),
    path('logout/', logout_user, name="logout"),
    path('register/', Register_user, name="register"),
    path('record/<int:id>', customer_record, name="record"),
    path('delete_record/<int:id>', delete_record, name="delete"),
    path('add_record/', add_record, name="add"),
]