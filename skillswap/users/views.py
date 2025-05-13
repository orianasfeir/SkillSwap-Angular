from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Qualification
from .forms import CustomUserCreationForm, ProfileEditForm, QualificationForm
from skills.models import UserSkill
from reviews.models import Review
from django.db import models
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from .models import User
from .serializers import (
    UserSerializer, UserCreateSerializer, UserUpdateSerializer,
    QualificationSerializer
)
from django.db.models import Q
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from reviews.serializers import ReviewSerializer


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
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'token': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name
            }
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get', 'patch'])
    def profile(self, request):
        user = request.user
        if request.method == 'PATCH':
            # Log the incoming data for debugging
            print("PATCH request data:", request.data)

            serializer = UserUpdateSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            # Log the updated user data
            print("Updated user data:", serializer.data)

            return Response(serializer.data)
            
        user_skills = UserSkill.objects.filter(user=user).select_related('skill')
        for skill in user_skills:
            skill.divided_proficiency = skill.proficiency_level // 2 if skill.proficiency_level else 0
        
        reviews = Review.objects.filter(user_reviewed=user).select_related('reviewer', 'swap_request', 'swap_request__skill_requested')
        completed_swaps = user.requests_received.filter(status='completed')
        
        data = {
            'user': UserSerializer(user).data,
            'skills': [{'id': skill.id, 'name': skill.skill.name, 'proficiency': skill.divided_proficiency} 
                      for skill in user_skills],
            'reviews': [{
                'id': review.id, 
                'text': review.text, 
                'rating': review.rating,
                'reviewer': review.reviewer.username,
                'reviewer_profile_image': review.reviewer.profile_image.url if review.reviewer.profile_image else None,
                'skill_name': review.swap_request.skill_requested.name if review.swap_request and review.swap_request.skill_requested else 'Unknown skill'
            } for review in reviews],
            'completed_swaps': [{'id': swap.id, 'skill': swap.skill_requested.name} 
                               for swap in completed_swaps]
        }
        return Response(data)

    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        user = request.user
        profile = user.profile
        skills = user.user_skills.all()
        
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

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Return reviews where the user is either the reviewer or the one being reviewed
        return Review.objects.filter(
            Q(reviewer=self.request.user) | Q(user_reviewed=self.request.user)
        ).select_related('reviewer', 'user_reviewed')

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_api(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response(
            {'error': 'Please provide both username and password'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = authenticate(username=username, password=password)
    
    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'token': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name
            }
        })
    else:
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )