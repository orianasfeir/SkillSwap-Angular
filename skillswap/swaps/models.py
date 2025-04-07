from django.db import models
from users.models import User
from skills.models import Skill

class SkillSwapRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    ]
    
    user_requesting = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests_made')
    user_requested = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests_received')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    skill_offered = models.ForeignKey(Skill, on_delete=models.SET_NULL, null=True, related_name='offered_in_swaps')
    skill_requested = models.ForeignKey(Skill, on_delete=models.SET_NULL, null=True, related_name='requested_in_swaps')
    proposed_time = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        db_table = 'skill_swap_requests'