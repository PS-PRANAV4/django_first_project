
from email.mime import image
from operator import mod
from pickle import TRUE
from tkinter import CASCADE
from unicodedata import name
from django.db import models

# Create your models here.
maincategory = (('MEN','MEN'),('WOMEN','WOMEN'),('KIDS','KIDS'))
class MainCategory(models.Model):
    name = models.CharField(choices=maincategory,default='MEN',max_length=20)
    main_category_image = models.ImageField(upload_to = 'photos/maincategory',blank = True)
    
    def __str__(self):
        return self.name
    
class Category(models.Model):
    namer = models.CharField(max_length=50)
    image = models.ImageField(upload_to = 'photos/category',blank = True)
    description = models.TextField()
    main_cate = models.ForeignKey(MainCategory,blank=True,null=True, on_delete=models.CASCADE)

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
    image_product4 = models.ImageField(upload_to = 'photos/products2', blank = True)
    image_product5 = models.ImageField(upload_to = 'photos/products3', blank = True)

    def __str__(self):
        return self.name
