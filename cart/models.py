from django.db import models
from django.utils.translation import gettext as _
from accounts.models import Customer
from library.models import BaseModel


class Cart(BaseModel):
    customer = models.ForeignKey(Customer, verbose_name=_('customer'), null=True, blank=True, related_name='carts',
                                 on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False, verbose_name=_('is paid'))

    #  TODO-1: Invoice model must be created for the relation

    def __str__(self):
        return f"{self.customer} - {'Paid' if self.is_paid else 'Not paid'}"
