from django import views
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('payment',views.index),
    path('payment/<int:id>/<int:check>',views.order_payment),
    path("razorpay/callback/", views.callback, name="callback"),
    path("course", views.course_changer, ),


    
    
]
