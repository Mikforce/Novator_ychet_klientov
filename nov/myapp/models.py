from django.db import models
from django.conf import settings
from django.utils import timezone


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
