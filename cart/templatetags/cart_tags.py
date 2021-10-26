from django import template
from django.db.models import Sum, F


from cart.models import Cart

register = template.Library()


@register.simple_tag
def get_cart(request, service):
    try:
        cart = Cart.objects.get(id=request.COOKIES.get('cart_id', None), is_paid=False)
    except Cart.DoesNotExist:
        return None
    else:
        if cart.lines.filter(item__service=service).exists():
            return cart
    return None


@register.simple_tag
def calculate_total_price(cart):
    price = cart.lines.annotate(true_price=(F('quantity') * F('item__price'))).aggregate(Sum('true_price'))
    return price['true_price__sum']
