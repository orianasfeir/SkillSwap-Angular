from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Qualification
from .forms import CustomUserCreationForm, ProfileEditForm, QualificationForm
from skills.models import UserSkill
from reviews.models import Review
from django.db import models
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User
from .serializers import (
    UserSerializer, UserCreateSerializer, UserUpdateSerializer,
    QualificationSerializer
)
from django.db.models import Q

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
    active_swaps = user.requests_received.filter(status='accepted') | user.requests_made.filter(status='accepted')
    completed_swaps = user.requests_received.filter(status='completed') | user.requests_made.filter(status='completed')
    
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

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        login(request, user)
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def profile(self, request):
        user = request.user
        user_skills = UserSkill.objects.filter(user=user).select_related('skill')
        for skill in user_skills:
            skill.divided_proficiency = skill.proficiency_level // 2 if skill.proficiency_level else 0
        
        reviews = Review.objects.filter(user_reviewed=user).select_related('reviewer')
        completed_swaps = user.requests_received.filter(status='completed')
        
        data = {
            'user': UserSerializer(user).data,
            'skills': [{'id': skill.id, 'name': skill.skill.name, 'proficiency': skill.divided_proficiency} 
                      for skill in user_skills],
            'reviews': [{'id': review.id, 'text': review.text, 'rating': review.rating,
                        'reviewer': review.reviewer.username} for review in reviews],
            'completed_swaps': [{'id': swap.id, 'skill': swap.skill_requested.name} 
                               for swap in completed_swaps]
        }
        return Response(data)

    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        user = request.user
        profile = user.profile
        skills = user.skills.all()
        
        reviews = Review.objects.filter(
            Q(reviewer=user) | Q(user_reviewed=user)
        ).select_related('reviewer', 'user_reviewed')
        
        incoming_requests = user.requests_received.filter(status='pending')
        outgoing_requests = user.requests_made.filter(status='pending')
        active_swaps = user.requests_received.filter(status='accepted') | user.requests_made.filter(status='accepted')
        completed_swaps = user.requests_received.filter(status='completed') | user.requests_made.filter(status='completed')
        
        for swap in completed_swaps:
            swap.review = Review.objects.filter(swap_request=swap).first()
        
        data = {
            'profile': UserSerializer(user).data,
            'skills': [{'id': skill.id, 'name': skill.skill.name} for skill in skills],
            'reviews': [{'id': review.id, 'text': review.text, 'rating': review.rating,
                        'reviewer': review.reviewer.username} for review in reviews],
            'incoming_requests': [{'id': req.id, 'skill': req.skill_requested.name} 
                                for req in incoming_requests],
            'outgoing_requests': [{'id': req.id, 'skill': req.skill_requested.name} 
                                for req in outgoing_requests],
            'active_swaps': [{'id': swap.id, 'skill': swap.skill_requested.name} 
                            for swap in active_swaps],
            'completed_swaps': [{'id': swap.id, 'skill': swap.skill_requested.name,
                               'review': swap.review.text if swap.review else None} 
                               for swap in completed_swaps]
        }
        return Response(data)

class QualificationViewSet(viewsets.ModelViewSet):
    serializer_class = QualificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Qualification.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)