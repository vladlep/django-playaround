from django.db import models
from django.db.models import FileField
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


def generate_cost_name(instance, filename):
    import os
    from time import strftime
    f, ext = os.path.splitext(filename)
    new_filename = strftime("%s")
    return 'costs/%s%s' % (new_filename, ext)


class Cost(models.Model):
    number = models.CharField("Cost number", max_length=50)
    image = FileField(upload_to=generate_cost_name, null=True, blank=True)
    description = models.TextField(blank=True)
    amount = models.DecimalField(_('Total amount'), decimal_places=2, max_digits=40, null=True, blank=True)
    date = models.DateField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class CostLine(models.Model):
    cost = models.ForeignKey(Cost, related_name='cost_lines')
    amount = models.DecimalField(decimal_places=2, max_digits=40, null=True, blank=True)
    tax_rate = models.DecimalField(decimal_places=2, max_digits=40, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u'%s' % self.amount