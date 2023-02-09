from django.contrib import admin

from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "created_at", "views")
    list_display_links = ("id", "title")
    search_fields = ("title", "text")
    readonly_fields = ("views",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "post", "created_at")
    search_fields = ("post", "text")
