from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    first_name = models.CharField(_("first name"), max_length=150, blank=True, null=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True, null=True)
    email = models.EmailField(_("email address"), unique=True)
    avatar = models.ImageField(_("avatar"), upload_to="users/avatars", default="users/avatars/default.png")
    bio = models.TextField(_("bio"), blank=True, null=True)
    is_private = models.BooleanField(_("private"), default=False)
    is_verified = models.BooleanField(_("verified"), default=False)
    date_modified = models.DateTimeField(_("date modified"), auto_now=True)

    def __str__(self):
        return self.username
