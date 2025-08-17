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
            "updated_at"
        ]
        read_only_fields = ["id", "is_active", "created_at", "updated_at"]
        extra_kwargs = {
            "password": {"write_only": True},
        }
    def get_profile_image_url(self, obj):
        if not obj.profile_image:
            return None
        request = self.context.get("request")
        url = obj.profile_image.url  # '/media/…' 형태
        return request.build_absolute_uri(url) if request else url
    
    # 회원가입시 랜덤 사진 지정 
    def create(self, validated_data):
        if not validated_data.get("profile_image"):
            default_images = [
                'profiles/default1.png',
                'profiles/default2.png',
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
        request = self.context.get("request")
        profile_url = None
        if user.profile_image:
            try:
                profile_url = user.profile_image.url  # '/media/...' (문자열)
                if request:
                    profile_url = request.build_absolute_uri(profile_url)
            except ValueError:
                profile_url = None

        data.update({
            "email": user.email,
            "name": user.name,
            "role": user.role,
            "profile_image_url": profile_url,  # <-- bytes 대신 URL 문자열
        })
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
    
# 비밀번호 재설정 요청 시 이메일 검증
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        try:
            User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("해당 이메일을 가진 사용자가 존재하지 않습니다.")
        return value

class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password1 = serializers.CharField(required=True, write_only=True)
    new_password2 = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        if data['new_password1'] != data['new_password2']:
            raise serializers.ValidationError("두 비밀번호가 일치하지 않습니다.")
        
        try:
            # Django의 기본 비밀번호 검증 로직 사용
            validate_password(data['new_password1'])
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
            
        return data