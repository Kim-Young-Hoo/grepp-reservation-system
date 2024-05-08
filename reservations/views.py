from django.shortcuts import render

# Create your views here.
"""
TODO:
1. [PATCH] /reservations/{id}/confirm/{status} : 예약 확정. 어드민 only. race condition 고려
2. [POST] /reservations : 예약 생성. 로그인 필수.
3. [GET] /reservations : 예약 조회. 어드민 아니면 자기꺼만 조회, 어드민이면 전체 조회. 페이지네이션
4. [DELETE] /reservations : 예약 삭제(취소).
"""