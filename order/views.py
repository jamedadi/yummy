from abc import ABC

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, DetailView, UpdateView

from django_filters.views import FilterView

from order.filters import OrderFilter
from order.models import Order
from service.models import Service

from library.utils import CustomUserPasses


class BaseOrderServiceList(CustomUserPasses):
    model = Order

    def test_func(self):
        if self.service.service_provider != self.request.user:
            return False
        return True


class BaseOrderDetailUpdate(CustomUserPasses):
    model = Order

    def test_func(self):
        order = self.get_object()
        if order.invoice.cart.service.service_provider != self.request.user:
            return False
        return True


@method_decorator(require_http_methods(['GET']), name='dispatch')
@method_decorator(login_required(login_url=reverse_lazy('accounts:service-provider-login')), name='dispatch')
class OrderServiceListFilterView(FilterView):
    context_object_name = 'orders'
    filterset_class = OrderFilter
    template_name = 'order/service/order_filter_list.html'

    def dispatch(self, request, *args, **kwargs):
        self.service = get_object_or_404(Service, pk=self.kwargs.get('service_pk', None))
        if self.service.service_provider != self.request.user:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Order.objects.filter(invoice__cart__service=self.service)


@method_decorator(require_http_methods(['GET']), name='dispatch')
@method_decorator(login_required(login_url=reverse_lazy('accounts:service-provider-login')), name='dispatch')
class OrderServiceListView(BaseOrderServiceList, ListView):
    context_object_name = 'orders'
    template_name = 'order/service/order_list.html'

    def dispatch(self, request, *args, **kwargs):
        self.service = get_object_or_404(Service, pk=self.kwargs.get('service_pk', None))
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        today = timezone.now()
        time_filter = dict(
            created_time__day=today.strftime('%d'),
            created_time__month=today.strftime('%m'),
            created_time__year=today.strftime('%Y')
        )
        return Order.objects.exclude(is_delivered=True).filter(invoice__cart__service=self.service, **time_filter)


@method_decorator(require_http_methods(['GET']), name='dispatch')
@method_decorator(login_required(login_url=reverse_lazy('accounts:service-provider-login')), name='dispatch')
class OrderServiceDetailView(BaseOrderDetailUpdate, DetailView):
    context_object_name = 'order'
    template_name = 'order/service/order_detail.html'


@method_decorator(require_http_methods(['GET', 'POST']), name='dispatch')
@method_decorator(login_required(login_url=reverse_lazy('accounts:service-provider-login')), name='dispatch')
class OrderServiceUpdateView(BaseOrderDetailUpdate, UpdateView):
    fields = ('status',)
    context_object_name = 'order'
    template_name = 'order/service/order_update.html'

    def get_success_url(self):
        order = self.get_object()
        return reverse_lazy('order:service-order-list', kwargs={'service_pk': order.invoice.cart.service.id})
