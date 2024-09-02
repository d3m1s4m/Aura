from django.contrib import admin
from django.utils.html import format_html

from activities.models import Comment, Like, Save


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    actions = ('export_as_json',)
    autocomplete_fields = ('user', 'post')
    list_display = ('text', 'user', 'post', 'reply_to')
    list_per_page = 10
    search_fields = ('text', 'user__username__istartswith')

    @admin.action(description='Export selected comments as JSON')
    def export_as_json(self, request, queryset):
        from django.http import JsonResponse

        data = list(queryset.values())
        response = JsonResponse(data, safe=False)
        response['Content-Disposition'] = 'attachment; filename="comments.json"'
        return response


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    actions = ('export_as_json',)
    autocomplete_fields = ('user', 'post')
    list_display = ('user', 'post', 'created_at')
    list_per_page = 10
    search_fields = ('user__username__istartswith',)

    @admin.action(description='Export selected likes as JSON')
    def export_as_json(self, request, queryset):
        from django.http import JsonResponse

        data = list(queryset.values())
        response = JsonResponse(data, safe=False)
        response['Content-Disposition'] = 'attachment; filename="likes.json"'
        return response


@admin.register(Save)
class SaveAdmin(admin.ModelAdmin):
    actions = ('export_as_json',)
    autocomplete_fields = ('user', 'post')
    list_display = ('user', 'post', 'created_at')
    list_per_page = 10
    search_fields = ('user__username__istartswith',)

    @admin.action(description='Export selected saves as JSON')
    def export_as_json(self, request, queryset):
        from django.http import JsonResponse

        data = list(queryset.values())
        response = JsonResponse(data, safe=False)
        response['Content-Disposition'] = 'attachment; filename="saves.json"'
        return response

