from django.contrib import admin

from .models import FollowRelation, BlockRelation


@admin.register(FollowRelation)
class FollowRelationAdmin(admin.ModelAdmin):
    autocomplete_fields = ('from_user', 'to_user')
    list_display = ('from_user', 'to_user', 'is_accepted')
    list_display_links = ('from_user', 'to_user')
    list_filter = ('is_accepted',)
    list_per_page = 10
    search_fields = ('from_user__username__istartswith', 'to_user__username__istartswith')


@admin.register(BlockRelation)
class BlockRelationAdmin(admin.ModelAdmin):
    autocomplete_fields = ('blocker', 'blocked')
    list_display = ('blocker', 'blocked')
    list_display_links = ('blocker', 'blocked')
    list_per_page = 10
    search_fields = ('blocker__username__istartswith', 'blocked__username__istartswith')
