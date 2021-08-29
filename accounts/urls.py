from django.urls import path
from .views import ServiceProviderRegistrationView

app_name = 'accounts'
urlpatterns = [
    path(
        'seviceprovider/registration/', ServiceProviderRegistrationView.as_view(), name='service-provider-registration'
    ),
]
