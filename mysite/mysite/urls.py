"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.urls import path
from django.contrib import admin
from django.views.generic import TemplateView
from rest_framework import routers
from teams import views

router = routers.DefaultRouter()
router.register(r'teams', views.TeamViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^teams/', include('teams.urls')),
    path('account/', include('account.urls')),
    #path('account/', include('rest_email_auth.urls')),
    path('account/', include('django.contrib.auth.urls')),
    url(r'^scraper/', include('scraper.urls')),
    url(r'^$', TemplateView.as_view(template_name='teams/home.html'), name='home'),
    path('about/', TemplateView.as_view(template_name='teams/about.html'), name='about'),
    path('401/', TemplateView.as_view(template_name='teams/401.html'), name='401'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
