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
from myadmin import views

urlpatterns = [
    path('layout', views.layout, name='layout'),
    path('dashboard', views.dashboard, name='dashboard'),

    path('login', views.login, name='login'),
    path('login_check', views.login_check, name='login_check'),
    path('logout', views.logout, name='logout'),

    #State
    path('add_state', views.add_state, name='add_state'),
    path('all_state', views.all_state, name='all_state'),
    path('insert_state', views.insert_state, name='insert_state'),
    path('del_state/<int:id>', views.del_state, name='del_state'),
    path('edit_state/<int:id>', views.edit_state, name='edit_state'),
    path('update_state/<int:id>', views.update_state, name='update_state'),

    #City
    path('add_city', views.add_city, name='add_city'),
    path('all_city', views.all_city, name='all_city'),
    path('insert_city', views.insert_city, name='insert_city'),
    path('del_city/<int:id>', views.del_city, name='del_city'),
    path('edit_city/<int:id>', views.edit_city, name='edit_city'),
    path('update_city/<int:id>', views.update_city, name='update_city'),

    #Area
    path('add_area', views.add_area, name='add_area'),
    path('insert_area', views.insert_area, name='insert_area'),
    path('all_area', views.all_area, name='all_area'),
    path('del_area/<int:id>', views.del_area, name='del_area'),
    path('edit_area/<int:id>', views.edit_area, name='edit_area'),
    path('update_area/<int:id>', views.update_area, name='update_area'),

    #User
    path('user', views.user, name='user'),
    path('view_user/<int:id>', views.view_user, name='view_user'),
    path('verify/<int:id>', views.verify, name='verify'),

    #Notic
    path('add_notice', views.add_notice, name='add_notice'),
    path('insert_notice', views.insert_notice, name='insert_notice'),
    path('all_notice', views.all_notice, name='all_notice'),
    path('del_notice/<int:id>', views.del_notice, name='del_notice'),
    path('edit_notice/<int:id>', views.edit_notice, name='edit_notice'),
    path('update_notice/<int:id>', views.update_notice, name='update_notice'),
    # path('read_pdf/<int:id>', views.read_pdf, name='read_pdf'),
    # path('view_pdf/<int:id>', views.view_pdf, name='view_pdf'),

    path('all_contact', views.all_contact, name='all_contact'),
    path('del_contact/<int:id>', views.del_contact, name='del_contact'),

]
