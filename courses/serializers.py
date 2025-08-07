# courses/serializers.py

from rest_framework import serializers
from .models import Course, Chapter, Video


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['video_id', 'title', 'video_url', 'duration', 'order']


class ChapterSerializer(serializers.ModelSerializer):
    videos = VideoSerializer(source='video_set', many=True, read_only=True)

    class Meta:
        model = Chapter
        fields = ['chapter_id', 'title', 'order', 'videos']


class CourseSerializer(serializers.ModelSerializer):
    chapters = ChapterSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = [
            'course_id', 'title', 'category', 'type', 'level',
            'price', 'description', 'course_time', 'course_duedate',
            'discord_url', 'created_at', 'chapters'
        ]
