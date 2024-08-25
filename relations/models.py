from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from custom_lib.common_models import BaseModel


User = get_user_model()


class FollowRelation(BaseModel):
    from_user = models.ForeignKey(
        User, related_name="followings", on_delete=models.CASCADE, verbose_name=_("from user")
    )
    to_user = models.ForeignKey(
        User, related_name="followers", on_delete=models.CASCADE, verbose_name=_("to user")
    )
    is_accepted = models.BooleanField(_("accepted"), default=False)

    def accept(self):
        """accept the follow request"""
        self.is_accepted = True
        self.save()

    def decline(self):
        """decline the follow request"""
        self.delete()

    def __str__(self):
        return f'{self.from_user} > {self.to_user}'

    class Meta:
        verbose_name = _("follow relation")
        verbose_name_plural = _("follow relations")
        unique_together = ('from_user', 'to_user')
        ordering = ('-created_at',)


class BlockRelation(models.Model):
    blocker = models.ForeignKey(
        User, related_name="blocking", on_delete=models.CASCADE, verbose_name=_("blocker")
    )
    blocked = models.ForeignKey(
        User, related_name="blocked_by", on_delete=models.CASCADE, verbose_name=_("blocked by")
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.blocker} blocked {self.blocked}'

    class Meta:
        verbose_name = _("block relation")
        verbose_name_plural = _("block relations")
        unique_together = ('blocker', 'blocked')
        ordering = ('-created_at',)
