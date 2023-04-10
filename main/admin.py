from django.contrib import admin
from django.contrib.auth.models import Group, User
from main.models import Users, Profile, Products

# Unregister Group
admin.site.unregister(Group)
# Register your models here.
admin.site.register(Users)
admin.site.register(Profile)
admin.site.register(Products)