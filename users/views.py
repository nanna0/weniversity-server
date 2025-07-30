from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from .models import User
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer


class UserRegisterView(APIView):
    permission_classes = [AllowAny]  # Allow any user to register

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "회원가입이 완료되었습니다."},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from datetime import datetime


@api_view(["GET"])
@permission_classes([AllowAny])
def health_check(request):
    """헬스체크 엔드포인트"""
    return Response(
        {"status": "ok", "timestamp": datetime.now().isoformat()},
        status=status.HTTP_200_OK,
    )
