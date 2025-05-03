from rest_framework import serializers
from .models import Skill, UserSkill
from users.serializers import QualificationSerializer

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name', 'description', 'created_at', 'is_featured']

class UserSkillSerializer(serializers.ModelSerializer):
    skill = SkillSerializer(read_only=True)
    skill_id = serializers.PrimaryKeyRelatedField(
        queryset=Skill.objects.all(),
        source='skill',
        write_only=True
    )
    qualifications = QualificationSerializer(many=True, read_only=True)
    qualification_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.get_queryset().qualifications.all(),
        source='qualifications',
        many=True,
        write_only=True,
        required=False
    )

    class Meta:
        model = UserSkill
        fields = ['id', 'skill', 'skill_id', 'proficiency_level', 
                 'qualifications', 'qualification_ids']
        read_only_fields = ['id']

    def create(self, validated_data):
        qualifications = validated_data.pop('qualifications', [])
        user_skill = UserSkill.objects.create(**validated_data)
        if qualifications:
            user_skill.qualifications.set(qualifications)
        return user_skill

    def update(self, instance, validated_data):
        qualifications = validated_data.pop('qualifications', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if qualifications is not None:
            instance.qualifications.set(qualifications)
        return instance 