from django.urls import path
from .views import ServiceProviderRegistrationView, ServiceProviderLoginView, LogoutView, ServiceProviderProfileView

app_name = 'accounts'
urlpatterns = [
    path(
        'serviceprovider/registration/', ServiceProviderRegistrationView.as_view(), name='service-provider-registration'
    ),
    path('serviceprovider/login/', ServiceProviderLoginView.as_view(), name='service-provider-login'),
    path('serviceprovider/profile/', ServiceProviderProfileView.as_view(), name='service-provider-profile'),
    path('user/logout/', LogoutView.as_view(), name='user-logout')
]
