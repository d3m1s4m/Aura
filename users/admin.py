from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import User


@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    actions = ('deactivate_users', 'activate_users')
    list_display = (
        'username', 'email', 'is_staff', 'is_private', 'is_verified', 'is_active'
    )
    list_filter = (
        'is_staff', 'is_private', 'is_verified', 'is_active'
    )
    list_per_page = 10
    readonly_fields = ('date_joined', 'date_modified', 'last_login', 'avatar_thumbnail')
    search_fields = (
        'username', 'email', 'first_name__istartswith', 'last_name__istartswith'
    )

    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "bio", "avatar", "avatar_thumbnail")}),
        (_("Account status"), {"fields": ("is_active", "is_private", "is_verified")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined", "date_modified")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "password1", "password2"),
            },
        ),
    )

    @admin.action(description='Deactivate selected users')
    def deactivate_users(self, request, queryset):
        updated_count = queryset.update(is_active=False)
        self.message_user(
            request,
            f'Successfully deactivated {updated_count} users.',
            messages.SUCCESS
        )

    @admin.action(description='Activate selected users')
    def activate_users(self, request, queryset):
        updated_count = queryset.update(is_active=True)
        self.message_user(
            request,
            f'Successfully activated {updated_count} users.',
            messages.SUCCESS
        )

    @staticmethod
    def avatar_thumbnail(instance):
        if instance.avatar.name != '':
            return format_html(f'<img src="{instance.avatar.url}" width=100px height=100px />')
        return ''
