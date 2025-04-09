from django.db import models
from users.models import User, Qualification

class Skill(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'skills'

class UserSkill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skills')
    skill = models.ForeignKey('Skill', on_delete=models.CASCADE, related_name='skill')
    proficiency_level = models.IntegerField(blank=True, null=True)
    qualifications = models.ManyToManyField(Qualification, blank=True, related_name='user_skills')

    def __str__(self):
        return f"{self.user.username}'s {self.skill.name}"

    class Meta:
        db_table = 'user_skills'
        unique_together = (('user', 'skill'),)
