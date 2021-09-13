from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.http import require_http_methods

from address.models import CustomerAddress
from payment.forms import AddressSelectForm, GatewaySelectForm


@method_decorator(require_http_methods(['POST', 'GET']), name='dispatch')
@method_decorator(login_required(login_url=reverse_lazy('accounts:customer-login-register')), name='dispatch')
class CheckoutView(View):

    def get(self, request, *args, **kwargs):
        address_form = AddressSelectForm()
        address_form.base_fields['address'].queyset = CustomerAddress.objects.filter(customer_user=request.user)
        gateway_form = GatewaySelectForm()
        return render(request, 'payment/checkout.html',
                      context={'address_form': address_form, 'gateway_form': gateway_form}
                      )
