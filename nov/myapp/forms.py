from django import forms
from django.shortcuts import get_object_or_404, redirect
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Subscription, LessonSchedule, TrainingRoom, Group

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class SubscriptionForm(forms.ModelForm):
    lesson_schedule = forms.ModelChoiceField(queryset=LessonSchedule.objects.none())

    class Meta:
        model = Subscription
        fields = ['group', 'client', 'coach', 'lesson_schedule', 'attendance', 'price', 'comment', 'lessons_count']
        labels = {
            'group': 'Группа',
            'client': 'Клиент',
            'coach': 'Тренер',
            'attendance': 'Посещаемость',
            'price': 'Цена',
            'comment': 'Комментарий',
            'lessons_count': 'Количество занятий',
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['lesson_schedule'].queryset = LessonSchedule.objects.filter(name=self.instance.group)
        self.fields['lesson_schedule'].label = 'График занятий'


class LessonScheduleForm(forms.ModelForm):
    class Meta:
        model = LessonSchedule
        fields = ['name', 'day_of_week', 'time', 'num_lessons', 'training_room']
        widgets = {
            'training_room': forms.Select(attrs={'class': 'form-control'}),
        }


class TrainingRoomForm(forms.ModelForm):
    class Meta:
        model = TrainingRoom
        fields = ['name']