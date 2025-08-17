from rest_framework import serializers
from .models import Mission

class MissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mission
        fields = ['id', 'email', 'problem_id', 'title', 'user_code', 'is_correct', 'message', 'submitted_at']
        read_only_fields = ['id', 'submitted_at']

class MissionResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mission
        fields = ['problem_id', 'title', 'user_code', 'is_correct', 'message', 'submitted_at']