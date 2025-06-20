from django.urls import path
from .views import create_ticket, staff_ticket_list, support_ticket_list, update_ticket_status

urlpatterns = [
    path('create/', create_ticket, name='create_ticket'),
    path('staff/', staff_ticket_list, name='staff_ticket_list'),
    path('support/', support_ticket_list, name='support_ticket_list'),
    path('support/update/<int:ticket_id>/', update_ticket_status, name='update_ticket_status'),

]
