from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import SkillSwapRequest
from users.models import User
from skills.models import Skill
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

@login_required
def create_swap_request(request, user_id, skill_id):
    if request.method == 'POST':
        requested_user = get_object_or_404(User, pk=user_id)
        requested_skill = get_object_or_404(Skill, pk=skill_id)
        
        swap = SkillSwapRequest(
            user_requesting=request.user,
            user_requested=requested_user,
            skill_offered=get_object_or_404(Skill, pk=request.POST.get('skill_offered')),
            skill_requested=requested_skill,
            proposed_time=request.POST.get('proposed_time'),
            status='pending'
        )
        swap.save()
        return redirect('swaps:swap_list')
    
    requested_user = get_object_or_404(User, pk=user_id)
    requested_skill = get_object_or_404(Skill, pk=skill_id)
    available_skills = request.user.skills.all()
    return render(request, 'swaps/create_request.html', {
        'requested_user': requested_user,
        'requested_skill': requested_skill,
        'skills': available_skills
    })

@login_required
def swap_requests(request):
    requests = SkillSwapRequest.objects.filter(user_requested=request.user, status='pending')
    unread_count = requests.filter(is_read=False).count()
    return render(request, 'swaps/list.html', {
        'swap_requests': requests,
        'unread_count': unread_count
    })

@login_required
def accept_swap(request, swap_id):
    swap_request = get_object_or_404(SkillSwapRequest, id=swap_id)
    
    # Check if the user is the one being requested
    if swap_request.user_requested != request.user:
        messages.error(request, "You can only accept requests made to you.")
        return redirect('users:dashboard')
    
    # Only allow accepting pending requests
    if swap_request.status != 'pending':
        messages.error(request, "You can only accept pending swap requests.")
        return redirect('users:dashboard')
    
    swap_request.status = 'accepted'
    swap_request.save()
    messages.success(request, "Swap request accepted successfully.")
    return redirect('users:dashboard')

@login_required
def reject_swap(request, swap_id):
    swap_request = get_object_or_404(SkillSwapRequest, id=swap_id)
    
    # Check if the user is the one being requested
    if swap_request.user_requested != request.user:
        messages.error(request, "You can only reject requests made to you.")
        return redirect('users:dashboard')
    
    # Only allow rejecting pending requests
    if swap_request.status != 'pending':
        messages.error(request, "You can only reject pending swap requests.")
        return redirect('users:dashboard')
    
    swap_request.status = 'rejected'
    swap_request.save()
    messages.success(request, "Swap request rejected successfully.")
    return redirect('users:dashboard')

@login_required
def complete_swap(request, swap_id):
    swap = get_object_or_404(SkillSwapRequest, id=swap_id)
    
    # Ensure the user is either the requester or the receiver
    if request.user != swap.user_requesting and request.user != swap.user_requested:
        raise PermissionDenied("You don't have permission to complete this swap.")
    
    # Only allow completing accepted swaps
    if swap.status != 'accepted':
        messages.error(request, "Only accepted swaps can be marked as completed.")
        return redirect('users:dashboard')
    
    swap.status = 'completed'
    swap.save()
    
    messages.success(request, "Swap marked as completed successfully!")
    return redirect('users:dashboard')

@login_required
def cancel_swap(request, swap_id):
    swap_request = get_object_or_404(SkillSwapRequest, id=swap_id)
    
    # Check if the user is the one who made the request
    if swap_request.user_requesting != request.user:
        messages.error(request, "You can only cancel your own swap requests.")
        return redirect('users:dashboard')
    
    # Only allow canceling pending requests
    if swap_request.status != 'pending':
        messages.error(request, "You can only cancel pending swap requests.")
        return redirect('users:dashboard')
    
    # Delete the swap request
    swap_request.delete()
    messages.success(request, "Swap request cancelled successfully.")
    return redirect('users:dashboard')

class SkillSwapRequestViewSet(viewsets.ModelViewSet):
    serializer_class = SkillSwapRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SkillSwapRequest.objects.filter(
            user_requested=self.request.user
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
            skill_offered=serializer.validated_data['skill_offered'],
            skill_requested=serializer.validated_data['skill_requested'],
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
