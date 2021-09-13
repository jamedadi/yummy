from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, DetailView

from accounts.models import Customer
from accounts.utils import IsCustomer
from library.utils import CustomUserPasses
from order.models import Order


@method_decorator(require_http_methods(['GET']), name='dispatch')
@method_decorator(login_required(login_url=reverse_lazy('accounts:customer-login-register')), name='dispatch')
class CustomerOrdersListView(IsCustomer, ListView):
    template_name = 'order/customer/order_list.html'
    context_object_name = 'active_orders'

    def get_queryset(self):
        return Order.objects.select_related('invoice__cart').filter(customer=self.request.user, status__in=(0, 1))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['delivered_orders'] = Order.objects.select_related('invoice__cart').filter(customer=self.request.user,
                                                                                           status=2)
        return context


@method_decorator(require_http_methods(['GET']), name='dispatch')
@method_decorator(login_required(login_url=reverse_lazy('accounts:customer-login-register')), name='dispatch')
class CustomerOrderDetailView(CustomUserPasses, DetailView):
    model = Order
    template_name = 'order/customer/order_detail.html'
    context_object_name = 'order'

    def test_func(self):
        user = self.request.user
        if not isinstance(user, Customer):
            return False
        if self.get_object().customer != self.request.user:
            return False
        return True
