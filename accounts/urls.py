from django.urls import path
from .views import ServiceProviderRegistrationView

app_name = 'accounts'
urlpatterns = [
    path(
        'serviceprovider/registration/', ServiceProviderRegistrationView.as_view(), name='service-provider-registration'
    ),
]
