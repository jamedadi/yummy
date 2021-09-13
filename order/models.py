from django.db import models
from library.models import BaseModel
from django.utils.translation import ugettext_lazy as _

from payment.models import Invoice


class Order(BaseModel):
    PREPARING_FOOD = 0
    SENDING = 1

    STATUS = (
        (PREPARING_FOOD, _('preparing food')),
        (PREPARING_FOOD, _('sending')),
    )
    invoice = models.OneToOneField(Invoice, verbose_name=_('invoice'), related_name='order', on_delete=models.PROTECT)
    status = models.PositiveSmallIntegerField(verbose_name=_('status'), choices=STATUS, default=PREPARING_FOOD)
    is_delivered = models.BooleanField(verbose_name=_('is delivered'), default=False)

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')
        db_table = 'order'
