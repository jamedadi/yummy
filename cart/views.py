from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from django.views.generic import View, DeleteView, DetailView

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


@method_decorator(require_http_methods(('POST',)), name='dispatch')
@method_decorator(login_required(login_url=reverse_lazy('accounts:customer-login-register')), name='dispatch')
class CartLineDeleteView(DeleteView):
    model = CartLine

    def get_success_url(self):
        return reverse_lazy('item:list', kwargs={'service_pk': self.object.item.service.pk})


@method_decorator(require_http_methods(('POST',)), name='dispatch')
@method_decorator(login_required(login_url=reverse_lazy('accounts:customer-login-register')), name='dispatch')
class CartLineDecreaseView(DetailView):
    model = CartLine

    def get_success_url(self):
        return reverse_lazy('item:list', kwargs={'service_pk': self.object.item.service.pk})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        with transaction.atomic():
            if self.object.quantity >= 2:
                self.object.quantity += -1
                self.object.save()
        return HttpResponseRedirect(self.get_success_url())
