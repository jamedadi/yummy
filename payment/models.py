from django.db import models
from django.utils.translation import gettext as _
from accounts.models import Customer
from address.models import CustomerAddress
from library.models import BaseModel
import uuid


class Invoice(BaseModel):
    customer = models.ForeignKey(Customer, verbose_name=_('customer'), related_name='invoices',
                                 on_delete=models.SET_NULL, null=True)
    price = models.IntegerField(verbose_name=_('price'))
    is_paid = models.BooleanField(verbose_name=_('is paid'), default=False)
    cart = models.OneToOneField(verbose_name=_('cart'), related_name='invoice', on_delete=models.PROTECT)
    address = models.ForeignKey(CustomerAddress, verbose_name=_('address'), related_name='invoices',
                                on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = _('Invoice')
        verbose_name_plural = _('Invoices')
        db_table = 'invoice'

    def __str__(self):
        return f"{self.customer} - {self.price} - {'Paid' if self.is_paid else 'Not paid'}"


class Payment(BaseModel):
    uuid = models.UUIDField(unique=True, verbose_name=_('uuid'), db_index=True, default=uuid.uuid4)
    invoice = models.OneToOneField(Invoice, verbose_name=_('invoice'), related_name='payment', on_delete=models.CASCADE)
    price = models.IntegerField(verbose_name=_('price'))
    is_paid = models.BooleanField(verbose_name=_('is paid'), default=False)

    class Meta:
        verbose_name = _('Payment')
        verbose_name_plural = _('Payments')
        db_table = 'payment'

    def __str__(self):
        return f"{self.price} - {'Paid' if self.is_paid else 'Not paid'}"
