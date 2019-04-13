"""hose URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

from hose import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
    # path('legal/', TemplateView.as_view(template_name='legals.html'), name='legal'),
    path('legals/', views.legals, name='legals'),
    path('admin/', admin.site.urls),

    path('user/', include('hose_usage.urls')),

    path('api-auth', include('rest_framework.urls')),
    url(r'^auth/api-token-auth/', obtain_jwt_token),
    url(r'^auth/api-token-refresh/', refresh_jwt_token),
    url(r'^auth/api-token-verify/', verify_jwt_token),
]
