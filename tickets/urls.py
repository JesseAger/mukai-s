from django.urls import path
from .views import create_ticket

urlpatterns = [
    path('create/', create_ticket, name='create_ticket'),
    path('staff/', staff_ticket_list, name='staff_ticket_list'),
    path('support/', support_ticket_list, name='support_ticket_list'),
]
