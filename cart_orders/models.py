from datetime import datetime
from email.policy import default
from django.db import models
from product.models import Products
from admins.models import Accounts
from profiles.models import Profile
# Create your models here.

delivery_choices = (("PENDING", "PENDING"), ("DELIVERED","DELIVERED"),("CANCELED","CANCELED"))

class Cart(models.Model):
    user = models.OneToOneField(Accounts, on_delete=models.CASCADE, blank=True)
    grand_total = models.IntegerField(blank=True, null=True)
    def __str__(self):
        return self.user.username
    

class CartProduct(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, blank=True)
    quantity = models.IntegerField(blank=True)
    total_amount = models.IntegerField(blank=True)
    cart = models.ForeignKey(Cart, on_delete= models.CASCADE, blank=True)
    

    def __str__(self):
        return self.cart.user.username
    
    



class Order(models.Model):
    user = models.ForeignKey(Accounts, on_delete=models.CASCADE, blank=True)
    delivery_address = models.ForeignKey(Profile, on_delete=models.CASCADE)
    status = models.CharField(choices= delivery_choices, default="PENDING", max_length=20)
    grand_total = models.IntegerField(blank =True)
    order_date = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    delivery_date = models.DateTimeField(blank=True, null=True)

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