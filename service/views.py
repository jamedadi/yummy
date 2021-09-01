from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView

from accounts.utils import IsServiceProvider
from service.forms import ServiceCreateForm
from service.models import Service


@method_decorator(login_required(login_url=reverse_lazy('accounts:service-provider-login')), name='dispatch')
class ServiceCreateView(IsServiceProvider, CreateView):
    model = Service
    form_class = ServiceCreateForm
    template_name = 'service/create_form.html'
    success_url = reverse_lazy('accounts:service-provider-profile')

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.service_provider = self.request.user
        instance.save()
        return super().form_valid(form)


@method_decorator(login_required(login_url=reverse_lazy('accounts:service-provider-login')), name='dispatch')
class ServiceListView(IsServiceProvider, ListView):
    model = Service
    context_object_name = 'services'
    template_name = 'service/list.html'

    def get_queryset(self):
        return super().get_queryset().filter(service_provider=self.request.user)
