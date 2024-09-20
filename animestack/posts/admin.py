from django.contrib import admin

from posts.models import Group, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("pk", "author", "text", "pub_date", "group")
    list_filter = ("pub_date",)
    list_editable = ("group",)
    search_fields = ("text",)
    empty_value_display = "N/A"


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "slug", "description")
    search_fields = ("title",)
    empty_value_display = "N/A"
