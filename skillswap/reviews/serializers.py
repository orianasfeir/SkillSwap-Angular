from rest_framework import serializers
from .models import Review
from users.serializers import UserSerializer
from swaps.serializers import SkillSwapRequestSerializer
from users.models import User
from swaps.models import SkillSwapRequest

class ReviewSerializer(serializers.ModelSerializer):
    reviewer = UserSerializer(read_only=True)
    user_reviewed = UserSerializer(read_only=True)
    swap_request = SkillSwapRequestSerializer(read_only=True)
    
    # Write-only fields for creating/updating
    user_reviewed_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='user_reviewed',
        write_only=True
    )
    swap_request_id = serializers.PrimaryKeyRelatedField(
        queryset=SkillSwapRequest.objects.all(),
        source='swap_request',
        write_only=True
    )

    class Meta:
        model = Review
        fields = [
            'id', 'reviewer', 'user_reviewed', 'text', 'rating',
            'swap_request', 'created_at', 'user_reviewed_id', 'swap_request_id'
        ]
        read_only_fields = ['id', 'reviewer', 'created_at']

    def create(self, validated_data):
        validated_data['reviewer'] = self.context['request'].user
        return super().create(validated_data)

class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['user_reviewed_id', 'swap_request_id', 'text', 'rating'] 