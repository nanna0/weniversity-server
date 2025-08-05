from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.hashers import make_password
from .models import User
import random


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "password",
            "name",
            "gender",
            "birth_date",
            "role",
            "is_active",
            "created_at",
            "updated_at",
            "profile_image",
        ]
        read_only_fields = ["id", "is_active", "created_at", "updated_at"]
        extra_kwargs = {
            "password": {"write_only": True},
        }
    
    # 회원가입시 랜덤 사진 지정 
    def create(self, validated_data):
        if not validated_data.get("profile_image"):
            default_images = [
                'defaults/default1.png',
                'defaults/default2.png',
            ]
            validated_data['profile_image'] = random.choice(default_images)

        validated_data['password'] = make_password(validated_data['password'])    
        user = User.objects.create(**validated_data)
        return user
    
    

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = User.EMAIL_FIELD  # 기본은 'username', 우리는 'email'

    def validate(self, attrs):
        # email과 password로 사용자 인증 시도
        email = attrs.get("email")
        password = attrs.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("등록되지 않은 이메일입니다.")

        if not user.check_password(password):
            raise serializers.ValidationError("비밀번호가 틀렸습니다.")

        data = super().validate({"email": email, "password": password})
        data["email"] = user.email
        data['role'] = user.role # 권한 정보 프론트엔드에 함께 전달
        return data
    
# 마이페이지 정보 수정
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["name", "gender", "birth_date", "profile_image"]

# 비밀번호 수정
class UserPasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate_current_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("현재 비밀번호가 틀렸습니다.")
        return value

    def validate_new_password(self, value):
        # Django 비밀번호 검증 로직 (옵션)
        from django.contrib.auth.password_validation import validate_password
        validate_password(value)
        return value

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user