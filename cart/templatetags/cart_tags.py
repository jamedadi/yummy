from django import template
from django.db.models import Sum, F

from accounts.models import Customer

register = template.Library()


@register.simple_tag
def get_cart(request, service):
    if request.user.is_authenticated and isinstance(request.user, Customer):
        cart = request.user.carts.filter(is_paid=False).last()
        if cart and cart.lines.filter(item__service=service).exists():
            return cart
    return None


@register.simple_tag
def calculate_total_price(cart):
    price = cart.lines.annotate(true_price=(F('quantity') * F('item__price'))).aggregate(Sum('true_price'))
    return price['true_price__sum']