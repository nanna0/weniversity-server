from datetime import datetime
import random
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import authenticate
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from .models import User
from .serializers import UserSerializer, CustomTokenObtainPairSerializer


# ✅ 회원가입
class UserRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "회원가입이 완료되었습니다."},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ✅ 로그인 (커스텀 토큰 사용)
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# ✅ 관리자 페이지 접근 권한
from .permissions import IsAdminUserRole
class AdminDashboardView(APIView):
    permission_classes = [IsAdminUserRole] # 관리자 권한 확인

    def get(self, request):
        return Response({'message': '관리자 페이지입니다.'})

# ✅ 로그아웃
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {"detail": "Logout successful."},
                status=status.HTTP_205_RESET_CONTENT,
            )
        except KeyError:
            return Response(
                {"error": "Refresh token is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except TokenError:
            return Response(
                {"error": "Invalid token."},
                status=status.HTTP_400_BAD_REQUEST,
            )


# ✅ 헬스 체크
@api_view(["GET"])
@permission_classes([AllowAny])
def health_check(request):
    return Response(
        {
            "status": "ok",
            "timestamp": datetime.now().isoformat(),
        },
        status=status.HTTP_200_OK,
    )

# ✅ 마이페이지 조회/수정
class MyPageView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ✅ 프로필 이미지 업로드
class ProfileImageUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "프로필 이미지가 업데이트 되었습니다."}, serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)