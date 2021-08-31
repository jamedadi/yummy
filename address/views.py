from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, DeleteView

from accounts.models import Customer, ServiceProvider
from address.forms import CustomerAddressCreateUpdateForm, ServiceAddressCreateUpdateForm
from address.models import CustomerAddress, ServiceAddress
from library.utils import CustomUserPasses
from service.models import Service


class BaseAddress:
    model = CustomerAddress
    form_class = CustomerAddressCreateUpdateForm
    template_name = 'address/create_update_form.html'


@method_decorator(login_required(login_url=reverse_lazy('accounts:customer-login-register')), name='dispatch')
class CustomerAddressCreateView(BaseAddress, CreateView):
    success_url = reverse_lazy('accounts:customer-profile')

    def test_func(self):
        if not isinstance(self.request.user, Customer):
            return False

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        return super().form_valid(form)


@method_decorator(login_required(login_url=reverse_lazy('accounts:customer-login-register')), name='dispatch')
class CustomerAddressUpdateView(BaseAddress, UpdateView):
    success_url = reverse_lazy('accounts:customer-profile')

    def test_func(self):
        if not isinstance(self.request.user, Customer):
            return False

        obj = self.get_object()
        if obj.services.service_provider != self.request.user:
            return False

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        return super().form_valid(form)


@method_decorator(login_required(login_url=reverse_lazy('accounts:customer-login-register')), name='dispatch')
class CustomerAddressDeleteView(CustomUserPasses, DeleteView):
    model = CustomerAddress
    template_name = 'address/delete_form.html'
    success_url = reverse_lazy('accounts:customer-profile')

    def test_func(self):
        if not isinstance(self.request.user, Customer):
            return False

        obj = self.get_object()
        if obj.customer_user != self.request.user:
            return False


@method_decorator(login_required(login_url=reverse_lazy('accounts:service-provider-login')), name='dispatch')
class ServiceAddressCreateView(CustomUserPasses, CreateView):
    model = ServiceAddress
    form_class = ServiceAddressCreateUpdateForm
    template_name = 'address/create_update_form.html'
    success_url = reverse_lazy('accounts:service-provider-profile')
    raise_exception = True

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.service = get_object_or_404(Service, id=self.kwargs['service_pk'])

    def test_func(self):
        if not isinstance(self.request.user, ServiceProvider):
            return False
        if self.service.service_provider != self.request.user:
            return False
        if self.service.address:
            return False, True, reverse_lazy('accounts:service-provider-profile')

    def form_valid(self, form):
        with transaction.atomic():
            instance = form.save()
            self.service.address = instance
            self.service.save()
            return super().form_valid(form)


@method_decorator(login_required(login_url=reverse_lazy('accounts:service-provider-login')), name='dispatch')
class ServiceAddressUpdateView(CustomUserPasses, UpdateView):
    model = ServiceAddress
    form_class = ServiceAddressCreateUpdateForm
    template_name = 'address/create_update_form.html'
    success_url = reverse_lazy('accounts:service-provider-profile')

    def test_func(self):
        if not isinstance(self.request.user, ServiceProvider):
            return False

        obj = self.get_object()
        if obj.services.service_provider != self.request.user:
            return False
