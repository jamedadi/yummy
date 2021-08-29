from django.contrib.auth.hashers import make_password
from django.urls import reverse_lazy
from django.views.generic import FormView
from .forms import ServiceProviderRegistrationForm


class ServiceProviderRegistrationView(FormView):
    form_class = ServiceProviderRegistrationForm
    template_name = 'accounts/service_provider_registration.html'
    success_url = reverse_lazy('accounts:service-provider-login')

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.password = make_password(instance.password)
        instance.save()
        return self.form_valid(form)
