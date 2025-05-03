from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Review
from .forms import ReviewForm
from swaps.models import SkillSwapRequest
from django.core.exceptions import PermissionDenied
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Avg
from .serializers import ReviewSerializer, ReviewCreateSerializer

# Create your views here.

@login_required
def create_review(request, swap_id):
    swap = get_object_or_404(SkillSwapRequest, id=swap_id)
    
    # Ensure the user is either the requester or the receiver
    if request.user != swap.user_requesting and request.user != swap.user_requested:
        raise PermissionDenied("You don't have permission to review this swap.")
    
    # Only allow reviewing completed swaps
    if swap.status != 'completed':
        messages.error(request, "You can only review completed swaps.")
        return redirect('users:dashboard')
    
    # Check if user has already reviewed this swap
    if Review.objects.filter(swap_request=swap, reviewer=request.user).exists():
        messages.error(request, "You have already reviewed this swap.")
        return redirect('users:dashboard')
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.reviewer = request.user
            review.user_reviewed = swap.user_requesting if request.user == swap.user_requested else swap.user_requested
            review.swap_request = swap
            review.save()
            
            messages.success(request, "Review submitted successfully!")
            return redirect('users:dashboard')
    else:
        form = ReviewForm()
    
    return render(request, 'reviews/create_review.html', {
        'form': form,
        'swap': swap
    })

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Review.objects.all()

    def get_queryset(self):
        return self.queryset.filter(
            user_reviewed=self.request.user
        ).select_related('reviewer', 'user_reviewed', 'swap_request')

    def get_serializer_class(self):
        if self.action == 'create':
            return ReviewCreateSerializer
        return ReviewSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=['get'])
    def user_reviews(self, request):
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response(
                {'error': 'user_id parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        reviews = self.queryset.filter(user_reviewed_id=user_id).select_related(
            'reviewer', 'user_reviewed', 'swap_request'
        )
        serializer = self.get_serializer(reviews, many=True)
        
        # Calculate average rating
        avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
        
        return Response({
            'reviews': serializer.data,
            'average_rating': round(avg_rating, 1)
        })

    @action(detail=False, methods=['get'])
    def my_reviews(self, request):
        reviews = self.queryset.filter(reviewer=request.user).select_related(
            'user_reviewed', 'swap_request'
        )
        serializer = self.get_serializer(reviews, many=True)
        return Response(serializer.data)
