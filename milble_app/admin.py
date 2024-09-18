# admin.py
from django.contrib import admin
from django.contrib.auth.models import User
from .models import SignupRequest

@admin.register(SignupRequest)
class SignupRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'approved', 'verification_image', 'unit')
    list_filter = ('approved', 'unit')
    search_fields = ('id', 'unit')

    actions = ['approve_requests']

    def approve_requests(self, request, queryset):
        for signup_request in queryset:
            if not signup_request.approved:
                # User 객체 생성
                user = User.objects.create(username=signup_request.id)
                user.set_password(signup_request.password)  # 비밀번호 암호화
                user.save()

                # 인증사진 처리 또는 추가 작업

                # 승인된 요청의 상태 업데이트
                signup_request.approved = True
                signup_request.save()

        self.message_user(request, "Selected requests have been approved.")
    
    approve_requests.short_description = "Approve selected requests"
