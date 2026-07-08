"""
URL configuration for netology_shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from backend.views import RegisterView
from backend.views import LoginView

urlpatterns = [
    path('admin/', admin.site.core_admin_site if hasattr(admin.site, 'core_admin_site') else admin.site.urls),
    path('api/v1/user/register/', RegisterView.as_view(), name='user-register'),
    path('api/v1/user/login/', LoginView.as_view(), name='user-login'),
]