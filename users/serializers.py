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

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        if not validated_data.get("profile_image"):
            default_images = [
                'defaults/default1.png',
                'defaults/default2.png',
                'defaults/default3.png',
            ]
            validated_data['profile_image'] = random.choice(default_images)
        user = User.objects.create_user(**validated_data)
        return super().create(validated_data)

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
        return data