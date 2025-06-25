from django.shortcuts import render
from .models import Notification
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required


def get_user_notifications(user):
    return Notification.objects.filter(user=user).order_by('-created_at')

@login_required
def mark_notification_read(request, notification_id):
    note = get_object_or_404(Notification, id=notification_id, user=request.user)
    if request.method == 'POST':
        note.is_read = True
        note.save()
    return redirect('staff_dashboard') 