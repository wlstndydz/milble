# models.py
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    unit = models.CharField(max_length=255, blank=True)  # unit 필드 추가

class SignupRequest(models.Model):
    
    id = models.CharField(max_length=150, unique=True, primary_key=True)  # 기본 키로 설정
    password = models.CharField(max_length=128)  # 비밀번호 (암호화된 상태로 저장)
    verification_image = models.ImageField(upload_to='verification_images/')  # 인증사진 업로드
    approved = models.BooleanField(default=False)  # 요청 승인 상태
    unit = models.CharField(max_length=255)  # 드롭다운 메뉴 대신 문자열로 입력 가능

    def __str__(self):
        return self.id
    
    
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.CharField(max_length=100)  # 글쓴이
    unit = models.CharField(max_length=100)  # 부대 소속
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=100)  # 글쓴이
    unit = models.CharField(max_length=100)  # 부대 소속

    def __str__(self):
        return f'Comment on {self.post.title} by {self.author}'

class Reply(models.Model):
    comment = models.ForeignKey(Comment, related_name='replies', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=100)  # 글쓴이
    unit = models.CharField(max_length=100)  # 부대 소속

    def __str__(self):
        return f'Reply to {self.comment.id} by {self.author}'