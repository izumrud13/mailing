from django import forms
from blog.models import Blog
from mailing.forms import StyleFormMixin


class BlogForm(StyleFormMixin, forms.ModelForm):
    """Форма для модели Blog"""

    class Meta:
        model = Blog
        fields = ('title', 'content', 'image', 'is_published')