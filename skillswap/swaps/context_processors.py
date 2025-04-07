from .models import SkillSwapRequest

def unread_swap_requests(request):
    if request.user.is_authenticated:
        unread_count = SkillSwapRequest.objects.filter(
            user_requested=request.user,
            status='pending',
            is_read=False
        ).count()
        return {'unread_count': unread_count}
    return {'unread_count': 0} 