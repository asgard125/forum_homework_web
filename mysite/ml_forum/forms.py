from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from captcha.fields import CaptchaField
from .models import *


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label="Логин", widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label="Почта", widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label="Повторите пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    captcha = CaptchaField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label="Логин", widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    captcha = CaptchaField()


class AddTopicForm(forms.Form):
    name = forms.CharField(label="Название:", max_length=30,  widget=forms.TextInput(attrs={'class': 'form-input'}))
    description = forms.CharField(label="Описание:", max_length=50, widget=forms.TextInput(attrs={'class': 'form-input'}))
    post = forms.CharField(label="Ваш пост:", widget=forms.Textarea(attrs={'cols': 100, 'rows': 10}))
    captcha = CaptchaField()


class EditProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = UserProfile
        fields = ['name', 'surname', 'biography', 'photo', 'email', 'github', 'telegram', 'is_public']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'surname': forms.TextInput(attrs={'class': 'form-input'}),
            'biography': forms.Textarea(attrs={'cols': 100, 'rows': 10}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'github': forms.TextInput(attrs={'class': 'form-input'}),
            'telegram': forms.TextInput(attrs={'class': 'form-input'}),
        }

    def save(self):
        profile = super(EditProfileForm, self).save(commit=False)
        if profile.telegram != '':
            profile.telegram = "https://t.me/" + profile.telegram.split('/')[-1]
        if profile.github != '':
            profile.github= "https://github.com/" + profile.github.split('/')[-1]
        profile.save()
        return profile






# class EditProfileForm(forms.Form):
#     name = forms.CharField(label="Имя", max_length=25,  widget=forms.TextInput(attrs={'class': 'form-input'}), required=False)
#     surname = forms.CharField(label="Фамилия", max_length=25, widget=forms.TextInput(attrs={'class': 'form-input'}), required=False)
#     biography = forms.CharField(label="О себе", widget=forms.Textarea(attrs={'cols': 100, 'rows': 10}), required=False)
#     email = forms.EmailField(label="Почта:", widget=forms.EmailInput(attrs={'class': 'form-input'}), required=False)
#     photo = forms.ImageField(label="Фото профиля", required=False)
#     github = forms.CharField(label="Github", max_length=100, widget=forms.TextInput(attrs={'class': 'form-input'}), required=False)
#     telegram = forms.CharField(label="Telegram", max_length=100, widget=forms.TextInput(attrs={'class': 'form-input'}), required=False)
#     is_public = forms.BooleanField(label="Публичный профиль", required=False)


class VerifyProfileForm(forms.Form):
    code = forms.IntegerField(label="На почту был выслан код подтверждения")