from django.urls import path
from .views import ServiceProviderRegistrationView, ServiceProviderLoginView, UserLogoutView, ServiceProviderProfileView

app_name = 'accounts'
urlpatterns = [
    path(
        'serviceprovider/registration/', ServiceProviderRegistrationView.as_view(), name='service-provider-registration'
    ),
    path('serviceprovider/login/', ServiceProviderLoginView.as_view(), name='service-provider-login'),
    path('serviceprovider/profile/', ServiceProviderProfileView.as_view(), name='service-provider-profile'),
    path('user/logout/', UserLogoutView.as_view(), name='user-logout')
]
