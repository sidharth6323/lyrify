"""lyrify URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from lyrics.views import english,search,hindi,base,about,report, all_matches, angular, scorecard, commentary

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^eng/$',english),
    url(r'^$',search),
    url(r'^hin/(.+)/(.+)/(.+)/$',hindi),
    url(r'^base/$',base),
    url(r'^about/$',about),
    url(r'^report/$',report),
    url(r'^livescoreAPI/$',all_matches),
    url(r'^angular/$',angular),
    url(r'^scorecard/(\d+)/$',scorecard),
    url(r'^commentary/(\d+)/$',commentary),
    ]
