from django import views
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.main),
    path('signin',views.signin),
    path('add_product',views.add_product),
    path('edit_product/<int:id>',views.edit_product),
    path('product',views.product),
    path('accounts',views.account),
    # path('accounts/(?P<burn>\w+?)/$',views.account),
    # path('add_users',views.add_users),
    path('block/<int:id>',views.block),
    path('logout',views.signout),
    path('delete/<int:id>',views.delete_product),
    path('add_category', views.add_category),
    path('delete_category/<int:id>', views.delete_category),
    path('change_order_status/<int:id>',views.change),
    path('change_order_status/<int:id>/<str:status>',views.change),
    path('accounts',views.account),
    
    
]
