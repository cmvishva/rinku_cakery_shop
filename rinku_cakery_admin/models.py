from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
from django.db import models

from django.forms import ModelForm
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin,Group, Permission
from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.forms import PasswordChangeForm

class admindata(models.Model):
    adminusername = models.CharField(max_length=100)
    adminpassword = models.CharField(max_length=200)

        
class Main_menu(models.Model):
    menuname = models.CharField(max_length=100)
    menuurl = models.CharField(max_length=200)
    
    
class Sliders(models.Model):
    sname = models.CharField(max_length = 120,blank=True)
    sdesc = models.TextField(blank=True)
    simage = models.FileField(upload_to= 'media/')

class Sliderdata(ModelForm):
    class Meta:
        model = Sliders
        fields = ["sname" ,"sdesc" ,"simage"]

class Category(models.Model):
    categoryname = models.CharField(max_length=50)
    
class Product(models.Model):
    id = models.AutoField(primary_key=True,default=None)
    pimage = models.FileField(upload_to='media/')
    pname = models.CharField(max_length=100)
    pprice = models.IntegerField(max_length=10) 
    pdesc = models.TextField(blank=True)
    pstatus = models.CharField(max_length=500,blank=True)
    catfk = models.ForeignKey(Category,on_delete=models.CASCADE)
    pweight_500gm = models.BooleanField(default=False)
    pweight_1kg = models.BooleanField(default=False)
    pweight_1_5kg = models.BooleanField(default=False)
    pweight_2kg = models.BooleanField(default=False)
    pweight_2_5kg = models.BooleanField(default=False)
    pweight_3kg = models.BooleanField(default=False)
    pweight_3_5kg = models.BooleanField(default=False)
    pweight_4kg = models.BooleanField(default=False)
    pweight_4_5kg = models.BooleanField(default=False)
    pweight_5kg = models.BooleanField(default=False)


class product_data(ModelForm):
    class Meta:
        model = Product
        fields = ["pimage","pname" ,"pprice","catfk","pdesc","pstatus","pweight_500gm","pweight_1kg","pweight_1_5kg","pweight_2kg","pweight_3kg","pweight_3_5kg","pweight_4kg","pweight_4_5kg","pweight_5kg"]
        

        
           
# ================================================= About Page ================================================
class aboutheader(models.Model):
    
    about_header_text = models.TextField(blank=True)
    about_header_img = models.FileField(upload_to= 'media/')

class about_header_data(ModelForm):
    class Meta:
        model = aboutheader
        fields = ["about_header_text","about_header_img" ]
        
class Aboutsec1(models.Model):
    as1title = models.CharField(max_length = 200)
    as1image1 = models.FileField(upload_to= 'media/')
    as1image2 = models.FileField(upload_to= 'media/',default=None)
    as1desc = models.TextField(blank=True)

class About_sec1_data(ModelForm):
    class Meta:
        model = Aboutsec1
        fields = ["as1title" ,"as1image1","as1image2","as1desc"]         
            
class Aboutsec2(models.Model):
    as2title = models.CharField(max_length = 200)
    as2image1 = models.FileField(upload_to= 'media/',)
    as2image2 = models.FileField(upload_to= 'media/',default=None)
    as2desc = models.TextField(blank=True)

class About_sec2_data(ModelForm):
    class Meta:
        model = Aboutsec2
        fields = ["as2title" ,"as2image1","as2image2","as2desc" ]   
        
        
        
# ================================================= Contact Page ================================================              
        
class contactheader(models.Model):

    contact_header_title = models.CharField(max_length = 200,default='Contact Us',blank=True, null=True)
    contact_header_text = models.TextField(blank=True)
    contact_header_img = models.FileField(upload_to= 'media/')

class contact_header_data(ModelForm):
    class Meta:
        model = contactheader
        fields = ["contact_header_text","contact_header_img","contact_header_title"]
        
class contactmiddle(models.Model):
    contact_middle_img = models.FileField(upload_to= 'media/')

class contact_middle_data(ModelForm):
    class Meta:
        model = contactmiddle
        fields = ["contact_middle_img" ]
        
class contact_address(models.Model):
    address = models.CharField(max_length = 5000)
    email = models.EmailField(max_length = 100)
    mobile = models.CharField(max_length = 20)
    
class contact_address_data(ModelForm):
    class Meta:
        model = contact_address
        fields = ["address","email","mobile"] 
        
class contact_message(models.Model):
    cmname = models.CharField(max_length = 120)
    cmemail = models.CharField(max_length = 120)
    cmsubject = models.TextField(blank=True)
    cmmessage = models.TextField(blank=True)

class contact_message_data(ModelForm):
    class Meta:
        model = contact_message
        fields = ["cmname" ,"cmemail" ,"cmsubject","cmmessage"]  
# ================================================= Cart Page ================================================               
        
class cartheader(models.Model):
    cart_header_img = models.FileField(upload_to= 'media/')
    cart_header_imgname = models.TextField(blank=True)
    
class cart_header_data(ModelForm):
    class Meta:
        model = cartheader
        fields = ["cart_header_img","cart_header_imgname"]

  
# ================================================= Better Hygine Background ================================================               
        
class bh_background(models.Model):
    image = models.FileField(upload_to= 'media/')
    text = models.TextField(blank=True)

class bh_background_data(ModelForm):
    class Meta:
        model = bh_background
        fields = ["image","text"]
 
       
        
# ================================================= Footer ================================================               
        
class Footerimg(models.Model):
    
    fimage = models.FileField(upload_to= 'media/')

class FooterData(ModelForm):
    class Meta:
        model = Footerimg
        fields = ["fimage"]
 
 
 






