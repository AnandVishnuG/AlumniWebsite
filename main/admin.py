from django.contrib import admin
from django.contrib.auth.models import Group, User
from main.models import Profile, Product, Cart, CartItem, Post, Image, Feedback, Poll, Poll_choice, Order, OrderItem, BillingAddress, Vote

# Unregister Group
# admin.site.unregister(Group)
# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Image)
# admin.site.unregister(Product)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Feedback)
admin.site.register(Poll)
admin.site.register(Poll_choice)
admin.site.register(Vote)

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(BillingAddress)

