from django.urls import path
from . import views
from .views import staff_dashboard, support_dashboard, admin_dashboard

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('staff/dashboard/', staff_dashboard, name='staff_dashboard'),
    path('support/dashboard/', support_dashboard, name='support_dashboard'),
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('admin/users/', views.manage_users, name='manage_users'),
    path('admin/users/delete/<int:user_id>/', views.delete_user, name='delete_user'),

]
