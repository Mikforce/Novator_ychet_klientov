from django.contrib import admin

# Register your models here. admin,5257@5257.5257, 5257
from django.contrib import admin
from .models import Group, Coach, Administrator, Subscription, Client
from django.contrib import admin
from .models import Profile


admin.site.register(Profile)
admin.site.register(Coach)
admin.site.register(Client)
admin.site.register(Administrator)
admin.site.register(Subscription)
admin.site.register(Group)