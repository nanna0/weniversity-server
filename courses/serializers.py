from rest_framework import serializers
from .models import Course, Chapter, Video, Instructor

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
class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['video_id', 'title', 'video_url', 'duration', 'order_index']


class ChapterSerializer(serializers.ModelSerializer):
    videos = VideoSerializer(source='video_set', many=True, read_only=True)

    class Meta:
        model = Chapter
        fields = ['chapter_id', 'title', 'order_index', 'videos']


class CourseSerializer(serializers.ModelSerializer):
    chapters = ChapterSerializer(many=True, read_only=True)
    instructors = InstructorSerializer(many=True, read_only=True)
    code_str = serializers.SerializerMethodField()
    class Meta:
        model = Course
        fields = "__all__"

    def get_price_label(self, obj):
        if obj.price == 0:
            return "free"
        elif obj.price > 0:
            return "paid"
        else:
            return "gov"
        
    def get_code_str(self, obj):
        return f"{obj.code:05d}" if obj.code is not None else None

class CourseDetailSerializer(serializers.ModelSerializer):
    chapters = ChapterSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ["course_id", "uuid", "order_index", "title", "category", "type", "level",
                  "price", "description", "course_time", "course_duedate",
                  "discord_url", "is_active", "created_at", "chapters"]
        
