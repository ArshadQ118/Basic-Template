from django.urls import path
from . import views
from django.contrib import admin
from django.contrib.auth import login, logout
from .views import activation_sent, activate
from django.http import HttpResponseRedirect
from django.views.generic import View
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy


app_name = 'myapp'

urlpatterns = [
    path('', views.HomeView, name='home'),
    
    path('contact/', views.contact, name='contact'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registration, name='register'),
    path('sent/', activation_sent, name="activation_sent"),
    path('profile/',views.profile,name='profile'),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),
    path('password-change/', views.password_change, name='password_change'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='password_reset_form.html',email_template_name = 'password_reset_email.html',     
                                                                success_url = reverse_lazy('myapp:password_reset_done')),name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('password_reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html',success_url = reverse_lazy('myapp:password_reset_complete')), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
] 
