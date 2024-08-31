from django.contrib import admin
from django.utils.html import format_html

from contents.models import Media, Post, PostTag, TaggedUser, Tag


class MediaInline(admin.TabularInline):
    model = Media

    extra = 1
    readonly_fields = ('thumbnail',)

    @staticmethod
    def thumbnail(instance):
        if instance.file and instance.file.name:
            if instance.media_type == Media.IMAGE:
                return format_html(f'<img src="{instance.file.url}" width=100px height=100px />')
        return ''


class PostTagInline(admin.TabularInline):
    model = PostTag

    extra = 0


class TaggedUserInline(admin.TabularInline):
    model = TaggedUser

    extra = 0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = (MediaInline, PostTagInline, TaggedUserInline)

    actions = ('export_as_json',)
    autocomplete_fields = ('user',)
    list_display = ('user', 'caption', 'location', 'created_at')
    list_per_page = 10
    search_fields = ('user__username__istartswith', 'caption')

    def save_model(self, request, obj, form, change):
        """ensure the clean method is called before saving"""
        obj.full_clean()  # call full_clean to enforce the validation
        super().save_model(request, obj, form, change)

    @admin.action(description='Export selected posts as JSON')
    def export_as_json(self, request, queryset):
        from django.http import JsonResponse

        data = list(queryset.values())
        response = JsonResponse(data, safe=False)
        response['Content-Disposition'] = 'attachment; filename="posts.json"'
        return response


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    actions = ('export_as_json',)
    list_display = ('name', 'created_at')
    list_per_page = 10
    search_fields = ('name',)

    @admin.action(description='Export selected tags as JSON')
    def export_as_json(self, request, queryset):
        from django.http import JsonResponse

        data = list(queryset.values())
        response = JsonResponse(data, safe=False)
        response['Content-Disposition'] = 'attachment; filename="tags.json"'
        return response
