# grepp-reservation-system

---
# 로컬 환경 구동 방법
### docker 설치 되었을 경우 (권장)
1. git repository clone
2. docker-compose 실행
```
$ docker-compose up -d
```
3. http://localhost:8000/frontend 접속
- 테스트용 admin 계정
  - email : admin@test.com
  - password : 1234

### docker 없을 경우
1. git repository clone
2. 로컬 postgresql 서버 설치 후 db 설정 
   1. `settings.py`에서 `DATABASES` configuration을 로컬 postgresql에 맞게 설정
   2. migration 실행
    ``` 
   $ python manage.py migrate
    ```
3. django 서버 실행
```commandline
$ python manage.py runserver
```
4. python manage.py shell로 admin user 생성
```
from users.models import User
User.objects.create_user(email={email}, password={password})
```
5. http://localhost:8000/frontend 접속

# 프로젝트 구성
## Frontend
- `Html` + `Javascript`로 구현
- `Chatgpt` 활용
- django의 `collectstatic` 활용
- http://localhost:8000/frontend 접속 시 확인 가능

## Backend 
- `Django` + `Django Rest Framework`로 구현
- Django의 `Token Authentication`으로 인증/인가 구현, 클라이언트 local storage에 token 저장하여 활용
- `ModelViewSet`과 `ModelSerializer`를 활용하여 코드 간소화
- docker-compose 빌드 시 최초 Dummy Data 추가될 수 있도록 `frontend/management/commands/data_initiation.py` 실행되도록 함


# API 구성
## User
- [POST] /api/register : 회원 가입 
  - request body
    ```
    {
        "name": "name",
        "email": "email@email.com",
        "password": "password"
    }
    ```
  - response
    ```
      {
         "id": 12,
         "name": "name",
         "email": "email@email.com",
         "token": "007286e6585132cee672ef2ec1409fbe3deec0ca"
      }
    ```
- [POST] /api/login/ : 회원 로그인
  - request body
      ```
      {
        "email": "email@email.com",
        "password": "password"
      }
      ```
  - response
    ```
    {
        "token": "007286e6585132cee672ef2ec1409fbe3deec0ca",
        "is_staff": false
    }
    ```

- [GET] /api/users/{int:user_id}/reservations : 해당 회원 예약 정보 조회
  - response
  - ```
    {
    "next": null,
    "previous": null,
    "count": 2,
    "results": [
        {
            "id": 91,
            "is_confirmed": false,
            "created_at": "2024-05-09T07:33:52.300825Z",
            "updated_at": "2024-05-09T07:33:52.300840Z"
        },
        {
            "id": 92,
            "is_confirmed": false,
            "created_at": "2024-05-09T07:33:54.477731Z",
            "updated_at": "2024-05-09T07:33:54.477745Z"
        }
      ]
    }
    ```

## Exam
- [POST] /api/exams/ : 시험 생성 (admin only)
  - request body
  - ```commandline
    {
    "title": "시험 제목",
    "description": "시험 설명",
    "start_time": "2024-05-09 10:00:00"
    }
    ```
  - response
  - ```commandline
    {
        "id": 31,
        "is_reserved": false,
        "is_confirmed": false,
        "title": "시험 제목",
        "description": "시험 설명",
        "duration": 2,
        "start_time": "2024-05-09T10:00:00Z",
        "reservation_count": 0,
        "capacity": 50000,
        "created_at": "2024-05-09T07:36:44.094442Z",
        "updated_at": "2024-05-09T07:36:44.094460Z"
    }
    ```
- [GET] /api/exams/ : 시험 목록 조회
  - response
  - ```commandline
     {
       "next": "http://localhost:8000/api/exams/?page=2",
       "previous": null,
       "count": 31,
       "results": [
           {
               "id": 31,
               "is_reserved": false,
               "is_confirmed": false,
               "title": "시험 제목",
               "description": "시험 설명",
               "duration": 2,
               "start_time": "2024-05-09T10:00:00Z",
               "reservation_count": 0,
               "capacity": 50000,
               "created_at": "2024-05-09T07:36:44.094442Z",
               "updated_at": "2024-05-09T07:36:44.094460Z"
           }, ...
       ]
     }
     ```

- [GET] /api/exams/{int:exam_id}/ : 시험 디테일 조회
    - response
    - ```commandline
       {
           "id": 1,
           "is_reserved": false,
           "is_confirmed": false,
           "title": "시험 0번",
           "description": "이 시험은 이러이러이러합니다",
           "duration": 2,
           "start_time": "2024-05-09T06:00:00Z",
           "reservation_count": 0,
           "capacity": 50000,
           "created_at": "2024-05-09T06:43:15.441734Z",
           "updated_at": "2024-05-09T06:43:15.441744Z"
       }

      ```
    

## Reservation
- [POST] /api/exams/{int:exam_id}/reservations/ : 해당 시험의 예약 생성 (token required)
  - response
  - ```commandline
    {
        "id": 93,
        "is_confirmed": false,
        "created_at": "2024-05-09T07:40:57.135489Z",
        "updated_at": "2024-05-09T07:40:57.135504Z"
    }
    ```

- [GET] /api/exams/{int:exam_id}/reservations/ : 해당 시험의 예약 목록 조회 (admin only)
  - response
  - ```commandline
    {
        "next": null,
        "previous": null,
        "count": 1,
        "results": [
            {
                "id": 93,
                "is_confirmed": false,
                "created_at": "2024-05-09T07:40:57.135489Z",
                "updated_at": "2024-05-09T07:40:57.135504Z"
            }
        ]
    }
    ```
- [PUT] /api/exams/{int:exam_id}/reservations/{int:reservation_id}/ : 유저의 예약 수정. 확정 되기 전까지만 가능.
- [DELETE] /api/exams/{int:exam_id}/reservations/{int:reservation_id}/ : 유저의 예약 삭제.
  - response : 없음 (status 204 no content)
- [PATCH] /api/exams/{int:exam_id}/reservations/{int:reservation_id}/ : 예약 확정 (admin only)
  - 
