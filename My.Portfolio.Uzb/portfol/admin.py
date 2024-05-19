from django.contrib import admin
from .models import Category, Site, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name',)


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'see', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'subtitle', 'body')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'site', 'email', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'email', 'body')