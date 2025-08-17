# Weniversity Server 🎓

**Weniversity Server**는 온라인 교육 플랫폼 **Weniversity**의 백엔드 서버입니다.  
Django + Django REST Framework(DRF)를 기반으로 구축되었으며, 강의 콘텐츠 관리, 사용자 인증, 수강 관리 등 **교육 서비스 전반의 API**를 제공합니다.

---

## 🚀 주요 기능 (Features)

### 사용자 관리

- 회원가입, 로그인(JWT)
- 권한/역할(Role) 기반 접근 제어

### 강의/커리큘럼 관리

- 코스/챕터/비디오 3depth의 구조로 구성된 강의 생성 및 수정
- 카테고리별, 레벨별, 유형별, 가격별 강의 분류 관리 및 수강 신청 기능
- 강의 목록 조회 및 다중 검색 기능

### 미션 평가 시스템

- (추가예정)

### 교강사 관리

- 교강사 코드 구분 관리
- 교강사별 담당 과목 매칭 관리

### \*교육 컨텐츠(동영상) 관리

- 강의별 세부 수업(Lesson) 관리
- 강의별 중간/기말 미션 관리
- 수강 신청 및 이력 관리

### CI/CD

- Github Actions 기반 CI/CD (추가 가능)

---

## 🚀 시작하기

### 1) 요구사항

- Python 3.10+ (권장)
- 가상환경 사용 권장(venv/conda/poetry 등)
- SQLite는 기본 동작, 운영은 별도 RDB 권장

### 2) 설치

1. 클론

```
git clone https://github.com/nanna0/weniversity-server.git
cd weniversity-server
```

2. 가상환경 생성/활성화 (예: venv)

```
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

3. 패키지 설치

```
pip install --upgrade pip
pip install -r requirements.txt
```

### 3) 환경변수

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

### 4) DB 마이그레이션/관리자 생성/개발 서버

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

### 📋 객관식 & 주관식 문제

- 추가 예정

### 🎥 강의 영상

- 추가 예정

## 개발일정(WBS)

```mermaid
gantt
    dateFormat  YYYY-MM-DD
    title       weniversity 프로젝트 WBS
    excludes    weekends

    section 프로젝트 준비 (나영)
    프로젝트 킥오프 미팅                     :2025-07-29 1d
    요구사항 분석 및 기술 스택 결정            :2025-07-29, 1d
    ERD 작성                             :2025-07-29, 1d

    section 배포 환경 설정 (나영)
    main.yaml 파일 작성                   :2025-07-31, 1d
    github CI/CD action 설정             :2025-07-31, 1d
    배포 서버 ubuntu 설정                  :2025-07-31, 1d
    nginx, gunicorn 설정                 :2025-07-31, 1d


    section 모델 작성 (나영)
    users 모델 작성                       :2025-07-30, 1d
    Intructor 모델 작성                   :2025-08-06, 1d
    courses 모델 작성                     :2025-08-07, 1d
    chapter 모델 작성                     :2025-08-07, 1d
    videos 모델 작성                      :2025-08-07, 1d
    Enrollment 모델 작성                  :2025-08-12, 1d
    missions 모델 작성                    :


    section user 앱 (나영)
    회원가입 기능 구현                       :2025-08-01, 1d
    로그인/로그아웃 기능 구현                  :2025-08-01, 1d
    사용자 프로필 CRUD 구현                  :2025-08-02, 1d
    프로필 이미지 랜덤 설정 구현                :2025-08-02, 1d
    권한 설정 구현                          :2025-08-03, 1d
    비밀번호 변경 이메일 전송 로직 구현          :2025-08-03, 1d
    users 앱 단위 테스트                    :2025-08-04, 1d

    section courses 앱 (나영)
    과목 CRUD 기능 어드민 구현                     :2025-08-05, 1d
    과목 필터 검색 및 페이지네이션 구현                :2025-08-05, 1d
    강사 CRUD 기능 어드민 구현                     :2025-08-06, 1d
    강사 프로필 등록, course 연결                  :2025-08-07, 1d
    과목 필터 다중검색 구현                        :2025-08-08, 1d
    과목 가격별 범위 구현                          :2025-08-11, 1d
    과목 조회 기능 구현                           :2025-08-12, 1d
    chapter, video 단위 구현                    :2025-08-12, 1d
    courses 앱 단위 테스트                       :2025-08-13, 1d

    section enrollment(my-course) 앱 (나영)
    수강신청 구현                                :2025-08-13, 1d
    내가 신청한 과목 조회, 수강률 구현                :2024-08-13, 1d
    강의 좋아요, 내가 좋아한 강의 리스트 구현          :2025-08-14, 1d
    내가 신청한 강의 필터 검색 구현                  :2025-08-14, 1d
    enrollment 앱 단위 테스트                    :2024-08-14, 1d


    section missions 앱 (여밈)


    section videos 앱 (여밈)


    section 통합 및 테스트
    앱 간 통합 작업                         :2025-08-15, 1d
    통합 테스트                             :2025-08-15, 1d
    사용자 시나리오 기반 전체 테스트             :2025-08-16, 1d
    성능 테스트                             :2025-08-16, 1d

    section 마무리
    발견된 버그 수정                         :2025-08-16, 1d
    최종 점검                              :2025-08-16, 1d

    section 프로젝트 마무리
    최종 테스트 및 QA                       :2025-08-17, 1d
    프로젝트 문서화 완료                      :2025-08-17, 1d
    최종 발표 자료 준비                      :2025-08-17, 1d
```
<br/>

## 데이터베이스 모델링 (ERD)
```mermaid
erDiagram
  %% Auto-generated from db.sqlite3 (Mermaid-friendly)
  auth_group {
    int id PK
    string name
  }
  auth_group_permissions {
    int id PK
    int group_id
    int permission_id
  }
  auth_permission {
    int id PK
    int content_type_id
    string codename
    string name
  }
  courses_chapter {
    int chapter_id PK
    string title
    datetime created_at
    int course_id
    int order_index   %% unsigned
  }
  courses_course {
    int course_id PK
    string title
    string category
    string type
    string level
    int price
    text description
    datetime course_time
    datetime course_duedate
    string discord_url
    datetime created_at
    bool is_active
    int order_index   %% unsigned
    string price_type
    int code          %% unsigned
    string course_image
  }
  courses_courselike {
    int id PK
    datetime created_at
    int course_id
    int user_id
  }
  courses_enrollment {
    int id PK
    string status
    datetime enrolled_at
    datetime expired_at
    decimal progress
    int course_id
    int user_id
  }
  courses_instructor {
    int instructor_id PK
    string name
    int code
    datetime created_at
    string affiliation
    int course_id
    string profile_image
    string english_name
  }
  courses_video {
    int video_id PK
    string title
    int duration
    int chapter_id
    int course_id
    int order_index   %% unsigned
    string video_file
  }
  django_admin_log {
    int id PK
    text object_id
    string object_repr
    smallint action_flag  %% unsigned
    text change_message
    int content_type_id
    int user_id
    datetime action_time
  }
  django_content_type {
    int id PK
    string app_label
    string model
  }
  django_migrations {
    int id PK
    string app
    string name
    datetime applied
  }
  django_session {
    string session_key PK
    text session_data
    datetime expire_date
  }
  token_blacklist_blacklistedtoken {
    int id PK
    datetime blacklisted_at
    bigint token_id
  }
  token_blacklist_outstandingtoken {
    int id PK
    string jti
    text token
    datetime created_at
    datetime expires_at
    int user_id
  }
  users_user {
    datetime last_login
    bool is_superuser
    string first_name
    string last_name
    bool is_staff
    datetime date_joined
    int id PK
    string email
    string password
    string name
    string gender
    date birth_date
    string role
    bool is_active
    datetime created_at
    datetime updated_at
    string profile_image
  }
  users_user_course {
    int id PK
    int user_id
    int course_id
  }
  users_user_groups {
    int id PK
    int user_id
    int group_id
  }
  users_user_user_permissions {
    int id PK
    int user_id
    int permission_id
  }

  auth_permission ||--|{ auth_group_permissions : "permission_id -> id"
  auth_group ||--|{ auth_group_permissions : "group_id -> id"
  django_content_type ||--|{ auth_permission : "content_type_id -> id"
  courses_course ||--|{ courses_chapter : "course_id -> course_id"
  users_user ||--|{ courses_courselike : "user_id -> id"
  courses_course ||--|{ courses_courselike : "course_id -> course_id"
  users_user ||--|{ courses_enrollment : "user_id -> id"
  courses_course ||--|{ courses_enrollment : "course_id -> course_id"
  courses_course ||--|{ courses_instructor : "course_id -> course_id"
  courses_course ||--|{ courses_video : "course_id -> course_id"
  courses_chapter ||--|{ courses_video : "chapter_id -> chapter_id"
  users_user ||--|{ django_admin_log : "user_id -> id"
  django_content_type ||--o{ django_admin_log : "content_type_id -> id"
  token_blacklist_outstandingtoken ||--|{ token_blacklist_blacklistedtoken : "token_id -> id"
  users_user ||--o{ token_blacklist_outstandingtoken : "user_id -> id"
  courses_course ||--|{ users_user_course : "course_id -> course_id"
  users_user ||--|{ users_user_course : "user_id -> id"
  auth_group ||--|{ users_user_groups : "group_id -> id"
  users_user ||--|{ users_user_groups : "user_id -> id"
  auth_permission ||--|{ users_user_user_permissions : "permission_id -> id"
  users_user ||--|{ users_user_user_permissions : "user_id -> id"

```

## 🌟 메인 기능
- **👤 사용자 관리**:
  - JWT와 리프레시 토큰을 통해 안전하고 효율적인 사용자 인증 및 권한 관리 기능을 구현했습니다.
  - 회원가입, 로그인, 로그아웃, 비밀번호 찾기 이메일 발송 기능을 제공합니다.
  - 사용자 역할은 관리자, 수강생으로 구분됩니다.

- **📚 강의 관리**:
  - 코스, 챕터, 비디오 3depth로 강의를 관리합니다.
  - 강의 유형별, 레벨별, 가격별, 분야별 필터 다중 검색 기능을 지원합니다.
  - 수강신청 및 수강 기간을 관리하며 내가 수강중인 강의 역시 유형별, 가격별로 필터 다중 검색을 지원합니다.
  - 강의 좋아요 기능과 내가 좋아요한 강의를 따로 조회할 수 있습니다.

- **🧑🏻‍🏫 강사 관리**:
  - 관리자가 강사 프로필을 등록/수정/삭제/조회 관리할 수 있습니다.

- **🎥 동영상 학습 시스템**:
  - 

- **📈 학습 진행 관리**:
  - 사용자는 자신의 학습 진행 상황을 확인하고, 동영상 시청 기록을 관리할 수 있습니다.

- **🔒 권한 관리**:
  - 관리자와 사용자 역할에 따른 권한을 설정하고 관리할 수 있습니다.

- **📝 미션 평가 시스템**:
  - 

## ✅ API 명세서

### user

| Description | HTTP Method | URL Pattern Endpoint | Authentication | note |
| --- | --- | --- | --- | --- |
| 회원가입 | `POST` | `/api/users/register/` |  |  |
| 로그인(JWT) | `POST` | `/api/users/login/` |  | refresh token |
| 토큰리프레쉬 | `POST` | `/api/users/refresh/` | **✅** | refresh token |
| 로그아웃 | `POST` | **`/api/users/logout/`** | **✅** |  |
| 마이페이지(프로필사진) 조회/변경 | `GET`/ `PUT` | `/api/users/mypage/` | **✅** |  |
| 비밀번호 변경 | `PATCH` | `/api/users/mypage/change-password/` | **✅** |  |
| 비밀번호 변경 이메일 발송 | `POST` | `api/password-reset/` | **✅** |  |
| 내가 좋아요한 코스 리스트 | `GET` | `api/users/mypage/likes/` | **✅** |  |

### 강의/영상

| Description | HTTP Method | URL Pattern Endpoint | Authentication | note |
| --- | --- | --- | --- | --- |
| 강의 목록 | `GET` | `/api/courses/` |  |  |
| 강의 상세 | `GET` | `/api/courses/<id>/` |  |  |
| 강의 필터 | `GET` | `/api/courses/?` |  |  |
| 강의 좋아요 | `POST` | `/api/courses/int:course_id/like/` | **✅** |  |
| 강의 좋아요 취소 | `DELETE` | `/api/courses/int:course_id/like/` | **✅** |  |

### 수강 등록/진도

| Description | HTTP Method | URL Pattern Endpoint | Authentication | note |
| --- | --- | --- | --- | --- |
| 내 수강 강의 | `GET` | `/api/my-courses/` | **✅** |  |
| 수강 신청 | `POST` | `/api/courses/enroll/<int:course_id/>` | **✅** |  |
| 내 수강 강의 필터 | `GET` | `/api/my-courses/?` | **✅** |  |


## 프로젝트 회고
### 최나영 
```
구현해야 할 내용이 방대하여 막막했으나, 할 수 있는것과 해야 할 것을 구분하는 과정에서 팀원들과 원활한 소통으로 순조롭게 방향을 정할 수 있어서 감사했습니다.

부족한 실력이지만 반복적인 구현과 해보지 않은것에 대한 도전을 통해 나날이 성장함을 느꼈습니다.
가장 인상깊었던 작업은 사용자 인증 관리를 통해 JWT 인증 시스템을 구현하면서 Django REST Framework의 장점을 크게 느꼈고, permission 구현으로 권한 관리를 적용하며 이후 다시 프로젝트를 구성할 때 어떤식으로 접근하면 좋을지 감을 찾을 수 있었습니다. 

또 실제 서비스를 구현하기 위해 어떻게 앱 구조를 효율적으로 구성해야 하는가 고민을 많이 하였는데 완벽하진 않지만 다시 돌아보니 아쉬운 부분과 개선점이 명확히 보일 정도로 구조적인 측면에서 크게 성장했음을 느꼈습니다.

이번 프로젝트를 통해 성장할 수 있었음에 감사하며, 앞으로 마주할 다양한 경험과 성장 또한 기대됩니다.
개발은 참 재밌습니다. 부족한 실력에 위축감이 들 때도 있지만 시간이 해결해줄 것이라 긍정적으로 생각하며 다가가면 너무나 재밌는 분야입니다.
다시 교육계로 돌아가 앞으로 만날 교육생들에게 더 의미있고 유익한 교육을 제공할 수 있을것이라 기대됩니다. 

임신 기간동안 만삭이 다 될 때까지 대부분의 일상을 함께한 모두의 연구소 백엔드 과정, 성장을 위한 발걸음에 동행할 수 있어서 감사했습니다.
```
