from django.urls import path
from . import views
from .views import staff_dashboard, support_dashboard, admin_dashboard

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
     path('logout/', views.logout_view, name='logout'),
    path('staff/dashboard/', staff_dashboard, name='staff_dashboard'),
    path('support/dashboard/', support_dashboard, name='support_dashboard'),
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
]
