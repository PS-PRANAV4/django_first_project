import django
from django.db import models
from requests import request
from admins.models import Accounts
from django.db.models.signals import post_save
from product.models import Products

# Create your models here.

class Notification(models.Model):
    user = models.ForeignKey(Accounts, on_delete=models.CASCADE,null=True, blank=True)
    action = models.ForeignKey(Products, on_delete=models.CASCADE, null=True, blank=True)


def create_notification(sender, instance, created, **kwargs):
    if created:

        
        print()
        Notification.objects.create(action=instance)
        print('object created')

post_save.connect(create_notification, sender=Products)