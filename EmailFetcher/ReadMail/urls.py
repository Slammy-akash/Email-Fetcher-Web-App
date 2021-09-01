
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name="ShopHome"),
    path('logout',views.handleLogout, name="logout")
]
