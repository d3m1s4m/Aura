from django.contrib import admin, messages

from notifications.models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    actions = ('mark_as_read', 'mark_as_unread', 'export_as_json')
    autocomplete_fields = ('receiver', 'sender', 'post')
    list_display = ('receiver', 'sender', 'is_read', 'notification_type')
    list_editable = ('is_read',)
    list_filter = ('is_read', 'notification_type')
    list_per_page = 10
    search_fields = ('receiver__username__istartswith',)

    @admin.action(description='Export selected notifications as JSON')
    def export_as_json(self, request, queryset):
        from django.http import JsonResponse

        data = list(queryset.values())
        response = JsonResponse(data, safe=False)
        response['Content-Disposition'] = 'attachment; filename="notifications.json"'
        return response

    @admin.action(description='Mark selected notifications as read')
    def mark_as_read(self, request, queryset):
        updated_count = queryset.update(is_read=True)
        self.message_user(
            request,
            f'Successfully marked {updated_count} notifications as read.',
            messages.SUCCESS
        )

    @admin.action(description='Mark selected notifications as unread')
    def mark_as_unread(self, request, queryset):
        updated_count = queryset.update(is_read=False)
        self.message_user(
            request,
            f'Successfully marked {updated_count} notifications as unread.',
            messages.SUCCESS
        )



