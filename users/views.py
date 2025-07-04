from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from notifications.views import get_user_notifications

def homepage(request):
    context= {}
    return render(request, 'users/home.html', context)

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            template = loader.get_template('users/signup_success.html')
            return HttpResponse(template.render({}, request))
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.role == 'STAFF':
                return redirect('staff_dashboard')
            elif user.role == 'SUPPORT':
                return redirect('support_dashboard')
            elif user.role == 'ADMIN':
                return redirect('admin_dashboard')

    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')

@login_required
def staff_dashboard(request):
    if request.user.role != 'STAFF':
        return redirect('login')
    return render(request, 'users/staff_dashboard.html')

@login_required
def support_dashboard(request):
    if request.user.role != 'SUPPORT':
        return redirect('login')
    
    notifications = get_user_notifications(request.user)
    return render(request, 'users/support_dashboard.html', {'notifications':notifications})

@login_required
def admin_dashboard(request):
    if request.user.role != 'ADMIN':
        return redirect('login')
    
    notifications = get_user_notifications(request.user)
    return render(request, 'users/admin_dashboard.html', {'notifications':notifications})

@login_required
def staff_dashboard(request):
    if request.user.role != 'STAFF':
        return redirect('login')
    
    notifications = get_user_notifications(request.user)
    return render(request, 'users/staff_dashboard.html', {'notifications': notifications})

@login_required
def manage_users(request):
    if request.user.role != 'ADMIN':
        return redirect('login')

    User = get_user_model()
    users = User.objects.exclude(id=request.user.id)  # exclude self
    return render(request, 'users/manage_users.html', {'users': users})

@login_required
def delete_user(request, user_id):
    if request.user.role != 'ADMIN':
        return redirect('login')

    User = get_user_model()
    user = User.objects.get(id=user_id)
    user.delete()
    return redirect('manage_users')
