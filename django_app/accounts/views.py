from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm, UserProfileForm
from .models import UserProfile
from gameplay.models import Play, PlaySession


def register(request):
    """User registration"""
    if request.user.is_authenticated:
        return redirect('stories:list')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome, {user.username}! Your account has been created.")
            return redirect('stories:list')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/login.html', {'form': form})


def login_view(request):
    """User login"""
    if request.user.is_authenticated:
        return redirect('stories:list')
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            next_url = request.GET.get('next', 'stories:list')
            return redirect(next_url)
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """User logout"""
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('stories:list')


@login_required
def profile(request):
    """View/edit user profile"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=profile)
    
    # Get user's play history
    plays = Play.objects.filter(user=request.user)[:10]
    sessions = PlaySession.objects.filter(user=request.user)[:5]
    
    return render(request, 'accounts/profile.html', {
        'form': form,
        'profile': profile,
        'plays': plays,
        'sessions': sessions
    })
