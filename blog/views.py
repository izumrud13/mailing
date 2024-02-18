from pytils.translit import slugify

from blog.forms import BlogForm
from blog.models import Blog

from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin


class ArticleListView(LoginRequiredMixin, ListView):
    """Контроллер отображения страницы статей"""
    model = Blog

    def get_queryset(self, *args, **kwargs):
        """Отображение только опубликованных статей"""
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset


class ArticleDetailView(LoginRequiredMixin, DetailView):
    """Контроллер отображения отдельной статьи"""
    model = Blog

    def get_object(self, queryset=None):
        """Реализация счетчика просмотров"""
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class ArticleCreateView(LoginRequiredMixin, CreateView):
    """Контроллер создания статьи"""
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy('blog:articles')

    def form_valid(self, form):
        """Генерация slug к статье"""
        if form.is_valid():
            new_article = form.save()
            new_article.user = self.request.user
            new_article.slug = slugify(new_article.title)
            new_article.save()
        return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Контроллер редактирования статьи"""
    model = Blog
    form_class = BlogForm


    def test_func(self):
        user = self.request.user
        if user == self.get_object().user:
            return True
        return self.handle_no_permission()

    def form_valid(self, form):
        """Обновление slug"""
        if form.is_valid():
            new_article = form.save()
            new_article.slug = slugify(new_article.title)
            new_article.save()
        return super().form_valid(form)

    def get_success_url(self):
        """Редирект на статью"""
        return reverse('blog:view', args=[self.kwargs.get('slug')])


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Контроллер удаления статьи"""
    model = Blog
    success_url = reverse_lazy('blog:articles')

    def test_func(self):
        user = self.request.user
        if user == self.get_object().user:
            return True
        return self.handle_no_permission()
