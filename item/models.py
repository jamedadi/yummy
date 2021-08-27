from django.db import models
from django.utils.translation import gettext as _

from library.models import BaseModel


class Item(BaseModel):
    upc = models.BigIntegerField(unique=True, db_index=True)
    available = models.BooleanField(default=True)
    name = models.CharField(verbose_name=_('name'), max_length=50)
    description = models.TextField(verbose_name=_('description'), blank=True)
    price = models.IntegerField(verbose_name=_('price'))
    image = models.ImageField(verbose_name=_('image'), blank=True, null=True, upload_to='items/')

    # TODO-1: Service model must be created for the relation
    # TODO-2 : ServiceCategory must be created for the relation

    class Meta:
        verbose_name = _('item')
        verbose_name_plural = _('items')
        db_table = 'item'

    def __str__(self):
        return self.name

    @property
    def stock(self):
        return self.line.quantity


class ItemLine(BaseModel):
    item = models.OneToOneField(Item, related_name='line', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = _('item line')
        verbose_name_plural = _('item lines')
        db_table = 'item_line'
