from django.db import models
from django.utils.translation import gettext as _
from accounts.models import Customer
from library.models import BaseModel


class Invoice(BaseModel):
    customer = models.ForeignKey(Customer, verbose_name=_('customer'), related_name='invoices',
                                 on_delete=models.SET_NULL)
    price = models.IntegerField(verbose_name=_('price'))
    is_paid = models.BooleanField(verbose_name=_('is paid'), default=False)

    #  TODO: Address must be created for relation

    class Meta:
        verbose_name = _('invoice')
        verbose_name_plural = _('invoices')
        db_table = 'invoice'
