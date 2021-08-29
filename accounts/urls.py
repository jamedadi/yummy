from django.urls import path
from .views import ServiceProviderRegistrationView, ServiceProviderLoginView

app_name = 'accounts'
urlpatterns = [
    path(
        'serviceprovider/registration/', ServiceProviderRegistrationView.as_view(), name='service-provider-registration'
    ),
    path('serviceprovider/login/', ServiceProviderLoginView.as_view(), name='service-provider-login'),
]
