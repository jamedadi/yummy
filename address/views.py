from django.urls import reverse_lazy
from django.views.generic import CreateView

from address.forms import CustomerAddressCreateForm
from address.models import CustomerAddress


class CustomerAddressCreateView(CreateView):
    model = CustomerAddress
    form_class = CustomerAddressCreateForm
    template_name = 'address/create.html'
    success_url = reverse_lazy('accounts:customer-profile')

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        return super().form_valid(form)
