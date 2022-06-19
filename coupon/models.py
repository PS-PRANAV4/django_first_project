from django.db import models

# Create your models here.
from django.db import models
from admins.models import Accounts as CustomUSer
import random
# Create your models here.


class Coupon(models.Model):
    number = models.CharField(max_length=15, blank=True)
    coupon_amount = models.IntegerField()


    def __str__(self):
        return str(self.number)
    
   
