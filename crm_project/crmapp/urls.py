from django.urls import path
from .views import home, logout_user, Register_user, customer_record, delete_record, add_record, update_record, activate, Change_Password
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', home, name="home"),
    path('logout/', logout_user, name="logout"),
    path('register/', Register_user, name="register"),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',  activate, name='activate'),
    path('record/<int:id>', customer_record, name="record"),
    path('delete_record/<int:id>', delete_record, name="delete"),
    path('add_record/', add_record, name="add"),
    path('update_record/<int:id>', update_record, name="update"),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    path('ChangePassword/', Change_Password,name='ChangePassword'),
]