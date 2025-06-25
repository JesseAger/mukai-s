from django.shortcuts import render

from .models import Notification

def get_user_notifications(user):
    return Notification.objects.filter(user=user).order_by('-created_at')

