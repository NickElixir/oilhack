from django import forms

class RegisterForm(forms.Form):
    username = forms.CharField(label='Логин:', max_length=100, required=True)
    first_name = forms.CharField(label='Имя:', max_length=100, required=True)
    last_name = forms.CharField(label='Фамилия:', max_length=100, required=True)
    password = forms.CharField(label='Пароль:', max_length=100, required=True, widget=forms.PasswordInput)
    password2 = forms.CharField(label='Пароль снова:', max_length=100, required=True, widget=forms.PasswordInput)


class LoginForm(forms.Form):
    username = forms.CharField(label='Логин:', max_length=100, required=True)
    password = forms.CharField(label='Пароль:', max_length=100, required=True, widget=forms.PasswordInput)
