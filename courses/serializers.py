from rest_framework import serializers
from .models import Course, Chapter, Video, Instructor, Enrollment, CourseLike
from django.core.validators import FileExtensionValidator
class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructor
        fields = [
            'instructor_id',
            'name',
            'english_name',
            'code',
            'course',
            'created_at',
            'affiliation',
            "profile_image",
        ]
class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['video_id', 'title', 'video_file', 'duration', 'order_index']


class ChapterSerializer(serializers.ModelSerializer):
    videos = VideoSerializer(many=True, read_only=True)

    class Meta:
        model = Chapter
        fields = ['chapter_id', 'title', 'order_index', 'videos']


class CourseSerializer(serializers.ModelSerializer):
    chapters = ChapterSerializer(many=True, read_only=True)
    instructors = InstructorSerializer(many=True, read_only=True)
    is_liked = serializers.BooleanField(read_only=True)
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
        fields = ["course_id", "order_index", "title", "category", "type", "level",
                  "price", "description", "course_time", "course_duedate",
                  "discord_url", "is_active", "created_at", "chapters", "course_image", "code"]
        
class CourseMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['course_id', 'title', 'description']   # 필요 시 fields 축소/확장

class MyCourseSerializer(serializers.ModelSerializer):
    course = CourseMiniSerializer(read_only=True)

    class Meta:
        model = Enrollment
        fields = ['course', 'status', 'progress', 'enrolled_at']


class CourseMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['course_id', 'title', 'description', 'course_image']

class MyLikedCourseSerializer(serializers.ModelSerializer):
    course = CourseMiniSerializer(read_only=True)
    liked_at = serializers.DateTimeField(source='created_at', read_only=True)

    class Meta:
        model = CourseLike
        fields = ['course', 'liked_at']

