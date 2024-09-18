# forms.py
from django import forms
from .models import SignupRequest
from django.contrib.auth.forms import AuthenticationForm

# forms.py
from django import forms
from .models import SignupRequest

class SignupRequestForm(forms.ModelForm):
    password2 = forms.CharField(widget=forms.PasswordInput(), label="Confirm Password")  # 비밀번호 확인 필드 추가

    class Meta:
        model = SignupRequest
        fields = ['id', 'password', 'password2', 'unit', 'verification_image']
        widgets = {
            'password': forms.PasswordInput(),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id'].label = "아이디"  # 라벨 한글로 설정
        self.fields['password'].label = "비밀번호"  # 라벨 한글로 설정
        self.fields['password2'].label = "비밀번호 확인"
        self.fields['verification_image'].label = "현역병 인증 사진"  # 라벨 한글로 설정
        self.fields['unit'].label = "부대 소속"  # 라벨 한글로 설정

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

    def clean_unit(self):
        unit = self.cleaned_data.get('unit')
        if not unit:
            raise forms.ValidationError("부대 소속은 필수 입력 사항입니다.")
        return unit



class LoginForm(forms.Form):
    id = forms.CharField(label='ID', max_length=150)
    password = forms.CharField(widget=forms.PasswordInput(), label='Password')

    def clean(self):
        cleaned_data = super().clean()
        id = cleaned_data.get('id')
        password = cleaned_data.get('password')

        # 커스텀 인증 로직을 사용할 것이므로, 추가적인 validation은 생략하거나 구현할 수 있습니다.
        return cleaned_data
