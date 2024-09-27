# forms.py
from django import forms
from .models import SignupRequest
from django.contrib.auth.forms import AuthenticationForm
from .models import Post, Comment, Reply, Unit

class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ['name', 'answer1', 'answer2', 'answer3']
        labels = {
            'name': '전체 부대명',
            'answer1': '질문1에 대한 답',
            'answer2': '질문2에 대한 답',
            'answer3': '질문3에 대한 답',
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': '예) 1사단 11여단 1대대 1중대'}),
            'answer1': forms.TextInput(attrs={'placeholder': '예) 22생활관'}),
            'answer2': forms.TextInput(attrs={'placeholder': '예) 홍길동'}),
            'answer3': forms.TextInput(attrs={'placeholder': '예) 12대'}),
        }
        
class SignupRequestForm(forms.ModelForm):
    password2 = forms.CharField(widget=forms.PasswordInput(), label="Confirm Password")  # 비밀번호 확인 필드 추가

    class Meta:
        model = SignupRequest
        fields = ['id', 'password', 'password2', 'verification_image']
        widgets = {
            'password': forms.PasswordInput(),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id'].label = "아이디"  # 라벨 한글로 설정
        self.fields['password'].label = "비밀번호"  # 라벨 한글로 설정
        self.fields['password2'].label = "비밀번호 확인"
        self.fields['verification_image'].label = "현역병 인증 사진"  # 라벨 한글로 설정

    def clean_id(self):
        id = self.cleaned_data.get('id')
        if SignupRequest.objects.filter(id=id).exists():
            raise forms.ValidationError("This ID is already taken.")
        return id

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password and password2 and password != password2:
            raise forms.ValidationError("두 비밀번호가 일치하지 않습니다.")
        
        return cleaned_data


class LoginForm(forms.Form):
    id = forms.CharField(label='ID', max_length=150)
    password = forms.CharField(widget=forms.PasswordInput(), label='Password')

    def clean(self):
        cleaned_data = super().clean()
        id = cleaned_data.get('id')
        password = cleaned_data.get('password')

        # 커스텀 인증 로직을 사용할 것이므로, 추가적인 validation은 생략하거나 구현할 수 있습니다.
        return cleaned_data
    
class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'content']  # unit과 author 필드는 제외

    def save(self, commit=True, user=None):
        post = super().save(commit=False)  # 게시물 객체 생성

        if user:
            post.author = user.username  # 현재 로그인한 사용자 이름 설정
            post.unit = user.unit  # 현재 로그인한 사용자의 부대 정보 설정
        
        if commit:
            post.save()  # 게시물 저장
        return post
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']  # content 필드만 폼에 포함
        
        
class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content']
        
class UnitSearchForm(forms.Form):
    query = forms.CharField(label='부대 검색', max_length=100, 
                            widget=forms.TextInput(attrs={'placeholder': '부대명 검색'}))

class UnitJoinForm(forms.Form):
    answer1 = forms.CharField(label='질문 1', max_length=255)
    answer2 = forms.CharField(label='질문 2', max_length=255)
    answer3 = forms.CharField(label='질문 3', max_length=255)