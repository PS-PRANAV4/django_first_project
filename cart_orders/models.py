
from datetime import datetime
from email.policy import default
from django.db import models
from product.models import Products
from admins.models import Accounts
from profiles.models import Profile
import uuid
# Create your models here.

tran_type = (("PAYPAL","PAYPAL"),("RAZORPAY","RAZORPAY"),("COD","COD"))

delivery_choices = (("ACCEPTED", "ACCEPTED"), ("DELIVERED","DELIVERED"),("CANCELED","CANCELED"),("FAILED","FAILED"),("SHIPPED","SHIPPED"),("OUT FOR DEIVERY","OUT FOR DELIVERY"))

class Cart(models.Model):
    user = models.OneToOneField(Accounts, on_delete=models.CASCADE, blank=True, null=True)
    grand_total = models.IntegerField(blank=True, null=True)
    coupon_offer = models.IntegerField(default=0)
    def __str__(self):
        try:
            return self.user.username
        except:
            return f"GUEST USER"

class CartProduct(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, blank=True)
    quantity = models.IntegerField(blank=True)
    total_amount = models.IntegerField(blank=True)
    cart = models.ForeignKey(Cart, on_delete= models.CASCADE, blank=True,null=True)
    

    def __str__(self):
        try:
            a = ( self.cart.user.username, self.product.name)
            return '-'.join(a)
        except:
            return "GUEST USER"

    



class Order(models.Model):
    user = models.ForeignKey(Accounts, on_delete=models.SET_NULL, blank=True, null=True)
    delivery_address = models.ForeignKey(Profile, on_delete=models.CASCADE)
    status = models.CharField(choices= delivery_choices, default="ACCEPTED", max_length=20)
    grand_total = models.IntegerField(blank =True)
    order_date = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    delivery_date = models.DateTimeField(blank=True, null=True)
    order_id = models.UUIDField(editable=False,default=uuid.uuid4,blank=True,null=True)
    transaction_id = models.CharField(max_length=100,blank=True,null=True)
    transaction_type = models.CharField(choices=tran_type,null=True,blank=True, max_length=20)

    def __str__(self):
        return self.user.username

class ProductOrders(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, blank=True)
    quantity = models.IntegerField(blank=True)
    total_amount = models.IntegerField(blank=True)
    main_order = models.ForeignKey(Order, on_delete=models.CASCADE)
    
    def __str__(self):
        a = (self.product.name,'  product sold to->', self.main_order.user.username)
        return ' '.join(a)