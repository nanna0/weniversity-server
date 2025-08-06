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
from .serializers import UserSerializer, CustomTokenObtainPairSerializer, UserUpdateSerializer, UserPasswordChangeSerializer

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
        serializer = UserUpdateSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
         # --- 디버깅 코드 추가 ---
        print("===================================")
        print("1. VIEW DATA CHECK START")
        print(f"request.user: {request.user}")
        print(f"request.data: {request.data}")
        # 파일 데이터는 request.FILES에 별도로 담깁니다. 이 부분이 가장 중요합니다.
        print(f"request.FILES: {request.FILES}") 
        print("1. VIEW DATA CHECK END")
        print("===================================")
        # --- 디버깅 코드 끝 ---
        serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "회원정보가 수정되었습니다."})
        print("SERIALIZER ERRORS:", serializer.errors) 
        return Response(serializer.errors, status=400)
    
# ✅ 비밀번호 변경
class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        serializer = UserPasswordChangeSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "비밀번호가 변경되었습니다."})
        return Response(serializer.errors, status=400)
    
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .serializers import PasswordResetRequestSerializer, PasswordResetConfirmSerializer
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.template.loader import render_to_string


# 1. 비밀번호 재설정 요청을 받는 View
class PasswordResetRequestView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.get(email=email)

            # 토큰 및 UID 생성
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            
            # 재설정 링크 생성
            reset_link = f"{settings.FRONTEND_URL}/password-reset-confirm/{uid}/{token}/"
            
            # 이메일 내용 템플릿화
            subject = "[YourService] 비밀번호 재설정 안내"
            message = render_to_string('emails/password_reset_email.html', {
                'username': user.username,
                'reset_link': reset_link,
            })

            # 이메일 발송
            print(f"Sending password reset email to {email} with link: {reset_link}")
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                html_message=message # HTML 형식으로 이메일 보내기
            )

            return Response({"message": "비밀번호 재설정 이메일이 발송되었습니다."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 2. 비밀번호 재설정 확인 및 변경 View
class PasswordResetConfirmView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, uidb64, token, *args, **kwargs):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            if serializer.is_valid():
                new_password = serializer.validated_data['new_password1']
                user.set_password(new_password)
                user.save()
                return Response({"message": "비밀번호가 성공적으로 변경되었습니다."}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"error": "링크가 유효하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)