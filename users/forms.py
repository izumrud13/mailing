from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from mailing.forms import StyleFormMixin
from users.models import User


class RegisterForm(StyleFormMixin, UserCreationForm):
    """Форма для регистрации"""
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class UserForm(StyleFormMixin, UserChangeForm):
    """Форма для профиля пользователя"""
    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'avatar', 'country', 'phone')

    def __init__(self, *args, **kwargs):
        """Скрытие поля password"""
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()


class ListUserForm(StyleFormMixin, forms.ModelForm):
    """Форма модели User для списка"""

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'country')