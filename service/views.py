from abc import ABC

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.shortcuts import get_object_or_404, redirect

from accounts.utils import IsServiceProvider
from service.forms import ServiceCreateUpdateForm, ServiceCategoryCreateUpdateForm, DeliveryAreaCreateUpdateForm, \
    ServiceAvailableTimeCreateUpdateForm
from service.models import Service, ServiceCategory, DeliveryArea, ServiceAvailableTime
from service.utils import CustomServiceIsServiceProvider


class BaseCreateView(ABC):
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.service = get_object_or_404(Service, pk=self.kwargs['service_pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['service'] = self.service
        return context


class BaseServiceCategory(ABC, IsServiceProvider):
    model = ServiceCategory
    form_class = ServiceCategoryCreateUpdateForm
    template_name = 'service_category/create_update_form.html'

    def get_success_url(self):
        return reverse_lazy('service:service-detail', kwargs={'pk': self.object.service.pk})


class BaseDeliveryArea(ABC, IsServiceProvider):
    model = DeliveryArea
    form_class = DeliveryAreaCreateUpdateForm
    template_name = 'delivery_area/create_update_form.html'

    def get_success_url(self):
        return reverse_lazy('service:service-detail', kwargs={'pk': self.object.service.pk})


class BaseServiceAvailableTime(ABC, IsServiceProvider):
    model = ServiceAvailableTime
    form_class = ServiceAvailableTimeCreateUpdateForm
    template_name = 'service_available_time/create_update_form.html'

    def get_success_url(self):
        return reverse_lazy('service:service-detail', kwargs={'pk': self.object.service.pk})


@method_decorator(login_required(login_url=reverse_lazy('accounts:service-provider-login')), name='dispatch')
class ServiceCreateView(IsServiceProvider, CreateView):
    model = Service
    form_class = ServiceCreateUpdateForm
    template_name = 'service/service_provider/create_update_form.html'
    success_url = reverse_lazy('service:service-list')

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.service_provider = self.request.user
        instance.save()
        return super().form_valid(form)


@method_decorator(login_required(login_url=reverse_lazy('accounts:service-provider-login')), name='dispatch')
class ServiceUpdateView(CustomServiceIsServiceProvider, UpdateView):
    model = Service
    form_class = ServiceCreateUpdateForm
    template_name = 'service/service_provider/create_update_form.html'
    success_url = reverse_lazy('service:service-list')


@method_decorator(login_required(login_url=reverse_lazy('accounts:service-provider-login')), name='dispatch')
class ServiceDeleteView(CustomServiceIsServiceProvider, DeleteView):
    model = Service
    template_name = 'service/service_provider/delete_form.html'
    success_url = reverse_lazy('service:service-list')


@method_decorator(login_required(login_url=reverse_lazy('accounts:service-provider-login')), name='dispatch')
class ServiceDetailView(CustomServiceIsServiceProvider, DetailView):
    model = Service
    context_object_name = 'service'
    template_name = 'service/service_provider/detail.html'


@method_decorator(login_required(login_url=reverse_lazy('accounts:service-provider-login')), name='dispatch')
class ServiceListView(IsServiceProvider, ListView):
    model = Service
    context_object_name = 'services'
    template_name = 'service/service_provider/list.html'

    def get_queryset(self):
        return super().get_queryset().filter(service_provider=self.request.user)


@method_decorator(login_required(login_url=reverse_lazy('accounts:service-provider-login')), name='dispatch')
class ServiceCategoryCreateView(BaseServiceCategory, BaseCreateView, CreateView):
    def test_func(self):
        return self.service.service_provider == self.request.user and super().test_func()

    def get_success_url(self):
        return reverse_lazy('service:service-detail', kwargs={'pk': self.service.pk})

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.service = self.service
        instance.save()
        return super().form_valid(form)


@method_decorator(login_required(login_url=reverse_lazy('accounts:service-provider-login')), name='dispatch')
class ServiceCategoryUpdateView(BaseServiceCategory, UpdateView):

    def test_func(self):
        obj = self.get_object()
        return obj.service.service_provider == self.request.user and super().test_func()


@method_decorator(login_required(login_url=reverse_lazy('accounts:service-provider-login')), name='dispatch')
class ServiceCategoryDeleteView(BaseServiceCategory, DeleteView):
    context_object_name = 'category'
    template_name = 'service_category/delete_form.html'

    def test_func(self):
        obj = self.get_object()
        return obj.service.service_provider == self.request.user and super().test_func()


@method_decorator(login_required(login_url=reverse_lazy('accounts:service-provider-login')), name='dispatch')
class ServiceCategoryDetailView(BaseServiceCategory, DetailView):
    context_object_name = 'category'
    template_name = 'service_category/detail.html'

    def test_func(self):
        obj = self.get_object()
        return obj.service.service_provider == self.request.user and super().test_func()


@method_decorator(login_required(login_url=reverse_lazy('accounts:service-provider-login')), name='dispatch')
class DeliveryAreaCreate(BaseDeliveryArea, BaseCreateView, CreateView):

    def get_success_url(self):
        return reverse_lazy('service:service-detail', kwargs={'pk': self.service.pk})

    def test_func(self):
        return self.service.service_provider == self.request.user and super().test_func()

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.service = self.service
        instance.save()
        return super().form_valid(form)


@method_decorator(login_required(login_url=reverse_lazy('accounts:service-provider-login')), name='dispatch')
class DeliveryUpdateView(BaseDeliveryArea, UpdateView):
    def test_func(self):
        obj = self.get_object()
        return obj.service.service_provider == self.request.user and super().test_func()


@method_decorator(login_required(login_url=reverse_lazy('accounts:service-provider-login')), name='dispatch')
class DeliveryDeleteView(BaseDeliveryArea, DeleteView):
    context_object_name = 'delivery'
    template_name = 'delivery_area/delete_form.html'

    def test_func(self):
        obj = self.get_object()
        return obj.service.service_provider == self.request.user and super().test_func()


@method_decorator(login_required(login_url=reverse_lazy('accounts:service-provider-login')), name='dispatch')
class ServiceAvailableTimeCreateView(BaseServiceAvailableTime, BaseCreateView, CreateView):
    def test_func(self):
        return self.service.service_provider == self.request.user and super().test_func()

    def get_success_url(self):
        return reverse_lazy('service:service-detail', kwargs={'pk': self.service.pk})

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
class ServiceAvailableTimeUpdateView(BaseServiceAvailableTime, UpdateView):
    def test_func(self):
        obj = self.get_object()
        return obj.service.service_provider == self.request.user and super().test_func()


@method_decorator(login_required(login_url=reverse_lazy('accounts:service-provider-login')), name='dispatch')
class ServiceAvailableTimeDeleteView(BaseServiceAvailableTime, DeleteView):
    context_object_name = 'available_time'
    template_name = 'service_available_time/delete_form.html'

    def test_func(self):
        obj = self.get_object()
        return obj.service.service_provider == self.request.user and super().test_func()
