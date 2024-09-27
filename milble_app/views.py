from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login  # 'login'을 'auth_login'으로 임포트
from .forms import SignupRequestForm
from .models import SignupRequest
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User  # User 모델을 임포트
from .forms import LoginForm  # 여기서 LoginForm을 임포트
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from .models import Post, Comment # Category 모델 임포트 추가
from django.shortcuts import get_object_or_404
from .forms import CommentForm, ReplyForm
from .models import CustomUser
from django.http import HttpResponseForbidden
from .models import Unit
from .forms import UnitForm
from .forms import UnitSearchForm, UnitJoinForm


from django.shortcuts import render
from .models import Unit, Post

def index(request):
    # 인기 게시물: 좋아요 또는 댓글 순으로 5개
    popular_posts = Post.objects.all().order_by('-views')[:5]

    # 사용자 로그인 확인 및 소속 부대의 게시물 가져오기
    user_unit_posts = None
    if request.user.is_authenticated and request.user.unit:
        user_unit = request.user.unit
        print(Post.objects.filter(unit=user_unit))
        # 우리부대 게시물: 좋아요 순으로 2개, 최신순으로 3개
        # 인기 게시물 2개
        popular_user_unit_posts = Post.objects.filter(unit=user_unit).order_by('-views')[:2]
        print(popular_user_unit_posts)



        # 최근 게시물에서 인기 게시물 제외
        recent_user_unit_posts = Post.objects.filter(unit=user_unit).exclude(id__in=popular_user_unit_posts.values_list('id', flat=True)).order_by('-created_at')[:3]

        user_unit_posts = {
            'popular': popular_user_unit_posts,
            'recent': recent_user_unit_posts
        }

    # 부대별 게시물 가져오기
    units = Unit.objects.all()
    unit_posts = {}
    for unit in units:
        unit_posts[unit] = Post.objects.filter(unit=unit).order_by('-created_at')[:5]  # 각 부대별 상위 5개 게시물

    return render(request, 'index.html', {
        'popular_posts': popular_posts,
        'user_unit_posts': user_unit_posts,
        'unit_posts': unit_posts  # 부대별 게시물 추가
    })



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
            
            # 사용자 인증
            user = authenticate(request, username=id, password=password)
            if user is not None:
                # 로그인
                auth_login(request, user)
                return redirect('/')  # 성공 시 이동할 URL 이름으로 변경
            else:
                form.add_error(None, 'Invalid ID or password.')
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})

@login_required
def profile_view(request):
    # 현재 로그인된 사용자 정보를 가져옵니다.
    user = request.user

    # CustomUser 모델의 필드를 사용하여 추가적인 정보가 필요한 경우 처리할 수 있습니다.
    # 예를 들어, unit 필드를 가져오거나 다른 정보를 사용할 수 있습니다.
    context = {
        'user': user,
        # 필요한 경우 CustomUser 모델의 필드에 대한 추가 정보도 여기에 포함할 수 있습니다.
        'unit': user.unit,
    }
    return render(request, 'profile.html', context)

#게시물 생성뷰
@login_required
def post_create(request):
    user = request.user  # 현재 로그인한 사용자
    
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False, user=user)  # user를 전달
            post.save()  # 게시물 저장
            return redirect('/')
    else:
        form = PostForm()

    return render(request, 'post_form.html', {'form': form})

def unit_posts_view(request, unit_name):
    # unit_name에 해당하는 부대 정보를 가져옵니다.
    unit = get_object_or_404(Unit, name=unit_name)
    
    # 해당 부대의 게시물들을 가져옵니다.
    posts = Post.objects.filter(unit=unit).order_by('-created_at')  # 최신순으로 정렬

    # 모든 부대 정보를 가져오되, 현재 부대(unit)를 제외합니다.
    units = Unit.objects.exclude(name=request.user.unit)
    
    return render(request, 'unit_posts.html', {
        'current_unit': unit,  # 현재 선택된 부대
        'posts': posts,
        'units': units,  # 부대 리스트
        'user': request.user  # 로그인 여부 및 유저 정보 확인
    })


def popular_posts_view(request):
    # 좋아요와 댓글 수를 기준으로 인기 게시물 정렬
    popular_posts = Post.objects.all().order_by('-likes', '-comments')  # 좋아요, 댓글 수 기준으로 정렬
    
    # 모든 부대 목록 가져오기
    units = Unit.objects.all()

    return render(request, 'popular_posts.html', {
        'posts': popular_posts,
        'units': units,  # 부대 목록 전달
    })


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()  # 해당 게시물에 달린 모든 댓글을 가져옴

    # 조회수 업데이트
    post.views += 1
    post.save()

    if request.method == "POST":
        custom_user = request.user  # 로그인된 사용자의 CustomUser 객체

        # 댓글 작성 처리
        if 'comment-submit' in request.POST:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.author = custom_user.username
                comment.unit = custom_user.unit
                comment.save()
                
                # Update the comment count on the post
                post.comments_count += 1  # Assuming you have a comments_count field in Post model
                post.save()
                return redirect('post_detail', post_id=post_id)

        # 대댓글 작성 처리
        elif 'reply-submit' in request.POST:
            reply_form = ReplyForm(request.POST)
            comment_id = request.POST.get('comment_id')
            comment = get_object_or_404(Comment, id=comment_id)

            if reply_form.is_valid():
                reply = reply_form.save(commit=False)
                reply.comment = comment
                reply.author = custom_user.username
                reply.unit = custom_user.unit
                reply.save()
                return redirect('post_detail', post_id=post_id)

    else:
        form = CommentForm()

    # 만든이 마스킹 처리
    author_masked = post.author[0] + '*' * (len(post.author) - 1)

    context = {
        'post': post,
        'author_masked': author_masked,
        'comments': comments,
        'form': form,
    }
    return render(request, 'post_detail.html', context)

#좋아요기능
def post_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user

    if user.is_authenticated:
        if user in post.liked_users.all():
            # 이미 좋아요를 누른 경우 -> 좋아요 취소
            post.liked_users.remove(user)
            post.likes -= 1
        else:
            # 좋아요를 누르지 않은 경우 -> 좋아요 추가
            post.liked_users.add(user)
            post.likes += 1
        post.save()

    return redirect('post_detail', post_id=post_id)

def unit_create_view(request):
    if request.method == 'POST':
        form = UnitForm(request.POST)
        if form.is_valid():
            # 부대 저장
            unit = form.save()
            
            # 생성한 부대에 자동으로 사용자 가입
            user = request.user
            user.unit = unit
            user.save()

            # 성공 시 리디렉션 (메인 페이지로 이동)
            return redirect('/')
    else:
        units = Unit.objects.all()
        form = UnitForm()

    return render(request, 'create_unit.html', {
        'form': form,
        'units': units
    })

#부대 가입
def join_unit_view(request):
    search_form = UnitSearchForm(request.GET or None)
    join_form = None
    unit = None

    if search_form.is_valid():
        query = search_form.cleaned_data['query']
        units = Unit.objects.filter(name__icontains=query)  # 부대명 검색

        # 부대 선택 후 질문 표시
        if 'unit_id' in request.GET:
            unit_id = request.GET.get('unit_id')
            unit = get_object_or_404(Unit, id=unit_id)
            join_form = UnitJoinForm(request.POST or None)

            if request.method == 'POST' and join_form.is_valid():
                # 답변 검증 로직
                if (unit.answer1 == join_form.cleaned_data['answer1'] and
                    unit.answer2 == join_form.cleaned_data['answer2'] and
                    unit.answer3 == join_form.cleaned_data['answer3']):
                    # 가입 처리 (유저와 부대 연결)
                    request.user.unit = unit
                    request.user.save()
                    return render(request, 'index')
                else:
                    join_form.add_error(None, '답변이 일치하지 않습니다.')
    else:
        units = None

    return render(request, 'join_unit.html', {
        'search_form': search_form,
        'join_form': join_form,
        'units': units,
        'selected_unit': unit
    })