from django.db import models
from django.utils.translation import gettext_lazy as _

from custom_lib.common_models import BaseModel


class Location(BaseModel):
    name = models.CharField(_("name"), max_length=255)
    lat = models.DecimalField(_("latitude"), max_digits=9, decimal_places=6)
    long = models.DecimalField(_("longitude"), max_digits=9, decimal_places=6)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("location")
        verbose_name_plural = _("locations")
        unique_together = ('lat', 'long')
        constraints = [
            models.UniqueConstraint(fields=['name', 'lat', 'long'], name='unique_location')
        ]
