from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.db.models import Sum


class UserActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=255)
    timestamp = models.DateTimeField(default=timezone.now)


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
    address = models.CharField(max_length=255, default='Unknown Address')  # Add a default value here
    card_number = models.CharField(max_length=100, unique=True)
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

    def calculate_total_price(self, start_date, end_date):
        total_price = 0

        subscriptions = Subscription.objects.filter(coach=self, date__range=[start_date, end_date])

        for subscription in subscriptions:
            total_price += subscription.price

        return total_price


class Subscription(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE)
    lessons_count = models.IntegerField()
    attendance = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Добавляем поле для стоимости абонемента
    comment = models.TextField(blank=True, null=True)
    button_highlighted = models.BooleanField(default=False)
    date = models.DateTimeField(default=timezone.now)  # Добавляем поле для даты создания

    def __str__(self):
        return f'Subscription {self.id}'

class MarkedAttendance(models.Model):
    user = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name='marked_attendance')  # Связь с пользователем, которого отметили
    timestamp = models.DateTimeField(auto_now_add=True)  # Время отметки
    group = models.CharField(max_length=100)  # Группа, к которой относится пользователь

    def __str__(self):
        return f'{self.user} - {self.group} - {self.timestamp}'