
from email.mime import image
from operator import mod
from pickle import TRUE
from tkinter import CASCADE
from unicodedata import name
from django.db import models

# Create your models here.


class Category(models.Model):
    namer = models.CharField(max_length=50)
    image = models.ImageField()
    description = models.TextField()


    def __str__(self):
        return self.namer


class Products(models.Model):
    name = models.CharField(max_length=100)
    details = models.TextField()
    price = models.IntegerField()
    offer = models.IntegerField()
    stock = models.IntegerField()
    category_id = models.ForeignKey(Category, on_delete=models.PROTECT)
    image_product = models.ImageField(upload_to = 'photos/products', blank = True)

    def __str__(self):
        return self.name
