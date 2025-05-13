from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Skill, UserSkill
from .forms import AddSkillForm, QualificationForm
from reviews.models import Review
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import SkillSerializer, UserSkillSerializer

class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def retrieve(self, request, pk=None):
        skill = self.get_object()
        user_has_skill = UserSkill.objects.filter(
            user=request.user,
            skill=skill
        ).exists()
        
        users_offering = UserSkill.objects.filter(
            skill=skill
        ).exclude(
            user=request.user
        ).select_related(
            'user'
        ).prefetch_related(
            'qualifications'
        )
        
        reviews = Review.objects.filter(
            swap_request__skill_requested=skill
        ).select_related('reviewer')
        
        data = {
            'skill': SkillSerializer(skill).data,
            'user_has_skill': user_has_skill,
            'users_offering': [{
                'user': {
                    'id': us.user.id,
                    'username': us.user.username,
                    'profile_image': us.user.profile_image.url if us.user.profile_image else None
                },
                'proficiency_level': us.proficiency_level,
                'qualifications': [{
                    'id': q.id,
                    'description': q.description,
                    'verified': q.verified
                } for q in us.qualifications.all()]
            } for us in users_offering],
            'reviews': [{
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'reviewer': review.reviewer.username
            } for review in reviews]
        }
        return Response(data)

class UserSkillViewSet(viewsets.ModelViewSet):
    serializer_class = UserSkillSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserSkill.objects.filter(user=self.request.user).select_related('skill')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def browse(self, request):
        skills = Skill.objects.all().order_by('-created_at')
        return Response(SkillSerializer(skills, many=True).data)

    @action(detail=False, methods=['get'])
    def home(self, request):
        recent_skills = Skill.objects.order_by('-created_at')[:3]
        recent_reviews = Review.objects.select_related('reviewer').order_by('-created_at')[:3]
        
        data = {
            'featured_skills': SkillSerializer(recent_skills, many=True).data,
            'recent_reviews': [{
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'reviewer': review.reviewer.username
            } for review in recent_reviews]
        }
        return Response(data)