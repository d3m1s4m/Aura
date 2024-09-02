from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from contents.models import Post
from custom_lib.common_models import BaseModel

User = get_user_model()


class Comment(BaseModel):
    text = models.TextField(_("text"))
    user = models.ForeignKey(
        User, related_name="comments", on_delete=models.CASCADE, verbose_name=_("user")
    )
    post = models.ForeignKey(
        Post, related_name="comments", on_delete=models.CASCADE, verbose_name=_("post")
    )
    reply_to = models.ForeignKey(
        'self', related_name="replies", on_delete=models.CASCADE, verbose_name=_("reply to"),
        blank=True, null=True
    )

    def clean(self):
        """validate comment text length"""
        super().clean()
        max_caption_length = 256
        if self.text and len(self.text) > max_caption_length:
            raise ValidationError({
                'caption': _('Comment text cannot exceed 256 characters.')
            })

    def save(self, *args, **kwargs):
        self.full_clean()  # ensure validation is run before saving
        super().save(*args, **kwargs)

    def __str__(self):
        return self.text[:100]

    class Meta:
        verbose_name = _("comment")
        verbose_name_plural = _("comments")


class Like(models.Model):
    user = models.ForeignKey(
        User, related_name="likes", on_delete=models.CASCADE, verbose_name=_("user")
    )
    post = models.ForeignKey(
        Post, related_name="likes", on_delete=models.CASCADE, verbose_name=_("post")
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} liked {self.post.id}"

    class Meta:
        verbose_name = _("like")
        verbose_name_plural = _("likes")
        unique_together = ('user', 'post')


class Save(models.Model):
    user = models.ForeignKey(
        User, related_name="saves", on_delete=models.CASCADE, verbose_name=_("user")
    )
    post = models.ForeignKey(
        Post, related_name="saves", on_delete=models.CASCADE, verbose_name=_("post")
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} saved {self.post.id}"

    class Meta:
        verbose_name = _("save")
        verbose_name_plural = _("saves")
        unique_together = ('user', 'post')
