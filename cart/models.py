from django.db import models
from django.utils.translation import gettext as _
from accounts.models import Customer
from item.models import Item
from library.models import BaseModel
from payment.models import Invoice


class Cart(BaseModel):
    customer = models.ForeignKey(Customer, verbose_name=_('customer'), null=True, blank=True, related_name='carts',
                                 on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False, verbose_name=_('is paid'))
    invoice = models.OneToOneField(Invoice, verbose_name=_('invoice'), related_name='cart', on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.customer} - {'Paid' if self.is_paid else 'Not paid'}"

    class Meta:
        verbose_name = _('cart')
        verbose_name_plural = _('carts')
        db_table = 'cart'


class CartLine(BaseModel):
    item = models.ForeignKey(Item, verbose_name=_('item'), related_name='lines', on_delete=models.SET_NULL)
    cart = models.ForeignKey(Cart, verbose_name=_('cart'), related_name='lines', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, verbose_name=_('quantity'))

    def __str__(self):
        return f"{self.item} - {self.quantity}"

    class Meta:
        verbose_name = _('cart line')
        verbose_name_plural = _('cart lines')
        db_table = 'cart_line'
