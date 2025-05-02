from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('apps.users.urls')), # URL-адреса для авторизации
    path('', include('apps.main.urls')),   # URL-адреса главного приложения
]
