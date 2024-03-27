from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.db.models import Sum


class MyModel(models.Model):
    my_datetime_field = models.DateTimeField(default=timezone.now)
def default_datetime():
    return timezone.now()
class UserActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=255)
    timestamp = models.DateTimeField(default=default_datetime)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    active_time = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.user.username} Profile'

    @property
    def active_time_current_month(self):
        now = timezone.now()
        start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        end_of_month = start_of_month.replace(month=start_of_month.month % 12 + 1)

        user_activity_logs = UserActivityLog.objects.filter(user=self.user, timestamp__gte=start_of_month,
                                                            timestamp__lt=end_of_month)

        total_active_time = timedelta()
        for log in user_activity_logs:
            total_active_time += timedelta(seconds=log.duration)

        total_minutes = total_active_time.total_seconds() // 60
        return total_minutes


class Client(models.Model):
    full_name = models.CharField(max_length=255)
    birth_date = models.DateField()
    phone_number = models.CharField(max_length=20)
    parent_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, default='Unknown Address')  # Add a default value here
    card_number = models.CharField(max_length=100, unique=True)
    group_obj = models.ForeignKey('Group', on_delete=models.CASCADE, null=True, blank=True)
    date_joined = models.DateField()

    def __str__(self):
        return self.full_name

class Group(models.Model):
    name = models.CharField(max_length=255)
    coach = models.ForeignKey('Coach', on_delete=models.CASCADE, related_name='coach_groups')
    description = models.TextField()
    students = models.ManyToManyField(Client, related_name='group_students')
    def __str__(self):
        return f'{self.name} {self.coach}'

class Coach(models.Model):
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    students = models.ManyToManyField(Client, related_name='coach_students')
    groupqs = models.ManyToManyField(Group, related_name='coach_groupqs')
    percent = models.FloatField(default=0)
    def __str__(self):
        return self.full_name

class TrainingRoom(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class LessonSchedule(models.Model):
    name = models.ForeignKey(Group, on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=100)  # Например: 'Понедельник', 'Вторник'
    time = models.TimeField()
    num_lessons = models.PositiveIntegerField()
    training_room = models.ForeignKey(TrainingRoom, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} {self.day_of_week} {self.time} ({self.training_room})'


class Subscription(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE)
    lessons_count = models.IntegerField()
    attendance = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Добавляем поле для стоимости абонемента
    comment = models.TextField(blank=True, null=True)
    button_highlighted = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)  # Добавляем поле для даты создания
    end_date = models.DateTimeField()  # Добавляем поле для даты окончания абонемента
    lesson_schedule = models.ForeignKey(LessonSchedule, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.end_date:  # If end_date is not set
            self.end_date = self.date + timedelta(days=30) if self.date else timezone.now() + timedelta(days=30)
        super().save(*args, **kwargs)


    def __str__(self):
        return f'Subscription {self.id}'

class MarkedAttendance(models.Model):
    user = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name='marked_attendance')  # Связь с пользователем, которого отметили
    timestamp = models.DateTimeField(auto_now_add=True)  # Время отметки
    group = models.CharField(max_length=100)  # Группа, к которой относится пользователь

    def __str__(self):
        return f'{self.user} - {self.group} - {self.timestamp}'

