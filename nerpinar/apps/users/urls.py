from django.urls import path
from . import views

app_name = 'users' # Пространство имен для приложения

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('verify-email/', views.verify_email_view, name='verify_email'),
    path('resend-code/', views.resend_verification_code_view, name='resend_verification_code'),

]
