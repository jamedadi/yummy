from django.contrib.auth.mixins import UserPassesTestMixin
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView

from address.forms import CustomerAddressCreateUpdateForm, ServiceAddressCreateUpdateForm
from address.models import CustomerAddress, ServiceAddress
from service.models import Service


class BaseAddress:
    model = CustomerAddress
    form_class = CustomerAddressCreateUpdateForm
    template_name = 'address/create_update_form.html'


class CustomerAddressCreateView(BaseAddress, CreateView):
    success_url = reverse_lazy('accounts:customer-profile')

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        return super().form_valid(form)


class CustomerAddressUpdateView(BaseAddress, UpdateView):
    success_url = reverse_lazy('accounts:customer-profile')

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        return super().form_valid(form)


class CustomerAddressDeleteView(DeleteView):
    model = CustomerAddress
    template_name = 'address/delete_form.html'
    success_url = reverse_lazy('accounts:customer-profile')


class ServiceAddressCreateView(CreateView):
    model = ServiceAddress
    form_class = ServiceAddressCreateUpdateForm
    template_name = 'address/create_update_form.html'
    success_url = reverse_lazy('accounts:service-provider-profile')
    raise_exception = True

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.service = get_object_or_404(Service, id=self.kwargs['service_pk'])

    def form_valid(self, form):
        with transaction.atomic():
            instance = form.save()
            self.service.address = instance
            self.service.save()
            return super().form_valid(form)


class ServiceAddressUpdateView(UpdateView):
    model = ServiceAddress
    form_class = ServiceAddressCreateUpdateForm
    template_name = 'address/create_update_form.html'
    success_url = reverse_lazy('accounts:service-provider-profile')

    def form_valid(self, form):
        with transaction.atomic():
            instance = form.save(commit=False)
            if self.request.user == instance.services.last().service_provider:
                instance.save()
        return super().form_valid(form)
