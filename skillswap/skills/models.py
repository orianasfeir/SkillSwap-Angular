from django.db import models
from users.models import User

class Skill(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_featured = models.BooleanField(default=False)

    class Meta:
        db_table = 'skills'

class UserSkill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skills')
    skill = models.ForeignKey('Skill', on_delete=models.CASCADE)
    proficiency_level = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'user_skills'
        unique_together = (('user', 'skill'),)
