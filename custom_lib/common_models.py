from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    created_at = models.DateTimeField(_("created time"), auto_now_add=True)
    modified_at = models.DateTimeField(_("modified time"), auto_now=True)

    class Meta:
        abstract = True
