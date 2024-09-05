from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from contents.models import Post

User = get_user_model()


class Notification(models.Model):
    LIKE = 1
    COMMENT = 2
    FOLLOW = 3
    SAVE = 4
    MENTION = 5
    ACCEPT_REQUEST = 6
    FOLLOW_REQUEST = 7
    NOTIFICATION_TYPES = [
        (LIKE, _('Like')),
        (COMMENT, _('Comment')),
        (FOLLOW, _('Follow')),
        (SAVE, _('Save')),
        (MENTION, _('Mention')),
        (ACCEPT_REQUEST, _('Accept request')),
        (FOLLOW_REQUEST, _('Follow request')),
    ]

    sender = models.ForeignKey(
        User, related_name='sent_notifications', on_delete=models.CASCADE, verbose_name=_("sender")
    )
    receiver = models.ForeignKey(
        User, related_name='received_notifications', on_delete=models.CASCADE, verbose_name=_("receiver")
    )
    notification_type = models.PositiveSmallIntegerField(
        choices=NOTIFICATION_TYPES, verbose_name=_("notification type")
    )
    post = models.ForeignKey(
        Post, related_name='notifications', on_delete=models.CASCADE, verbose_name=_("post"),
        blank=True, null=True
    )
    is_read = models.BooleanField(_("read"), default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} {self.get_notification_type_display()} {self.receiver}"

    class Meta:
        verbose_name = _("notification")
        verbose_name_plural = _("notifications")
        ordering = ('-created_at',)
