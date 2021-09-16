from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.http import require_http_methods

from address.models import CustomerAddress
from cart.models import Cart
from library.utils import CustomUserPasses
from payment.forms import AddressSelectForm, GatewaySelectForm
from payment.models import Payment, Invoice


@method_decorator(require_http_methods(['POST', 'GET']), name='dispatch')
@method_decorator(login_required(login_url=reverse_lazy('accounts:customer-login-register')), name='dispatch')
class CheckoutView(CustomUserPasses, View):

    def test_func(self):
        if not self.cart.lines.exists():
            return False
        return True

    def dispatch(self, request, *args, **kwargs):
        cart_id = self.request.COOKIES.get('cart_id', None)
        self.cart = get_object_or_404(Cart, pk=cart_id)
        if self.cart.customer is None:
            self.cart.customer = request.user
            self.cart.save()

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        address_form = AddressSelectForm()
        address_form.base_fields['address'].queyset = CustomerAddress.objects.filter(customer_user=request.user)
        gateway_form = GatewaySelectForm()
        return render(request, 'payment/checkout.html',
                      context={'address_form': address_form, 'gateway_form': gateway_form}
                      )

    def post(self, request, *args, **kwargs):
        address_form = AddressSelectForm(request.POST)
        gateway_form = GatewaySelectForm(request.POST)

        if address_form.is_valid() and gateway_form.is_valid():
            address = address_form.cleaned_data['address']
            gateway = gateway_form.cleaned_data['gateway']
            with transaction.atomic():
                payment = Invoice.create(request.user, self.cart, address=address, gateway=gateway)
                bank_url = payment.bank_page

            return HttpResponseRedirect(bank_url)
        return self.get(request, *args, **kwargs)


@method_decorator(require_http_methods(['GET']), name='dispatch')
@method_decorator(login_required(login_url=reverse_lazy('accounts:customer-login-register')), name='dispatch')
class PaymentVerify(View):
    def get(self, request, *args, **kwargs):
        authority = self.request.GET.get('Authority', None)
        if authority:
            payment = get_object_or_404(Payment, authority=authority)
            is_paid, ref_id = payment.verify()
            response = render(request, 'payment/verify.html', {'is_paid': is_paid, 'ref_id': ref_id})
            response.delete_cookie('cart_id')
            return response
