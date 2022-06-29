import django
from django.db import models
from requests import request
from admins.models import Accounts
from django.db.models.signals import post_save
from product.models import Products
from product.models import MainCategory

# Create your models here.

class Notification(models.Model):
    main_categ = models.ForeignKey(MainCategory, on_delete=models.CASCADE,null=True, blank=True)
    action = models.ForeignKey(Products, on_delete=models.CASCADE, null=True, blank=True)
    time = models.DateTimeField(auto_now_add=True,blank=True, null=True,editable=True)
    def __str__(self):
        return self.action.name


def create_notification(sender, instance, created, **kwargs):
    if created:

        
        print()
        
        Notification.objects.create(action=instance, main_categ = instance.category_id.main_cate)
        print('object created')

post_save.connect(create_notification, sender=Products)