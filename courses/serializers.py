from rest_framework import serializers
from .models import Course, Chapter, Video, Instructor


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
        fields = "__all__"

class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructor
        fields = [
            'instructor_id',
            'name',
            'code',
            'course',
            'created_at',
            'affiliation',
            "profile_image",
        ]