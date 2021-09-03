from abc import ABC

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.shortcuts import get_object_or_404, redirect

from django_filters.views import FilterView

from accounts.utils import IsServiceProvider
from service.forms import ServiceCreateUpdateForm, ServiceCategoryCreateUpdateForm, DeliveryAreaCreateUpdateForm, \
    ServiceAvailableTimeCreateUpdateForm
from service.filters import ServiceFilter
from service.models import Service, ServiceCategory, DeliveryArea, ServiceAvailableTime
from service.utils import CustomServiceIsServiceProvider


class BaseServiceView(ABC):
    model = Service
    form_class = ServiceCreateUpdateForm
    template_name = 'service/service_provider/create_update_form.html'


class BaseCreateView(ABC, IsServiceProvider):
    def test_func(self):
        return self.service.service_provider == self.request.user and super().test_func()

    def get_success_url(self):
        return reverse_lazy('service:service-provider-service-detail', kwargs={'pk': self.service.pk})

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.service = get_object_or_404(Service, pk=self.kwargs['service_pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['service'] = self.service
        return context


class BaseOtherView(IsServiceProvider):
    def get_success_url(self):
        return reverse_lazy('service:service-provider-service-detail', kwargs={'pk': self.object.service.pk})

    def test_func(self):
        obj = self.get_object()
        return obj.service.service_provider == self.request.user and super().test_func()


class BaseServiceCategory(ABC, BaseOtherView):
    model = ServiceCategory
    form_class = ServiceCategoryCreateUpdateForm
    template_name = 'service_category/create_update_form.html'


class BaseDeliveryArea(ABC, BaseOtherView):
    model = DeliveryArea
    form_class = DeliveryAreaCreateUpdateForm
    template_name = 'delivery_area/create_update_form.html'


class BaseServiceAvailableTime(ABC, BaseOtherView):
    model = ServiceAvailableTime
    form_class = ServiceAvailableTimeCreateUpdateForm
    template_name = 'service_available_time/create_update_form.html'


@method_decorator(login_required(login_url=reverse_lazy('accounts:service-provider-login')), name='dispatch')
class ServiceProviderServiceCreateView(BaseServiceView, IsServiceProvider, CreateView):
    success_url = reverse_lazy('service:service-provider-service-list')

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.service_provider = self.request.user
        instance.save()
        return super().form_valid(form)


@method_decorator(login_required(login_url=reverse_lazy('accounts:service-provider-login')), name='dispatch')
class ServiceProviderServiceUpdateView(BaseServiceView, CustomServiceIsServiceProvider, UpdateView):
    success_url = reverse_lazy('service:service-provider-service-list')


@method_decorator(login_required(login_url=reverse_lazy('accounts:service-provider-login')), name='dispatch')
class ServiceProviderServiceDeleteView(BaseServiceView, CustomServiceIsServiceProvider, DeleteView):
    template_name = 'service/service_provider/delete_form.html'
    success_url = reverse_lazy('service:service-provider-service-list')


@method_decorator(login_required(login_url=reverse_lazy('accounts:service-provider-login')), name='dispatch')
class ServiceProviderServiceDetailView(BaseServiceView, CustomServiceIsServiceProvider, DetailView):
    context_object_name = 'service'
    template_name = 'service/service_provider/detail.html'


@method_decorator(login_required(login_url=reverse_lazy('accounts:service-provider-login')), name='dispatch')
class ServiceProviderServiceListView(BaseServiceView, IsServiceProvider, ListView):
    context_object_name = 'services'
    template_name = 'service/service_provider/list.html'

    def get_queryset(self):
        return super().get_queryset().filter(service_provider=self.request.user)


@method_decorator(login_required(login_url=reverse_lazy('accounts:service-provider-login')), name='dispatch')
class ServiceProviderServiceCategoryCreateView(BaseCreateView, CreateView):
    model = ServiceCategory
    form_class = ServiceCategoryCreateUpdateForm
    template_name = 'service_category/create_update_form.html'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.service = self.service
        instance.save()
        return super().form_valid(form)


@method_decorator(login_required(login_url=reverse_lazy('accounts:service-provider-login')), name='dispatch')
class ServiceProviderServiceCategoryUpdateView(BaseServiceCategory, UpdateView):
    pass


@method_decorator(login_required(login_url=reverse_lazy('accounts:service-provider-login')), name='dispatch')
class ServiceProviderServiceCategoryDeleteView(BaseServiceCategory, DeleteView):
    context_object_name = 'category'
    template_name = 'service_category/delete_form.html'


@method_decorator(login_required(login_url=reverse_lazy('accounts:service-provider-login')), name='dispatch')
class ServiceProviderDeliveryAreaCreate(BaseCreateView, CreateView):
    model = DeliveryArea
    form_class = DeliveryAreaCreateUpdateForm
    template_name = 'delivery_area/create_update_form.html'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.service = self.service
        instance.save()
        return super().form_valid(form)


@method_decorator(login_required(login_url=reverse_lazy('accounts:service-provider-login')), name='dispatch')
class ServiceProviderDeliveryUpdateView(BaseDeliveryArea, UpdateView):
    pass


@method_decorator(login_required(login_url=reverse_lazy('accounts:service-provider-login')), name='dispatch')
class ServiceProviderDeliveryDeleteView(BaseDeliveryArea, DeleteView):
    context_object_name = 'delivery'
    template_name = 'delivery_area/delete_form.html'


@method_decorator(login_required(login_url=reverse_lazy('accounts:service-provider-login')), name='dispatch')
class ServiceProviderServiceAvailableTimeCreateView(BaseCreateView, CreateView):
    model = ServiceAvailableTime
    form_class = ServiceAvailableTimeCreateUpdateForm
    template_name = 'service_available_time/create_update_form.html'

    def form_valid(self, form):
        with transaction.atomic():
            instance = form.save(commit=False)
            if self.service.available_times.filter(day=instance.day).exists():
                messages.info(self.request, f'This Service {self.service.name} has this day time', 'danger')
                return redirect(self.get_success_url())
            instance.service = self.service
            instance.save()
            return super().form_valid(form)


@method_decorator(login_required(login_url=reverse_lazy('accounts:service-provider-login')), name='dispatch')
class ServiceProviderServiceAvailableTimeUpdateView(BaseServiceAvailableTime, UpdateView):
    pass


@method_decorator(login_required(login_url=reverse_lazy('accounts:service-provider-login')), name='dispatch')
class ServiceProviderServiceAvailableTimeDeleteView(BaseServiceAvailableTime, DeleteView):
    context_object_name = 'available_time'
    template_name = 'service_available_time/delete_form.html'


class ServiceListView(FilterView):
    model = Service
    context_object_name = 'services'
    template_name = 'service/list.html'
    filterset_class = ServiceFilter
    queryset = Service.objects.filter(available=True)
