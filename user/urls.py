"""
URL configuration for notic project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path,include
from user import views

urlpatterns = [
    path('layout', views.layout, name='layout'),

    #Register
    path('register', views.register, name='register'),
    path('check_username', views.check_username, name='check_username'),
    path('check_email', views.check_email, name='check_email'),
    path('check_contact', views.check_contact, name='check_contact'),
    path('store_register', views.store_register, name='store_register'),

    path('login', views.login, name='login'),
    path('login_check', views.login_check, name='login_check'),
    path('logout', views.logout, name='logout'),

    path('notice', views.notice, name='notice'),
    path('search_view', views.search_view, name='search_view'),
    path('gen_pdf', views.gen_pdf, name='gen_pdf'),

    path('contact', views.contact, name='contact'),
    path('insert_contact', views.insert_contact, name='insert_contact'),
]
