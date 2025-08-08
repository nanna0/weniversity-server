"""
URL configuration for weniversity project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users.views import PasswordResetRequestView, PasswordResetConfirmView
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/users/", include("users.urls")),
    path("api/courses/", include("courses.urls")),
    # 비밀번호 재설정 API URL
    path(
        "api/password-reset/",
        PasswordResetRequestView.as_view(),
        name="password_reset_request",
    ),
    # # API URL은 Postman 등으로 테스트, 실제 사용자는 아래 UI URL로 접속
    # # post 요청을 받는 api이므로 path 형식을 아래와 같이 수정
    path(
        "api/password-reset/confirm/<str:uidb64>/<str:token>/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm_api",
    ),
    # 비밀번호 재설정 UI를 서빙하는 URL
    path(
        "password-reset-confirm/<str:uidb64>/<str:token>/",
        TemplateView.as_view(template_name="password_reset_form.html"),
        name="password_reset_confirm",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
