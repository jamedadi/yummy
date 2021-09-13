from django.db import models, transaction
from django.db.models import Sum, F
from django.utils.translation import gettext as _
from accounts.models import Customer
from item.models import Item
from library.models import BaseModel
from service.models import Service


class Cart(BaseModel):
    customer = models.ForeignKey(
        Customer,
        verbose_name=_('customer'),
        null=True, blank=True,
        related_name='carts',
        on_delete=models.CASCADE
    )
    is_paid = models.BooleanField(default=False, verbose_name=_('is paid'))
    service = models.ForeignKey(
        Service,
        verbose_name=_('service'),
        related_name='carts',
        on_delete=models.PROTECT,
        null=True
    )

    def __str__(self):
        return f"{self.customer} - {'Paid' if self.is_paid else 'Not paid'}"

    @property
    def total_price(self):
        return self.lines.all().annotate(price=F('quantity') * F('item__price')).aggregate(
            total_price=Sum('price')).get('total_price')

    @classmethod
    def get_cart(cls, cart_id):
        if cart_id is None:
            cart = cls.objects.create()
        else:
            cart, created = cls.objects.get_or_create(pk=cart_id)
        return cart

    def create_or_increase(self, item):
        with transaction.atomic():

            if item.service != self.service:  # adding the first item or item with different service
                self.empty_cart()
                self.service = item.service
                self.save()

            cart_line, create = self.lines.select_for_update().get_or_create(item=item, defaults={'cart': self})
            if not create:
                cart_line.quantity += 1
                cart_line.save()

    def empty_cart(self):
        self.lines.all().delete()

    class Meta:
        verbose_name = _('Cart')
        verbose_name_plural = _('Carts')
        db_table = 'cart'


class CartLine(BaseModel):
    item = models.ForeignKey(Item, verbose_name=_('item'), related_name='lines', on_delete=models.PROTECT)
    cart = models.ForeignKey(Cart, verbose_name=_('cart'), related_name='lines', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, verbose_name=_('quantity'))

    def __str__(self):
        return f"{self.item} - {self.quantity}"

    @property
    def price(self):
        return self.item.price * self.quantity

    class Meta:
        verbose_name = _('Cart line')
        verbose_name_plural = _('Cart lines')
        db_table = 'cart_line'
        ordering = ('created_time', 'modified_time')
        unique_together = ('item', 'cart')  # each cart can have one cart line with the same item
