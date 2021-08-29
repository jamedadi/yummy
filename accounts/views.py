from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from django.views.generic import FormView, RedirectView, TemplateView
from .forms import ServiceProviderRegistrationForm, ServiceProviderLoginForm


@method_decorator(require_http_methods(['POST', 'GET']), name='dispatch')
class ServiceProviderRegistrationView(FormView):
    form_class = ServiceProviderRegistrationForm
    template_name = 'accounts/service_provider/registration.html'
    success_url = reverse_lazy('accounts:service-provider-login')

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.password = make_password(instance.password)
        instance.save()
        return super().form_valid(form)


@method_decorator(require_http_methods(['POST', 'GET']), name='dispatch')
class ServiceProviderLoginView(FormView):
    form_class = ServiceProviderLoginForm
    template_name = 'accounts/service_provider/login.html'
    success_url = reverse_lazy('accounts:service-provider-profile')

    def form_valid(self, form):
        user = form.cleaned_data['user']
        user_authenticated = authenticate(username=user.username, password=user.password)
        if user_authenticated:
            login(self.request, user_authenticated)
        return super().form_valid(form)


@method_decorator(login_required(), name='dispatch')
class ServiceProviderProfileView(TemplateView):
    template_name = 'accounts/service_provider/profile.html'


class LogoutView(RedirectView):
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            logout(self.request)
        return super().get(request, *args, **kwargs)
