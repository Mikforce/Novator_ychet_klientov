from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib.auth.models import User


class UserActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.activity_type} - {self.timestamp}'
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    active_time = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.user.username} Profile'

    def calculate_active_time_current_month(self):
        now = timezone.now()
        start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        end_of_month = start_of_month.replace(month=start_of_month.month % 12 + 1)

        user_activity_logs = UserActivityLog.objects.filter(user=self.user, timestamp__gte=start_of_month,
                                                            timestamp__lt=end_of_month)

        total_active_time = timedelta()
        for log in user_activity_logs:
            total_active_time += timedelta(seconds=log.duration)

        total_minutes = total_active_time.total_seconds() // 60
        self.active_time = total_minutes
        self.save()

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


class Subscription(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE)
    lessons_count = models.IntegerField()
    attendance = models.BooleanField(default=False)
    comment = models.TextField(blank=True, null=True)


class MarkedAttendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='marked_attendance')  # Связь с пользователем, которого отметили
    timestamp = models.DateTimeField(auto_now_add=True)  # Время отметки
    group = models.CharField(max_length=100)  # Группа, к которой относится пользователь

    def __str__(self):
        return f'{self.user.username} - {self.group} - {self.timestamp}'