from django import views
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.first ),
    path('signin',views.signin ),
    path('signup',views.signup ),
    path('signout',views.signout ),
    path('profile',views.profile ),
    path('cart',views.cart ),
    path('product/<int:id>',views.product_details ),
    # path('verify/', views.verify_view),
    path('check',views.check_out ),
    
    
]
