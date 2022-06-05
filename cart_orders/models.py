from tkinter import CASCADE
from django.db import models
from product.models import Products
from admins.models import Accounts
from profiles.models import Profile
# Create your models here.

delivery_choices = (("PENDING", "PENDING"), ("DELIVERED","DELIVERED"),("CANCELED","CANCELED"))

class Cart(models.Model):
    user = models.OneToOneField(Accounts, on_delete=models.CASCADE, blank=True)
    grand_total = models.IntegerField(blank=True, null=True)
    def __int__(self):
        return self.user
    

class CartProduct(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, blank=True)
    quantity = models.IntegerField(blank=True)
    total_amount = models.IntegerField(blank=True)
    cart = models.ForeignKey(Cart, on_delete= models.CASCADE, blank=True)

    
    



class Order(models.Model):
    user = models.ForeignKey(Accounts, on_delete=models.CASCADE, blank=True)
    delivery_address = models.ForeignKey(Profile, on_delete=models.CASCADE)
    status = models.CharField(choices= delivery_choices, default="PENDING", max_length=20)
    grand_total = models.IntegerField(blank =True)

class ProductOrders(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, blank=True)
    quantity = models.IntegerField(blank=True)
    total_amount = models.IntegerField(blank=True)
    main_order = models.ForeignKey(Order, on_delete=models.CASCADE)