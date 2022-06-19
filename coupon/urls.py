
from django import views
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [

path('coupon', views.coupon),
path('generate',views.generate),


    
    
]






