from rest_framework import serializers
from .models import SkillSwapRequest
from users.serializers import UserSerializer
from skills.serializers import SkillSerializer
from users.models import User
from skills.models import Skill

class SkillSwapRequestSerializer(serializers.ModelSerializer):
    user_requesting = UserSerializer(read_only=True)
    user_requested = UserSerializer(read_only=True)
    skill_offered = SkillSerializer(read_only=True)
    skill_requested = SkillSerializer(read_only=True)
    
    # Write-only fields for creating/updating
    user_requested_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='user_requested',
        write_only=True
    )
    skill_offered_id = serializers.PrimaryKeyRelatedField(
        queryset=Skill.objects.all(),
        source='skill_offered',
        write_only=True
    )
    skill_requested_id = serializers.PrimaryKeyRelatedField(
        queryset=Skill.objects.all(),
        source='skill_requested',
        write_only=True
    )

    class Meta:
        model = SkillSwapRequest
        fields = [
            'id', 'user_requesting', 'user_requested', 'status',
            'skill_offered', 'skill_requested', 'proposed_time',
            'created_at', 'updated_at', 'is_read',
            'user_requested_id', 'skill_offered_id', 'skill_requested_id'
        ]
        read_only_fields = ['id', 'user_requesting', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['user_requesting'] = self.context['request'].user
        return super().create(validated_data)

class SkillSwapRequestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillSwapRequest
        fields = ['user_requested', 'skill_offered', 'skill_requested', 'proposed_time']

class SkillSwapRequestUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillSwapRequest
        fields = ['status', 'proposed_time']