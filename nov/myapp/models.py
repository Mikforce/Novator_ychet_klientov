from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Client(models.Model):
    full_name = models.CharField(max_length=255)
    birth_date = models.DateField()
    phone_number = models.CharField(max_length=20)
    parent_name = models.CharField(max_length=255)
    group_obj = models.ForeignKey('Group', on_delete=models.CASCADE, null=True, blank=True)
    date_joined = models.DateField()

class Group(models.Model):
    name = models.CharField(max_length=255)
    coach = models.ForeignKey('Coach', on_delete=models.CASCADE)
    description = models.TextField()
    students = models.ManyToManyField(Client, related_name='group_students')

class Coach(models.Model):
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    students = models.ManyToManyField(Client, null=True, blank=True)
    groupqs = models.ManyToManyField(Group, related_name='coach_groupqs', null=True, blank=True)

class Administrator(models.Model):
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)

class Subscription(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE)
    lessons_count = models.IntegerField()
    attendance = models.BooleanField(default=False)
    comment = models.TextField(blank=True, null=True)
