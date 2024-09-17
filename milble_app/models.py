# models.py
from django.db import models
from django.contrib.auth.models import User

class SignupRequest(models.Model):
    id = models.CharField(max_length=150, unique=True, primary_key=True)  # 기본 키로 설정
    password = models.CharField(max_length=128)  # 비밀번호 (암호화된 상태로 저장)
    verification_image = models.ImageField(upload_to='verification_images/')  # 인증사진 업로드
    approved = models.BooleanField(default=False)  # 요청 승인 상태

    def __str__(self):
        return self.id
