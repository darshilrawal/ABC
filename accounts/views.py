from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistrationForm


def register_view(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('main:home')
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful! Please login with your credentials.')
            return redirect('accounts:login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')
    else:
        form = RegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('main:home')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Try to authenticate treating email as username (for users where username=email)
        user = authenticate(request, username=email, password=password)
        
        # If that fails, try looking up user by email directly (for legacy users/admin)
        if user is None:
            from django.contrib.auth.models import User
            try:
                # Case insensitive search for email might be better, but exact match for now
                user_obj = User.objects.get(email=email)
                user = authenticate(request, username=user_obj.username, password=password)
            except (User.DoesNotExist, User.MultipleObjectsReturned):
                user = None
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name if user.first_name else user.username}!')
            next_url = request.GET.get('next', 'main:home')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid email or password.')
    
    return render(request, 'accounts/login.html')


def logout_view(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('main:home')


@login_required
def profile_view(request):
    """User profile view"""
    return render(request, 'accounts/profile.html')
