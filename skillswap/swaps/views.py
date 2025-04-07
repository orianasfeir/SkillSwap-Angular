from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import SkillSwapRequest
from users.models import User
from skills.models import Skill

@login_required
def create_swap_request(request, user_id, skill_id):
    if request.method == 'POST':
        requested_user = get_object_or_404(User, pk=user_id)
        offered_skill = get_object_or_404(Skill, pk=skill_id)
        
        swap = SkillSwapRequest(
            user_requesting=request.user,
            user_requested=requested_user,
            skill_offered=offered_skill,
            skill_requested=get_object_or_404(Skill, pk=request.POST.get('skill_requested')),
            proposed_time=request.POST.get('proposed_time'),
            status='pending'
        )
        swap.save()
        return redirect('swaps:swap_list')
    
    requested_user = get_object_or_404(User, pk=user_id)
    offered_skill = get_object_or_404(Skill, pk=skill_id)
    available_skills = request.user.skills.all()
    return render(request, 'swaps/create_request.html', {
        'requested_user': requested_user,
        'offered_skill': offered_skill,
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
    swap = get_object_or_404(SkillSwapRequest, pk=swap_id, user_requested=request.user)
    swap.status = 'accepted'
    swap.save()
    return redirect('swaps:swap_list')

@login_required
def reject_swap(request, swap_id):
    swap = get_object_or_404(SkillSwapRequest, pk=swap_id, user_requested=request.user)
    swap.status = 'rejected'
    swap.save()
    return redirect('swaps:swap_list')
