from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Review
from .forms import ReviewForm
from swaps.models import SkillSwapRequest
from django.core.exceptions import PermissionDenied

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
