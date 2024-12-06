
import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models

from django.db import models

from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin,Group, Permission
from django.contrib.auth.models import AbstractUser

from rinku_cakery_admin.models import *
    
class UserProfile(AbstractUser, PermissionsMixin):
    username = models.CharField(max_length = 120,unique=True)
    email = models.EmailField(max_length = 120,unique=True)
    password = models.CharField(max_length = 120)
    phone = models.CharField(max_length = 10)
    otp = models.CharField(max_length=25,default='0000')
    groups = models.ManyToManyField(Group, related_name="user_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="user_permissions", blank=True)
    
class Cart_Data(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    product = models.ForeignKey('rinku_cakery_admin.Product',on_delete=models.CASCADE)
    product_qty = models.IntegerField(null=False,blank=False)
    selected_weight = models.CharField(max_length=100,default=None)  # store the selected weight
    selected_price = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=10000,default=None)  
    
    
class checkout_data(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    product = models.ForeignKey('rinku_cakery_admin.Product',on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart_Data, on_delete=models.CASCADE)
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    lname = models.CharField(max_length=50)
    quantity = models.IntegerField(null=False,default=1)
    price = models.FloatField(null=False,default=0)
    weight = models.CharField(max_length=150,null=False,default=0)
    phone = models.CharField(max_length=20)
    address = models.TextField(default=None)
    date = models.DateField(default=datetime.datetime.today)

class orders_item(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    product = models.ForeignKey('rinku_cakery_admin.Product',on_delete=models.CASCADE)
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    lname = models.CharField(max_length=50)
    quantity = models.IntegerField(null=False)
    price = models.FloatField(null=False)
    weight = models.CharField(max_length=150,null=False)
    total_price = models.CharField(max_length=150,null=False)
    phone = models.CharField(max_length=20)
    address = models.TextField(default=None)
    date = models.DateField(auto_now_add=True)
    delivered = models.BooleanField(default=False)
    message = models.TextField(max_length=255, blank=True, null=True)
        
