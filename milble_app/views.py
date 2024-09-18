from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login  # 'login'을 'auth_login'으로 임포트
from .forms import SignupRequestForm
from .models import SignupRequest
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User  # User 모델을 임포트
from .forms import LoginForm  # 여기서 LoginForm을 임포트
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'index.html')

def signup_request_view(request):
    if request.method == 'POST':
        form = SignupRequestForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # 가입 요청 저장
            return redirect('signup_success')  # 성공 페이지로 리디렉션
    else:
        form = SignupRequestForm()
    return render(request, 'signup_request.html', {'form': form})

def signup_success(request):
    return render(request, 'signup_success.html')

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            id = form.cleaned_data['id']
            password = form.cleaned_data['password']
            
            try:
                user_request = SignupRequest.objects.get(id=id)
                if user_request.approved:
                    # 사용자 인증
                    user = authenticate(request, username=id, password=password)
                    if user is not None:
                        # 비밀번호가 정확한지 확인
                        if user.check_password(password):
                            auth_login(request, user)
                            return redirect('/')  # 성공 시 이동할 URL 이름으로 변경
                        else:
                            form.add_error(None, 'Invalid ID or password.')
                    else:
                        # 사용자 생성 필요
                        user = User(username=id)
                        user.set_password(password)
                        user.save()
                        # 로그인
                        auth_login(request, user)
                        return redirect('/')  # 성공 시 이동할 URL 이름으로 변경
                else:
                    form.add_error(None, 'Your account is not approved yet.')
            except SignupRequest.DoesNotExist:
                form.add_error(None, 'Invalid ID or password.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def profile_view(request):
    try:
        # 현재 로그인된 사용자 ID로 SignupRequest 객체를 가져옵니다.
        signup_request = SignupRequest.objects.get(id=request.user.username)
    except SignupRequest.DoesNotExist:
        signup_request = None

    context = {
        'user': request.user,
        'signup_request': signup_request
    }
    return render(request, 'profile.html', context)