from django.contrib import admin

from .models import FollowRelation, BlockRelation


@admin.register(FollowRelation)
class FollowRelationAdmin(admin.ModelAdmin):
    actions = ('export_as_json',)
    autocomplete_fields = ('from_user', 'to_user')
    list_display = ('from_user', 'to_user', 'is_accepted')
    list_display_links = ('from_user', 'to_user')
    list_filter = ('is_accepted',)
    list_per_page = 10
    search_fields = ('from_user__username__istartswith', 'to_user__username__istartswith')

    @admin.action(description='Export selected follow relations as JSON')
    def export_as_json(self, request, queryset):
        from django.http import JsonResponse

        data = list(queryset.values('from_user__username', 'to_user__username', 'is_accepted'))
        response = JsonResponse(data, safe=False)
        response['Content-Disposition'] = 'attachment; filename="follow_relations.json"'
        return response


@admin.register(BlockRelation)
class BlockRelationAdmin(admin.ModelAdmin):
    actions = ('export_as_json',)
    autocomplete_fields = ('blocker', 'blocked')
    list_display = ('blocker', 'blocked')
    list_display_links = ('blocker', 'blocked')
    list_per_page = 10
    search_fields = ('blocker__username__istartswith', 'blocked__username__istartswith')

    @admin.action(description='Export selected block relations as JSON')
    def export_as_json(self, request, queryset):
        from django.http import JsonResponse

        data = list(queryset.values('blocker', 'blocked'))
        response = JsonResponse(data, safe=False)
        response['Content-Disposition'] = 'attachment; filename="block_relations.json"'
        return response
