from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Qualification
from .forms import CustomUserCreationForm, ProfileEditForm, QualificationForm
from skills.models import UserSkill
from reviews.models import Review
from django.db import models

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
    # Calculate the divided proficiency level for each skill
    for skill in user_skills:
        skill.divided_proficiency = skill.proficiency_level // 2 if skill.proficiency_level else 0
    reviews = Review.objects.filter(user_reviewed=profile_user).select_related('reviewer')
    completed_swaps = profile_user.requests_received.filter(status='completed')
    
    context = {
        'profile_user': profile_user,
        'skills': user_skills,
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
    # Get all reviews where user is either the reviewer or the one being reviewed
    reviews = Review.objects.filter(models.Q(reviewer=user) | models.Q(user_reviewed=user)).select_related('reviewer', 'user_reviewed')
    print(f"Found {reviews.count()} reviews for user {user.username}")
    for review in reviews:
        print(f"Review: {review.text} by {review.reviewer.username} for {review.user_reviewed.username}")
    # Get both incoming and outgoing pending requests
    incoming_requests = user.requests_received.filter(status='pending')
    outgoing_requests = user.requests_made.filter(status='pending')
    active_swaps = user.requests_received.filter(status='accepted')
    completed_swaps = user.requests_received.filter(status='completed')
    
    # Add review information to completed swaps
    for swap in completed_swaps:
        swap.review = Review.objects.filter(swap_request=swap).first()
    
    context = {
        'profile': profile,
        'skills': skills,
        'reviews': reviews,
        'incoming_requests': incoming_requests,
        'outgoing_requests': outgoing_requests,
        'active_swaps': active_swaps,
        'completed_swaps': completed_swaps,
    }
    return render(request, 'users/dashboard.html', context)