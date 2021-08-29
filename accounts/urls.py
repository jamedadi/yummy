from django.urls import path, reverse_lazy
from .views import ServiceProviderRegistrationView, ServiceProviderLoginView, ServiceProviderProfileView
from django.contrib.auth.views import LogoutView
app_name = 'accounts'
urlpatterns = [
    path(
        'serviceprovider/registration/', ServiceProviderRegistrationView.as_view(), name='service-provider-registration'
    ),
    path('serviceprovider/login/', ServiceProviderLoginView.as_view(), name='service-provider-login'),
    path('serviceprovider/profile/', ServiceProviderProfileView.as_view(), name='service-provider-profile'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('accounts:service-provider-login')), name='logout')
]
