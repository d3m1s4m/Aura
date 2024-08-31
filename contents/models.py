from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from custom_lib.common_models import BaseModel
from locations.models import Location
from .tasks import process_post_content

User = get_user_model()


class Post(BaseModel):
    caption = models.TextField(_("caption"), blank=True, null=True)
    user = models.ForeignKey(
        User, related_name="posts", on_delete=models.CASCADE, verbose_name=_("user")
    )
    location = models.ForeignKey(
        Location, related_name='posts', on_delete=models.SET_NULL,
        blank=True, null=True, verbose_name=_("location")
    )

    def clean(self):
        """validate caption length"""
        super().clean()
        max_caption_length = 400
        if self.caption and len(self.caption) > max_caption_length:
            raise ValidationError({
                'caption': _('Caption cannot exceed 400 characters.')
            })

    def save(self, *args, **kwargs):
        """process post contents async before saving"""
        self.full_clean()  # ensure validation is run before saving
        super().save(*args, **kwargs)
        process_post_content.delay(self.id)  # trigger async task

    def __str__(self):
        return f'{self.user.username}: {self.id}'

    class Meta:
        verbose_name = _("post")
        verbose_name_plural = _("posts")


class Media(BaseModel):
    IMAGE = 1
    VIDEO = 2
    MEDIA_TYPE = (
        (IMAGE, _("Image")),
        (VIDEO, _("Video"))
    )

    post = models.ForeignKey(
        Post, related_name="media", on_delete=models.CASCADE, verbose_name=_("post")
    )
    media_type = models.PositiveSmallIntegerField(_("media type"), choices=MEDIA_TYPE, default=IMAGE)
    file = models.FileField(
        _("file"), upload_to='contents/media/',
        validators=[FileExtensionValidator(
            allowed_extensions=('jpg', 'jpeg', 'png', 'mp4', 'wmv', 'flv')
        )]
    )

    def clean(self):
        """limit file size"""
        super().clean()
        max_file_size = 10 * 1024 * 1024  # 10MB
        if self.file.size > max_file_size:
            raise ValidationError(_('File size must be under 10MB.'))

    def __str__(self):
        return f'{self.post} - {self.get_media_type_display()}:{self.id}'

    class Meta:
        verbose_name = _("media")
        verbose_name_plural = _("media")


class Tag(BaseModel):
    name = models.CharField(_("name"), max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("tag")
        verbose_name_plural = _("tags")
        ordering = ('name',)


class PostTag(BaseModel):
    post = models.ForeignKey(
        Post, related_name="tags", on_delete=models.CASCADE, verbose_name=_("post")
    )
    tag = models.ForeignKey(
        Tag, related_name="posts", on_delete=models.CASCADE, verbose_name=_("tag")
    )

    def __str__(self):
        return f'{self.post} - {self.tag.name}'

    class Meta:
        verbose_name = _("post tag")
        verbose_name_plural = _("posts tags")


class TaggedUser(BaseModel):
    user = models.ForeignKey(
        User, related_name='tagged_posts', on_delete=models.CASCADE, verbose_name=_("user")
    )
    post = models.ForeignKey(
        Post, related_name='tagged_users', on_delete=models.CASCADE, verbose_name=_("post")
    )

    def __str__(self):
        return f'{self.user.username} mentioned in {self.post.id}'

    class Meta:
        verbose_name = _("tagged user")
        verbose_name_plural = _("tagged users")
        unique_together = ('post', 'user')
