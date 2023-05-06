from django.contrib import admin

# Register your models here. 5257,5257@5257.5257, 5257
from django.contrib import admin
from .models import Teacher, Student, Administrator

admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Administrator)
