"""bootcamp2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf import settings

from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from django.contrib.auth import views as auth_views

from .core import views as core_views
from .feeds import views as feeds_views
from .authentication import views as authentication_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', feeds_views.feeds, name='home'),
    path('login/', auth_views.login,
         {'template_name': 'feeds/cover.html'}, name='login'),
    path('logout', auth_views.logout, {'next_page': '/'}, name='logout'),
    path('siginup/', authentication_views.signup, name='signup'),

    path('settings/', include('bootcamp2.core.urls')),
    path('feeds/', include('bootcamp2.feeds.urls')),
    path('articles/', include('bootcamp2.articles.urls')),

    path('<username>/', core_views.profile, name='profile'),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
