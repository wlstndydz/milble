# forms.py
from django import forms
from .models import SignupRequest
from django.contrib.auth.forms import AuthenticationForm

class SignupRequestForm(forms.ModelForm):
    class Meta:
        model = SignupRequest
        fields = ['id', 'password', 'verification_image']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean_id(self):
        id = self.cleaned_data.get('id')
        if SignupRequest.objects.filter(id=id).exists():
            raise forms.ValidationError("This ID is already taken.")
        return id


from django import forms
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(forms.Form):
    id = forms.CharField(label='ID', max_length=150)
    password = forms.CharField(widget=forms.PasswordInput(), label='Password')

    def clean(self):
        cleaned_data = super().clean()
        id = cleaned_data.get('id')
        password = cleaned_data.get('password')

        # 커스텀 인증 로직을 사용할 것이므로, 추가적인 validation은 생략하거나 구현할 수 있습니다.
        return cleaned_data
