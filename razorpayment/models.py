from django.db import models
from admins.models import Accounts



stat =  (("ACCEPTED", "ACCEPTED"), ("FAILED","FAILED"))
# Create your models here.
class Payment(models.Model):
    payment_id = models.CharField(max_length=100, blank=True)
    order_id = models.CharField(max_length=100)
    payment_signature = models.CharField(max_length=100, blank=True)
    user = models.ForeignKey(Accounts,on_delete=models.CASCADE)
    total_amount = models.IntegerField()
    status = models.CharField(choices= stat, max_length=50,blank=True)
