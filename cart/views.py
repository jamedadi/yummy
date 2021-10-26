from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from django.views.generic import View

from accounts.models import Customer
from cart.models import Cart, CartLine
from item.models import Item


class BaseCartView(View):
    def check_customer(self, cart):
        user = self.request.user
        if user.is_authenticated:
            if not isinstance(user, Customer):
                raise Http404
            if cart.customer is None:
                cart.customer = user
                cart.save()
                return cart
            else:
                if user != cart.customer:
                    raise Http404
                return cart
        elif cart.customer is not None:
            return Cart.objects.create()
        else:
            return cart

    def get_cart_set_cookie(self, redirect_url=None):
        response = HttpResponseRedirect(redirect_url)
        cart = Cart.get_cart(self.request.COOKIES.get('cart_id', None))
        cart = self.check_customer(cart)
        response.set_cookie('cart_id', cart.pk, max_age=15 * 60)
        return cart, response


@method_decorator(require_http_methods(('POST',)), name='dispatch')
class AddToCartView(BaseCartView):

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.kwargs['item'] = get_object_or_404(Item, pk=request.POST['item_id'])

    def get_success_url(self):
        return reverse_lazy('item:list', kwargs={'service_pk': self.kwargs['item'].service.pk})

    def post(self, request, *args, **kwargs):
        cart, response = self.get_cart_set_cookie(self.get_success_url())
        cart.create_or_increase(self.kwargs['item'])
        return response


@method_decorator(require_http_methods(('POST',)), name='dispatch')
class CartLineDeleteView(BaseCartView):
    model = CartLine

    def get_success_url(self):
        return reverse_lazy('item:list', kwargs={'service_pk': self.kwargs['cart_line'].item.service.pk})

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.kwargs['cart_line'] = get_object_or_404(CartLine, pk=self.kwargs['pk'])

    def post(self, request, *args, **kwargs):
        cart, response = self.get_cart_set_cookie(self.get_success_url())
        if self.kwargs['cart_line'].cart != cart:
            raise Http404
        self.kwargs['cart_line'].delete()
        return response


@method_decorator(require_http_methods(('POST',)), name='dispatch')
class CartLineDecreaseView(BaseCartView):

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.kwargs['cart_line'] = get_object_or_404(CartLine, id=self.kwargs['pk'])

    def get_success_url(self):
        return reverse_lazy('item:list', kwargs={'service_pk': self.kwargs['cart_line'].item.service.pk})

    def post(self, request, *args, **kwargs):
        cart, response = self.get_cart_set_cookie(self.get_success_url())
        if self.kwargs['cart_line'].cart != cart:
            raise Http404

        if self.kwargs['cart_line'].quantity >= 2:
            self.kwargs['cart_line'].quantity -= 1
            self.kwargs['cart_line'].save()

        return response


@method_decorator(require_http_methods(('POST',)), name='dispatch')
class EmptyCartView(BaseCartView):

    def post(self, request, *args, **kwargs):
        cart = Cart.get_cart(self.request.COOKIES.get('cart_id', None))
        cart = self.check_customer(cart)
        cart.empty_cart()
        cart.save()
        response = HttpResponseRedirect(reverse_lazy('item:list', kwargs={'service_pk': cart.service.pk}))
        return response
