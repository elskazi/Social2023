from django import forms

from django.contrib.auth.models import User  #Регистрация пользователей
from .models import Profile

# фома Login
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

# фома Регистрация пользователей
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')
    # проверка пароля и повтор пароля
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают!')
        return cd['password2']

    # Запрет пользователям использовать существующую электронную почту
    # def clean_email(self):
    #     data = self.cleaned_data['email']
    #     if User.objects.filter(email=data).exists():
    #         raise forms.ValidationError('Email already in use.')
    #     return data
    # Запрет пользователям использовать существующую электронную почту и менять на существующую
    def clean_email(self):
        data = self.cleaned_data['email']
        qs = User.objects.exclude(id=self.instance.id) \
        .filter(email=data)
        if qs.exists():
            raise forms.ValidationError(' Email already in use.')
        return data

# для увеленчения пойлей регитрации , берем 2 формы, стандартного Юзера из Джанго, и Профайла то что сами сделали в Модели
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['date_of_birth', 'photo']