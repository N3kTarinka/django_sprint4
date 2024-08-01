from django.contrib import admin

from blog.models import Category, Comment, Location, Post
from .constants import REPRESENTATION_LENGTH

admin.site.empty_value_display = 'Не задано'


class BaseAdmin(admin.ModelAdmin):
    list_per_page = REPRESENTATION_LENGTH


@admin.register(Category)
class CategoryAdmin(BaseAdmin):
    list_display = ('title', 'slug', 'is_published')
    list_editable = ('slug', 'is_published')
    list_display_links = ('title',)


@admin.register(Location)
class LocationAdmin(BaseAdmin):
    list_display = ('name', 'is_published')
    list_editable = ('is_published',)
    list_display_links = ('name',)


@admin.register(Post)
class PostAdmin(BaseAdmin):
    list_display = ('title', 'author', 'category',
                    'location', 'pub_date', 'is_published')
    list_editable = ('is_published',)
    search_fields = ('title', 'author', 'location', 'category')
    list_filter = ('is_published', 'author', 'location',
                   'category', 'pub_date')
    list_display_links = ('title',)


@admin.register(Comment)
class CommentAdmin(BaseAdmin):
    list_display = ('text', 'post', 'author', 'created_at')
    list_filter = ('post', 'author', 'created_at')
    search_fields = ('text', 'author')
