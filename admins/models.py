import email
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import uuid

# Create your models here.

class Manager(BaseUserManager):

    def create_user(self, first_name, last_name, username, email, phone_number, password=None, ):
        if not email:
            raise ValueError('user must have an email')
        
        if not username:
            raise ValueError('user must have an username')
        

        user = self.model(email = self.normalize_email(email), username = username, first_name = first_name, last_name = last_name,phone_number = phone_number)
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, first_name, last_name, email, username,phone_number, password):
        user = self.create_user(email = self.normalize_email(email), username = username, password = password, first_name = first_name, last_name = last_name,phone_number=phone_number)
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user













class Accounts(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100,unique=True)
    phone_number = models.CharField(max_length=50,blank=True, unique=True)
    profile_pic = models.ImageField(upload_to = 'photos/profile_pic', blank = True, max_length=300)



    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin =  models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)
    referal_code = models.UUIDField(default=uuid.uuid4)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name','phone_number']

    objects = Manager()

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, add_label):
        return True