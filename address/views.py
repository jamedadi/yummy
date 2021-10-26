from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, DeleteView, ListView

from accounts.models import ServiceProvider
from accounts.utils import IsCustomer, IsServiceProvider
from address.forms import CustomerAddressCreateUpdateForm, ServiceAddressCreateUpdateForm
from address.models import CustomerAddress, ServiceAddress
from library.utils import CustomUserPasses
from service.models import Service


class BaseAddress:
    model = CustomerAddress
    form_class = CustomerAddressCreateUpdateForm
    template_name = 'address/create_update_form.html'


@method_decorator(login_required(login_url=reverse_lazy('accounts:customer-login-register')), name='dispatch')
class CustomerAddressCreateView(BaseAddress, IsCustomer, CreateView):
    success_url = reverse_lazy('accounts:customer-profile')

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.customer_user = self.request.user
        instance.save()
        return super().form_valid(form)


@method_decorator(login_required(login_url=reverse_lazy('accounts:customer-login-register')), name='dispatch')
class CustomerAddressUpdateView(BaseAddress, IsCustomer, UpdateView):
    success_url = reverse_lazy('address:customer-address-list')

    def test_func(self):
        result = super().test_func()
        obj = self.get_object()
        return result and obj.customer_user == self.request.user

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        return super().form_valid(form)


@method_decorator(login_required(login_url=reverse_lazy('accounts:customer-login-register')), name='dispatch')
class CustomerAddressDeleteView(IsCustomer, DeleteView):
    model = CustomerAddress
    template_name = 'address/delete_form.html'
    success_url = reverse_lazy('accounts:customer-profile')

    def test_func(self):
        result = super().test_func()
        obj = self.get_object()
        return result and obj.customer_user == self.request.user


@method_decorator(login_required(login_url=reverse_lazy('accounts:customer-login-register')), name='dispatch')
class CustomerAddressListView(ListView):
    model = CustomerAddress
    template_name = 'address/customer_address_list.html'
    context_object_name = 'addresses'

    def get_queryset(self):
        return super().get_queryset().filter(customer_user=self.request.user)


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['service'] = self.service
        return context

    def test_func(self):
        if not isinstance(self.request.user, ServiceProvider):
            return False
        if self.service.service_provider != self.request.user:
            return False
        if self.service.address:
            return False, True, reverse_lazy('accounts:service-provider-profile')
        return True

    def form_valid(self, form):
        with transaction.atomic():
            instance = form.save()
            self.service.address = instance
            self.service.save()
            return super().form_valid(form)


@method_decorator(login_required(login_url=reverse_lazy('accounts:service-provider-login')), name='dispatch')
class ServiceAddressUpdateView(IsServiceProvider, UpdateView):
    model = ServiceAddress
    form_class = ServiceAddressCreateUpdateForm
    template_name = 'address/create_update_form.html'
    success_url = reverse_lazy('accounts:service-provider-profile')

    def test_func(self):
        result = super().test_func()
        obj = self.get_object()
        return result and obj.services.service_provider == self.request.user
