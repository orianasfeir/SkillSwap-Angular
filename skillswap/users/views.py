from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Qualification
from .forms import CustomUserCreationForm, ProfileEditForm, QualificationForm
from skills.models import UserSkill
from reviews.models import Review

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request):
    profile_user = request.user
    user_skills = UserSkill.objects.filter(user=profile_user).select_related('skill')
    reviews = Review.objects.filter(user_reviewed=profile_user).select_related('reviewer')
    completed_swaps = profile_user.requests_received.filter(status='completed')
    
    context = {
        'profile_user': profile_user,
        'skills': [user_skill.skill for user_skill in user_skills],
        'reviews': reviews,
        'completed_swaps': completed_swaps
    }
    return render(request, 'users/profile.html', context)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileEditForm(instance=request.user)
    return render(request, 'users/edit_profile.html', {'form': form})

@login_required
def add_qualification(request):
    if request.method == 'POST':
        form = QualificationForm(request.POST, request.FILES)
        if form.is_valid():
            qualification = form.save(commit=False)
            qualification.user = request.user
            qualification.save()
            return redirect('profile')
    else:
        form = QualificationForm()
    return render(request, 'users/add_qualification.html', {'form': form})

@login_required
def dashboard(request):
    user = request.user
    profile = user.profile
    skills = user.skills.all()
    reviews = user.reviews_received.all()
    swap_requests = user.requests_received.filter(status='pending')
    
    context = {
        'profile': profile,
        'skills': skills,
        'reviews': reviews,
        'swap_requests': swap_requests,
    }
    return render(request, 'users/dashboard.html', context)