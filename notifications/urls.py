from django.urls import path
from .views import mark_notification_read

urlpatterns = [
    path('read/<int:notification_id>/', mark_notification_read, name='mark_notification_read'),
]
