
from django import views
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [

path('<int:id>', views.user_profile),
path('address/<int:id>',views.user_address),
path('add_address/<int:id>',views.add_address),
path('orders/<int:id>',views.orders),
path('cancel/<int:id>',views.cancel),
path('account/<int:id>',views.account),
path('change_user', views.pic),

    
    
]






