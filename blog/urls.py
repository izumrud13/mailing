from django.urls import path
from django.views.decorators.cache import never_cache, cache_page

from blog.apps import BlogConfig
from blog.views import ArticleListView, ArticleCreateView, ArticleUpdateView, ArticleDeleteView, ArticleDetailView

app_name = BlogConfig.name

urlpatterns = [
    path('', ArticleListView.as_view(), name='articles'),
    path('create/', ArticleCreateView.as_view(), name='create'),
    path('update/<str:slug>/', ArticleUpdateView.as_view(), name='update'),
    path('delete/<str:slug>/', ArticleDeleteView.as_view(), name='delete'),
    path('articles/<str:slug>/', cache_page(60)(ArticleDetailView.as_view()), name='view'),
]