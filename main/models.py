from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.validators import RegexValidator
from ckeditor.fields import RichTextField
from datetime import datetime
from PIL import Image as Img, ImageOps
from decimal import Decimal
import io

# Profile is one-to-one with django user table, and can hold extra fields of User table
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school_id = models.CharField(max_length=20, default="0000")
    avatar = models.ImageField(upload_to='user/avatar', default="..\static\assets\img\profile\default-profile-photo.jpg")
    bio = models.TextField(max_length= 500, blank = True, default="")
    career_position = models.CharField(max_length=50, null=True, blank= True, default="Student")
    state = models.CharField(max_length=20, blank= True, null=True)
    country = models.CharField(max_length=20, blank= True, null=True)
    linkedin_url = models.CharField(max_length=255, blank= True, null=True)
    instagram_url = models.CharField(max_length=255, blank= True, null=True)
    twitter_url = models.CharField(max_length=255, blank= True, null=True)
    last_updated = models.DateTimeField(User, auto_now=True)
    def __str__(self):
        return self.user.email
# Auto create a profile when a user is created
def create_profile(sender,instance, created, **kwargs):
    if created:
        user_profile = Profile(user= instance)
        user_profile.save()

post_save.connect(create_profile, sender= User)    

# Image Model
class Image(models.Model):
    caption = models.CharField(max_length=20)
    photo   = models.ImageField(upload_to='user/images')
    def __str__(self):
        return (f'{self.caption}', f'{self.photo}')
# Posts Model
class Post(models.Model):
    user = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
    # Types of posts
    choices=(
                ('posts', 'Posts'),
                ('events', 'Events'),
                ('news', 'News'),
            )
    category = models.CharField(max_length=10, choices=choices, default='posts')
    body = RichTextField(blank=True, null=True)
    synopsis = models.CharField(max_length=100, default="Place holder")
    created_at = models.DateTimeField(auto_now_add=True)
    publish_date = models.DateTimeField(default=datetime.now)
    def __str__(self):
        return (f"{self.user}"
                f"({self.created_at})"
                f"{self.synopsis}")

# Feedbacks/Comment model
class Feedback(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment= models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name="feedbacks", on_delete=models.CASCADE)

# Product Model 
class Product(models.Model):
    # product_id = models.AutoField
    product_name = models.CharField(max_length=100) 
    product_isDigital = models.BooleanField(default=False, null= True, blank=False)
    product_category = models.CharField(max_length=100, default="") 
    product_subcategory = models.CharField(max_length=50, default="") 
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_desc = models.CharField(max_length=300)
    product_image = models.ImageField(upload_to='shop/images', default="")
    def save(self, *args, **kwargs):
        if self.product_image:
            # Open the image using Pillow
            image = Img.open(self.product_image)

            # Overwrite the original image file with the resized image
            output = io.BytesIO()
            max_size = (1200,800)
            resized_image = ImageOps.fit(image, max_size, Img.ANTIALIAS)
            resized_image.save(output, format='JPEG', quality=75)
            output.seek(0)
            self.product_image = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.product_image.name.split('.')[0], 'image/jpeg', output.getbuffer().nbytes, None)

        super(Product, self).save(*args, **kwargs)
    def __str__(self):
        return self.product_name

# Poll Model
class Poll(models.Model):
    question     = models.CharField(max_length=200)
    publish_date = models.DateField(default=datetime.now) 
    
    def __str__(self):
        return self.question

# Poll choices Model
class Poll_choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice = models.CharField(max_length=200)
    vote = models.IntegerField(default=0)
    
    def __str__(self):
        return self.choice
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(default=datetime.now())
    updated_at = models.DateTimeField(default=datetime.now)
    isPaid = models.BooleanField(default=False)
    def __str__(self):
        return str(self.total)
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=1)
    def __str__(self):
        return str(self.product.product_name)
# Billing address
class BillingAddress(models.Model):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank= True)
    email = models.EmailField(blank=True, null=True)
    company_name = models.CharField(max_length=100, blank=True, null= True)
    address = models.CharField(max_length=100)
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.first_name:
            self.first_name = self.user.first_name
        if not self.last_name:
            self.last_name = self.user.last_name
        if not self.email:
            self.email = self.user.email
        super().save(*args, **kwargs)
# Order table
class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=200, null = True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    shipping_address = models.ForeignKey(BillingAddress, blank=True, null=True, on_delete=models.SET_NULL)
    shipping_charge = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    @property
    def get_total(self):
        orderItems = self.orderitem_set.all()
        total = sum([ item.get_total for item in orderItems])
        return total 
    @property
    def get_total_shipping(self):
        total = self.get_total + self.shipping_charge
        return total
    
    @property
    def get_count(self):
        orderItems = self.orderitem_set.all()
        count = sum([ item.quantity for item in orderItems])
        return count
    @property
    def shipping(self):
        shipping = False
        orderItems = self.orderitem_set.all()
        for item in orderItems:
            if not item.product.product_isDigital:
                shipping = True
        return shipping 
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orderitem_set')
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def get_total(self):
        total = self.product.product_price * Decimal(self.quantity)    
        return total
class File(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    is_public = models.BooleanField(default=False)