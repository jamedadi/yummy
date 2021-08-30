from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView

from address.forms import CustomerAddressCreateUpdateForm
from address.models import CustomerAddress


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
