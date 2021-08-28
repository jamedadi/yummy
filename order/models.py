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
    invoice = models.ForeignKey(Invoice, verbose_name=_('invoice'), related_name='orders', on_delete=models.PROTECT)
    status = models.PositiveSmallIntegerField(verbose_name=_('status'), choices=STATUS)
    is_delivered = models.BooleanField(verbose_name=_('is delivered'), default=False)
