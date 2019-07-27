"""robocup URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('league/', views.chairProfile, name="chairProfile"),
    path('status/qualify/<int:id>/', views.quali, name='quali'),
    path('status/disqualify/<int:id>/', views.disquali, name='disquali'),
    path('teams/<int:id>/', views.team_detail, name='team_detail'),
    path('teams/create/', views.TeamCreate.as_view(), name='team_create'),
    path('teams/update/<int:pk>/', views.TeamUpdate.as_view(), name='team_update'),
    path('teams/delete/<int:pk>/', views.TeamDelete.as_view(), name='team_delete'),
    path('teams/members/<int:id>/', views.manage_team, name='manage_team'),
    # path('teams/membercreate/<int:id>/', views.MemberCreate.as_view(), name='membercreate'),
    path('myteams/', views.userteamView, name='my-teams'),
    path('finish/<int:id>/', views.finish, name='finish'),
    path('pdf/', views.pdf , name='pdf'),
]
