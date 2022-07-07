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
    path('verify', views.verify_view),
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
    path('guest',views.guest ),
    path('addcart/<int:id>/None',views.guest ),
    path('guest_show/<int:cart_id>/<int:total_offer>',views.guest_show),
    path('minus',views.minus),
    path('add',views.add),
    path('delet',views.delet),
    path('product_cart_add',views.cart_product_add),
    path('shop',views.shop),
    path('shop/<int:id>',views.shop_filter),
    path('shop_cate/<int:id>',views.shop_filter_cate),
    path('shop/search',views.shop_search),
    path('otp',views.login_otp), 
    path('otp_verify',views.otp_veify),
    path('guest_check',views.guest_check),
    path('redirects_for_guest',views.buy_now_redirect),
    path('best_deals', views.best_deals),
    path('pay_using wallet/<int:check>',views.pay_wallet),   









    
    
    
]
