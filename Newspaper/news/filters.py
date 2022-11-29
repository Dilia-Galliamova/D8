import django_filters.widgets
from django_filters import FilterSet, CharFilter, DateFromToRangeFilter, DateFilter
from django_filters.widgets import DateRangeWidget

from .models import Post, Author


class PostFilter(FilterSet):
    author = CharFilter(
        field_name='author__user__username',
        lookup_expr='icontains',
        label='Автор'
    )
    create_time = DateFromToRangeFilter(widget=DateRangeWidget(attrs={'placeholder': 'ГГГГ.ММ.ДД'}), label='За период')
    title = CharFilter(field_name='title', lookup_expr='icontains', label='Заголовок')
    class Meta:
        model = Post
        fields = {'title'}
