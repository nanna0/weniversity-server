from django.urls import path
from .views import (
    UserRegisterView,
    CustomTokenObtainPairView,
    LogoutView,
    MyPageView,
    PasswordChangeView,
    health_check,
    PasswordResetRequestView,
    PasswordResetConfirmView,
)
from rest_framework_simplejwt.views import TokenRefreshView



urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="user-register"),
    path("login/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("mypage/", MyPageView.as_view(), name="my_page"),
    path('mypage/change-password/', PasswordChangeView.as_view(), name='change-password'),
    path("health/", health_check, name="health_check"),
    # path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    # # # API URL은 Postman 등으로 테스트, 실제 사용자는 아래 UI URL로 접속
    # # # post 요청을 받는 api이므로 path 형식을 아래와 같이 수정
    # path('password-reset/confirm/<str:uidb64>/<str:token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm_api'),

 
]