from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import Subscription

@shared_task
def update_button_highlighted():
    subscriptions = Subscription.objects.filter(button_highlighted=True)
    for subscription in subscriptions:
        if subscription.date + timedelta(hours=12) < timezone.now():
            subscription.button_highlighted = False
            subscription.save()