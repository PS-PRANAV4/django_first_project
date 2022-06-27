from django.db import models
from admins.models import Accounts

# Create your models here.



class Todo(models.Model):
    content = models.TextField()
    user = models.ForeignKey(Accounts,on_delete=models.CASCADE)