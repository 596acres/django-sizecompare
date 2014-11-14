from django.db import models
from django.utils.translation import ugettext_lazy as _


class SizeComparable(models.Model):
    name = models.CharField(_('name'), max_length=250)
    sqft = models.IntegerField(_('square feet'))

    def __unicode__(self):
        return self.name
