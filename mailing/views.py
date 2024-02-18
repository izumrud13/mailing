from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
import random
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, TemplateView, CreateView, UpdateView, DeleteView, DetailView

from blog.models import Blog
from mailing.forms import ClientForm, MessageForm, MailingForm
from mailing.models import Client, Message, Mailing, Log


class HomeTemplateView(TemplateView):
    """Контроллер главной страницы"""
    template_name = 'mailing/index.html'

    def get_context_data(self, *args, **kwargs):
        """Вывод информации на главную страницу"""
        context_data = super().get_context_data(*args, **kwargs)
        clients_count = len(Client.objects.filter(user=self.request.user.pk))
        mailing_count = len(Mailing.objects.filter(user=self.request.user.pk))
        active_mailing = len(Mailing.objects.filter(user=self.request.user.pk, status='created'))
        blog_list = [blog for blog in Blog.objects.all()]
        random_blog_list = random.sample(blog_list, 3)
        context_data['clients_count'] = clients_count
        context_data['mailing_count'] = mailing_count
        context_data['active_mailing'] = active_mailing
        context_data['random_blog_list'] = random_blog_list
        return context_data


class ClientCreateView(LoginRequiredMixin, CreateView):
    """Контроллер страницы добавления нового клиента"""
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:home_page')

    def form_valid(self, form):
        """Добавление пользователя к клиенту"""
        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class ClientListView(LoginRequiredMixin, ListView):
    """Контроллер страницы клиентов"""
    model = Client

    def get_queryset(self):
        """Вывод клиентов пользователя"""
        return super().get_queryset().filter(user=self.request.user)


class ClientUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Контроллер страницы редактирования клиентов"""
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')

    def test_func(self):
        user = self.request.user
        if user == self.get_object().user:
            return True
        return self.handle_no_permission()


class ClientDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Контроллер удаления клиента"""
    model = Client
    success_url = reverse_lazy('mailing:client_list')

    def test_func(self):
        user = self.request.user
        if user == self.get_object().user:
            return True
        return self.handle_no_permission()


class MessageCreateView(LoginRequiredMixin, CreateView):
    """Контроллер страницы добавления нового сообщения"""
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:message_list')

    def form_valid(self, form):
        """Добавление пользователя к сообщению"""
        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Контроллер страницы редактирования сообщения"""
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:message_list')

    def test_func(self):
        user = self.request.user
        if user == self.get_object().user:
            return True
        return self.handle_no_permission()


class MessageDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Контроллер страницы удаления сообщения"""
    model = Message
    success_url = reverse_lazy('mailing:home_page')

    def test_func(self):
        user = self.request.user
        if user == self.get_object().user:
            return True
        return self.handle_no_permission()


class MessageListView(LoginRequiredMixin, ListView):
    """Контроллер страницы сообщений"""
    model = Message

    def get_queryset(self):
        """Вывод сообщений пользователя"""
        return super().get_queryset().filter(user=self.request.user)


class MailingCreateView(LoginRequiredMixin, CreateView):
    """Контроллер страницы добавления новой рассылки"""
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:home_page')

    def form_valid(self, form):
        """Добавление пользователя к рассылке"""
        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Контроллер страницы редактирования рассылки"""
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')

    def test_func(self):
        user = self.request.user
        if user == self.get_object().user:
            return True
        return self.handle_no_permission()


class MailingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Контроллер страницы удаления рассылки"""
    model = Mailing
    success_url = reverse_lazy('mailing:mailing_list')

    def test_func(self):
        user = self.request.user
        if user == self.get_object().user:
            return True
        return self.handle_no_permission()


class MailingListView(LoginRequiredMixin, ListView):
    """Контроллер страницы рассылок"""
    model = Mailing

    def get_queryset(self):
        """Вывод рассылок пользователя либо всех рассылок для модератора"""
        if self.request.user.has_perm('mailing.view_mailing'):
            return super().get_queryset()
        return super().get_queryset().filter(user=self.request.user)


def status_mailing(request, pk):
    """Контроллер смены статуса рассылки"""
    mailing = Mailing.objects.get(pk=pk)
    if request.user == mailing.user or request.user.has_perm('mailing.set_status'):
        if mailing.status == 'created':
            mailing.status = 'completed'
            mailing.save()
        elif mailing.status == 'completed':
            mailing.status = 'created'
            mailing.save()
    return redirect(reverse('mailing:mailing_list'))


class LogListView(LoginRequiredMixin, ListView):
    """Контроллер страницы логов"""
    model = Log

    def get_queryset(self):
        """Вывод сообщений пользователя"""
        return super().get_queryset().filter(user=self.request.user)


class LogDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """Контроллер страницы лога"""
    model = Log

    def test_func(self):
        user = self.request.user
        if user == self.get_object().user:
            return True
        return self.handle_no_permission()


class LogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Контроллер удаления лога"""
    model = Log
    success_url = reverse_lazy('mailing:log_list')

    def test_func(self):
        user = self.request.user
        if user == self.get_object().user:
            return True
        return self.handle_no_permission()
