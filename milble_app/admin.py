# admin.py
from django.contrib import admin
from django.contrib.auth.models import User
from .models import CustomUser, SignupRequest
from .models import Post, Comment, Reply
from .models import Unit

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username','is_staff', 'unit')
    search_fields = ('username', 'unit')

@admin.register(SignupRequest)
class SignupRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'approved', 'verification_image')
    list_filter = ('approved',)
    search_fields = ('id',)

    actions = ['approve_requests']

    def approve_requests(self, request, queryset):
        for signup_request in queryset:
            if signup_request.approved:  # 체크박스가 선택된 경우
                # CustomUser 객체 생성
                user = CustomUser(
                    username=signup_request.id,
                )
                user.set_password(signup_request.password)  # 비밀번호 암호화
                user.save()

                # 인증사진 처리 또는 추가 작업
                # 예: signup_request.verification_image.save()

                signup_request.delete()  # SignupRequest 객체 삭제

        self.message_user(request, "Selected requests have been approved and deleted.")
    
    approve_requests.short_description = "Approve selected requests"
    

admin.site.register(Unit)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Reply)