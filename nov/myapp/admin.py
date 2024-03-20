from django.contrib import admin

# Register your models here. admin,5257@5257.5257, 5257
from django.contrib import admin
from .models import Group, Coach, Subscription, Client, Profile
from django.contrib import admin



admin.site.register(Profile)
admin.site.register(Coach)
admin.site.register(Client)
admin.site.register(Subscription)
admin.site.register(Group)