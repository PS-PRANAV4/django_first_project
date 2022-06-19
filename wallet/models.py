from django.db import models
from admins.models import Accounts

# Create your models here.
class Wallet(models.Model):
    user = models.OneToOneField(Accounts, on_delete=models.CASCADE, blank=True)
    amount = models.IntegerField(default=0, )

    def __str__(self):
        return self.user.username