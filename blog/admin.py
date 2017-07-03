from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from taggit_helpers.admin import TaggitCounter

from .models import Post


class PostModelAdmin(TaggitCounter, SummernoteModelAdmin, admin.ModelAdmin):
    list_display = ["title", "updated", "timestamp", "taggit_counter"]
    list_display_links = ["updated"]
    list_editable = ["title"]
    list_filter = ["updated", "timestamp"]

    search_fields = ["title", "content"]

    class Meta:
        model = Post


admin.site.register(Post, PostModelAdmin)
