from django.db import models
from users.models import User
from swaps.models import SkillSwapRequest

class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='reviews_given')
    user_reviewed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_received')
    text = models.TextField()
    rating = models.IntegerField()
    swap_request = models.ForeignKey(SkillSwapRequest, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'reviews'
