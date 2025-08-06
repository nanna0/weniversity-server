from django.urls import path
from .views import (
    UserRegisterView,
    CustomTokenObtainPairView,
    LogoutView,
    MyPageView,
    PasswordChangeView,
    health_check
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
 
]