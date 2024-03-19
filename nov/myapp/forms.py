from django import forms
from django.shortcuts import get_object_or_404, redirect
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Subscription

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class SubscriptionForm(ModelForm):
    class Meta:
        model = Subscription
        fields = ['group', 'client', 'coach', 'lessons_count', 'attendance', 'comment']

