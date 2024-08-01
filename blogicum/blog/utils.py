from django.core.paginator import Paginator
from django.db.models import Count
from django.utils import timezone

from .models import Post


def get_published_posts():
    return Post.objects.select_related(
        'author',
        'category'
    ).filter(pub_date__lte=timezone.now(), is_published=True,
             category__is_published=True
             ).annotate(comment_count=Count('comments')).order_by('-pub_date')


def paginate_queryset(request, queryset, representation_length):
    paginator = Paginator(queryset, representation_length)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)
