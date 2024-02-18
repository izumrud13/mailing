import random
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail

from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, ListView
from django.shortcuts import redirect
from config.settings import EMAIL_HOST_USER
from mailing.models import Message
from mailing.services import send_mailing
from users.forms import RegisterForm, UserForm, ListUserForm
from users.models import User
from django.contrib.messages.views import SuccessMessageMixin


class LoginUserView(LoginView):
    """Контроллер страницы входа"""
    template_name = 'users/login.html'


class LogoutUserView(LogoutView):
    """Контроллер выхода из аккаунта"""
    pass


class RegisterUserView(SuccessMessageMixin, CreateView):
    """Контроллер страницы регистрации"""
    model = User
    form_class = RegisterForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/register.html'

    def get_success_message(self, cleaned_data):
        """Сообщение на страницу входа"""
        return 'Вам на почту отправлено письмо, для прохождения верификации перейдите по ссылку в письме'

    def form_valid(self, form):
        """Верификация по ссылке через почту"""
        new_user = form.save()
        code = ''.join(random.sample('0123456789', 5))
        new_user.verify_code = code
        new_user.is_active = False
        send_mail(
            'Верификация',
            f'Перейдите по ссылке для верификации: http://127.0.0.1:8000/users/verification/{code}',
            EMAIL_HOST_USER,
            [new_user.email]
        )
        return super().form_valid(form)


def verification(request, code):
    """Контроллер подтверждения верификации"""
    user = User.objects.get(verify_code=code)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))


class UserUpdateView(UpdateView):
    """Контроллер страницы редактирования профиля"""
    model = User
    form_class = UserForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        """Отключение необходимости получения pk"""
        return self.request.user


def generate_password(request):
    """Контроллер смены пароля и отправка нового сгенерированного пароля на почту"""
    new_password = User.objects.make_random_password()
    request.user.set_password(new_password)
    request.user.save()
    message = Message.objects.create(subject='Смена пароля', body=f'Ваш новый пароль для авторизации: {new_password}',
                                     user=User.objects.get(pk=request.user.pk))
    send_mailing([request.user.email], message)
    messages.success(request, 'Вам на почту отправлено письмо с новым паролем для вашего аккаунта')
    return redirect(reverse('users:login'))


class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """Контроллер страницы списка пользователей"""
    model = User
    form_class = ListUserForm
    permission_required = 'users.view_user'


@permission_required('users.set_is_active')
def status_user(request, pk):
    """Контроллер смены статуса пользователя"""
    user = User.objects.get(pk=pk)
    if not user.is_superuser:
        if user.is_active is True:
            user.is_active = False
            user.save()
        elif user.is_active is False:
            user.is_active = True
            user.save()
        return redirect(reverse('users:user_list'))