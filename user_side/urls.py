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
    path('addcart/<int:id>/<int:us>',views.addcart ),
    path('product/<int:id>',views.product_details ),
    path('cart/<int:us>',views.cart),
    path('verify/', views.verify_view),
    path('check/<int:id>',views.check_out ),
    path('delete/<int:id>/<int:us>',views.delete_cart ),
    path('checkout/<int:check>/<int:id>',views.checkout ),
    path('purchase/<int:check>/<int:id>',views.purchase),
    path('quantity/<int:us>/<str:op>/<int:pro>',views.add_quantity),
    path('hello',views.hello),
    path('hel',views.hel),
    path('invoice/<id>',views.invoice),
    path('paypaypal',views.paypal),
    path('filter',views.filter),
    path('invoice/pdf/<int:id>',views.invoice_pdf),
    path('buynow/<int:id>',views.buy_now),
    path('check',views.check_out ),
    path('add_coupon',views.add_coupon ),
    
    
]
