from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.
class Users(models.Model):
    name = models.CharField(max_length= 50)
    email = models.EmailField()
    desc = models.TextField(max_length= 500)
    phonenumber= models.IntegerField()
# Profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length= 500, default="")
    full_name = models.CharField(max_length= 50, default="")
    phone_number = models.IntegerField( null=True, blank= True)
    last_updated = models.DateTimeField(User, auto_now=True)
    def __str__(self):
        return self.user.email
def create_profile(sender,instance, created, **kwargs):
    if created:
        user_profile = Profile(user= instance)
        user_profile.save()
post_save.connect(create_profile, sender= User)    
# Products 
class Products(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=100) 
    product_category = models.CharField(max_length=100, default="") 
    product_subcategory = models.CharField(max_length=50, default="") 
    product_price = models.IntegerField()
    product_desc = models.CharField(max_length=300)
    product_image = models.ImageField(upload_to='shop/images', default="")
    