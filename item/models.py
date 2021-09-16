import random
import string

from django.db import models
from django.urls import reverse_lazy
from django.utils.translation import gettext as _

from library.models import BaseModel
from service.models import Service, ServiceCategory


class ItemManager(models.Manager):
    def available(self):
        return self.get_queryset().filter(available=True)


class Item(BaseModel):
    upc = models.BigIntegerField(verbose_name=_('upc'), unique=True, db_index=True, editable=False)
    available = models.BooleanField(verbose_name=_('available'), default=True)
    name = models.CharField(verbose_name=_('name'), max_length=50)
    description = models.TextField(verbose_name=_('description'), blank=True)
    price = models.IntegerField(verbose_name=_('price'))
    image = models.ImageField(verbose_name=_('image'), blank=True, null=True, upload_to='items/')
    service = models.ForeignKey(Service, verbose_name=_('service'), related_name='items', on_delete=models.CASCADE)
    category = models.ForeignKey(ServiceCategory, verbose_name=_('category'), related_name='items',
                                 on_delete=models.CASCADE)
    objects = ItemManager()

    class Meta:
        verbose_name = _('Item')
        verbose_name_plural = _('Items')
        db_table = 'item'

    @property
    def stock(self):
        return self.line.quantity

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.pk is None:  # only when we the instance is created
            random_digits = ''.join(random.choice(string.digits) for _ in range(5))
            self.upc = int(random_digits)
        return super().save(force_insert, force_update, using, update_fields)

    def get_absolute_url(self):
        return reverse_lazy("item:detail", kwargs={'pk': self.pk})


class ItemLine(BaseModel):
    item = models.OneToOneField(Item, verbose_name=_('item'), related_name='line', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0, verbose_name=_('quantity'))

    class Meta:
        verbose_name = _('Item line')
        verbose_name_plural = _('Item lines')
        db_table = 'item_line'

    def __str__(self):
        return f"{self.quantity}"
