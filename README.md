# Weniversity Server 🎓

**Weniversity Server**는 온라인 교육 플랫폼 **Weniversity**의 백엔드 서버입니다.  
Django + Django REST Framework(DRF)를 기반으로 구축되었으며, 강의 콘텐츠 관리, 사용자 인증, 수강 관리 등 **교육 서비스 전반의 API**를 제공합니다.

---

## 🚀 주요 기능 (Features)

### 사용자 관리
  - 회원가입, 로그인(JWT)
  - 권한/역할(Role) 기반 접근 제어
###  강의/커리큘럼 관리
  - 코스/챕터/비디오 3depth의 구조로 구성된 강의 생성 및 수정
  - 카테고리별, 레벨별, 유형별, 가격별 강의 분류 관리 및 수강 신청 기능
  - 강의 목록 조회 및 다중 검색 기능
### 미션 평가 시스템
  - (추가예정)
### 교강사 관리
  - 교강사 코드 구분 관리
  - 교강사별 담당 과목 매칭 관리
### *교육 컨텐츠(동영상) 관리
  - 강의별 세부 수업(Lesson) 관리
  - 강의별 중간/기말 미션 관리
  - 수강 신청 및 이력 관리
### CI/CD
  - Github Actions 기반 CI/CD (추가 가능)

---
## 🚀 시작하기
1) 요구사항
- Python 3.10+ (권장)
- 가상환경 사용 권장(venv/conda/poetry 등)
- SQLite는 기본 동작, 운영은 별도 RDB 권장

2) 설치
### 1) 클론
```
git clone https://github.com/nanna0/weniversity-server.git
cd weniversity-server
```

### 2) 가상환경 생성/활성화 (예: venv)
```
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

### 3) 패키지 설치
```
pip install --upgrade pip
pip install -r requirements.txt
```

3) 환경변수
```
# Django
SECRET_KEY=changeme-to-a-strong-secret
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# JWT(SimpleJWT) 예시(필요 시)
ACCESS_TOKEN_LIFETIME=60         # 분
REFRESH_TOKEN_LIFETIME=1440      # 분 (1일)

# EMAIL
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=...
EMAIL_HOST_PASSWORD=your app password
DEFAULT_FROM_EMAIL=...
```

4) DB 마이그레이션/관리자 생성/개발 서버
```
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
# http://127.0.0.1:8000
```

## 🛠️ 기술 스택 (Tech Stack)

- **Backend**

  - <img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=yellow"> <img src="https://img.shields.io/badge/django-092E20?style=for-the-badge&logo=django&logoColor=white"> <img src="https://camo.githubusercontent.com/6e311e5fb8b5e6c95e2609cba8f8f4de27cc35217a5d31f1119caca596cbebd4/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f444a414e474f2d524553546672616d65776f726b2d6666313730393f7374796c653d666f722d7468652d6261646765266c6f676f3d646a616e676f266c6f676f436f6c6f723d776869746526636f6c6f723d666631373039266c6162656c436f6c6f723d67726179" alt="DjangoREST" data-canonical-src="https://img.shields.io/badge/DJANGO-RESTframework-ff1709?style=for-the-badge&amp;logo=django&amp;logoColor=white&amp;color=ff1709&amp;labelColor=gray" style="max-width: 100%;">

- **Database**

  - SQLite3 (개발 기본)

- **인증/보안**

  - JWT 인증 (`djangorestframework-simplejwt`)
  - CORS 정책 지원
  - 환경변수 기반 보안 설정

- **InfraStructure**

  - <img src="https://img.shields.io/badge/AWS%20EC2-FF9900?style=for-the-badge&logo=amazon-ec2&logoColor=white"> ![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white) ![Gunicorn](https://img.shields.io/badge/gunicorn-%298729.svg?style=for-the-badge&logo=gunicorn&logoColor=white) ![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)

- **Project Management**
  - ![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white) ![Notion](https://img.shields.io/badge/Notion-%23ffffff.svg?style=for-the-badge&logo=notion&logoColor=black) ![Discord](https://img.shields.io/badge/Discord-%235865F2.svg?style=for-the-badge&logo=discord&logoColor=white)

---

## 📂 프로젝트 구조 (Directory Structure)
```
📦weniversity-server
┣ app/ # Django project root
┣ 📂.github
┃ ┣ 📂workflows
┃ ┃ ┣ 📜main.yaml
┣ 📂venv
┣ 📂weniversity
┃ ┣ 📜**init**.py
┃ ┣ 📜asgi.py
┃ ┣ 📜settings.py
┃ ┣ 📜urls.py
┃ ┣ 📜wsgi.py
┃ 📜.env
┃ 📜.gitignore
┃ 📜db.sqlite3
┃ 📜manage.py
┃ 📜README.md
┃ 📜requirements.txt
┣ 📂media
┃ ┣ 📂course
┃ ┣ 📂instructor_profiles
┃ ┣ 📂profiles
┃ ┣ 📂video
┣ 📂users
┃ ┣ 📂migrations
┃ ┃ ┣ 📜**init**.py
┃ ┣ 📂templates
┃ ┃ ┣ 📂emails
┃ ┃ ┃ ┣ 📜password_reset_form.html
┃ ┣ 📜**init**.py
┃ ┣ 📜admin.py
┃ ┣ 📜models.py
┃ ┣ 📜permissions.py
┃ ┣ 📜serializers.py
┃ ┣ 📜urls.py
┃ ┣ 📜views.py
┣ 📂courses
┃ ┣ 📂migrations
┃ ┃ ┣ 📜**init**.py
┃ ┣ 📜**init**.py
┃ ┣ 📜admin.py
┃ ┣ 📜filters.py
┃ ┣ 📜models.py
┃ ┣ 📜serializers.py
┃ ┣ 📜urls.py
┃ ┣ 📜views.py
```
## 🛠️ 개발

### 🔒 JWT 인증
- djangorestframework-simplejwt를 이용하여 사용자 인증을 진행

### 🔍 Filter 기반 검색
- django Filter 기반 다중 검색 기능 구현