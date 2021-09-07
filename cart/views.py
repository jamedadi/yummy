from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from django.views.generic import View

from cart.models import Cart, CartLine
from item.models import Item


@method_decorator(require_http_methods(('POST',)), name='dispatch')
@method_decorator(login_required(login_url=reverse_lazy('accounts:customer-login-register')), name='dispatch')
class AddToCartView(View):
    model = CartLine

    def post(self, request, *args, **kwargs):
        cart = Cart.get_cart(self.request.user)
        item = get_object_or_404(Item, pk=self.kwargs.get('item_pk'))
        cart.create_or_increase(item)

        return HttpResponseRedirect(
            reverse_lazy('item:list', kwargs={'service_pk': item.service.pk}))