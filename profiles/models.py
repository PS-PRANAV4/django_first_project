from pyexpat import model
from django.db import models
from admins.models import Accounts
# Create your models here.


class Profile(models.Model):
    first_name = models.CharField(max_length=20, blank=False)
    last_name = models.CharField(max_length=20, blank=False)
    country_name = models.CharField(max_length=30, blank=False)
    address = models.CharField(max_length=100, blank=False)
    town_city = models.CharField(max_length=50, blank=False)
    state = models.CharField(max_length=30, blank=False)
    post_code = models.CharField(max_length=30, blank=False)
    phone_number = models.CharField(blank=False, max_length=15)
    email = models.EmailField(max_length=50, blank=False)
    notes = models.TextField()
    accounts = models.ForeignKey(Accounts,on_delete=models.CASCADE)


    def __str__(self):
        a= (self.first_name, self.last_name, self.country_name, self.address, self.town_city, self.state, self.phone_number, self.email,'address of ->', self.accounts.first_name)
        return ' '.join(a)