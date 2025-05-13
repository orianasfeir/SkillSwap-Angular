from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import SkillSwapRequest
from users.models import User
from skills.models import Skill, UserSkill
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import (
    SkillSwapRequestSerializer,
    SkillSwapRequestCreateSerializer,
    SkillSwapRequestUpdateSerializer
)
from django.db import models


class SkillSwapRequestViewSet(viewsets.ModelViewSet):
    serializer_class = SkillSwapRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SkillSwapRequest.objects.filter(
            models.Q(user_requested=self.request.user) |
            models.Q(user_requesting=self.request.user)
        ).select_related(
            'user_requesting',
            'user_requested',
            'skill_offered',
            'skill_requested'
        )

    def get_serializer_class(self):
        if self.action == 'create':
            return SkillSwapRequestCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return SkillSwapRequestUpdateSerializer
        return SkillSwapRequestSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Create the swap request
        swap_request = SkillSwapRequest.objects.create(
            user_requesting=request.user,
            user_requested=serializer.validated_data['user_requested'],
            skill_offered_id=serializer.validated_data['skill_offered'].id,
            skill_requested_id=serializer.validated_data['skill_requested'].id,
            proposed_time=serializer.validated_data.get('proposed_time')
        )

        return Response(
            SkillSwapRequestSerializer(swap_request).data,
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        swap_request = self.get_object()
        
        if swap_request.status != 'pending':
            return Response(
                {'error': 'Only pending swap requests can be accepted.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        swap_request.status = 'accepted'
        swap_request.save()
        
        return Response(SkillSwapRequestSerializer(swap_request).data)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        swap_request = self.get_object()
        
        if swap_request.status != 'pending':
            return Response(
                {'error': 'Only pending swap requests can be rejected.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        swap_request.status = 'rejected'
        swap_request.save()
        
        return Response(SkillSwapRequestSerializer(swap_request).data)

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        swap_request = self.get_object()
        
        if swap_request.status != 'accepted':
            return Response(
                {'error': 'Only accepted swap requests can be completed.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        swap_request.status = 'completed'
        swap_request.save()
        
        return Response(SkillSwapRequestSerializer(swap_request).data)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        swap_request = self.get_object()
        
        if swap_request.status != 'pending':
            return Response(
                {'error': 'Only pending swap requests can be cancelled.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        swap_request.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        count = self.get_queryset().filter(is_read=False).count()
        return Response({'unread_count': count})
    
    @action(detail=False, methods=['get'])
    def pending(self, request):
        queryset = self.get_queryset().filter(status='pending')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def ongoing(self, request):
        queryset = self.get_queryset().filter(status__in=['accepted', 'in_progress'])
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def incoming_requests(self, request):
        """Return all incoming swap requests for the authenticated user."""
        queryset = self.get_queryset().filter(user_requested=request.user, status='pending')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def outgoing_requests(self, request):
        """Return all outgoing swap requests made by the authenticated user."""
        queryset = self.get_queryset().filter(user_requesting=request.user, status='pending')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def active_requests(self, request):
        """Return all active swap requests for the authenticated user."""
        queryset = self.get_queryset().filter(
            models.Q(user_requested=request.user) | models.Q(user_requesting=request.user),
            status__in=['accepted', 'in_progress']
        )
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
