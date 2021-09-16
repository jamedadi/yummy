from django.db import models

from accounts.models import Customer
from library.models import BaseModel
from django.utils.translation import ugettext_lazy as _

from payment.models import Invoice


class Order(BaseModel):
    PREPARING_FOOD = 0
    SENDING = 1
    DELIVERED = 2
    STATUS = (
        (PREPARING_FOOD, _('preparing food')),
        (SENDING, _('sending')),
        (DELIVERED, _('delivered'))
    )
    invoice = models.OneToOneField(Invoice, verbose_name=_('invoice'), related_name='order', on_delete=models.PROTECT)
    customer = models.ForeignKey(Customer, verbose_name=_('customer'), related_name='orders', on_delete=models.PROTECT)
    status = models.PositiveSmallIntegerField(verbose_name=_('status'), choices=STATUS, default=PREPARING_FOOD)

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')
        db_table = 'order'

    def __str__(self):
        return f"{self.customer} - {self.status}"

    @classmethod
    def create(cls, invoice):
        cls.objects.create(invoice=invoice, customer=invoice.customer)
